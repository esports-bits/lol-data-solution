import os
import urllib.request
import json
import pymysql.cursors
import pandas as pd
from pymongo import MongoClient
from itertools import chain
from riotwatcher import RiotWatcher
from tqdm import tqdm
from requests.exceptions import HTTPError
from converters.data2files import get_runes_reforged_json
from converters.data2frames import game_to_dataframe as g2df
from sqlalchemy import create_engine
from datetime import datetime as dt, timedelta
from config.constants import LEAGUES_DATA_DICT, SQL_LEAGUES_CONN, MONGODB_CREDENTIALS, \
    OFFICIAL_LEAGUE, API_KEY, SOLOQ, REGIONS, CUSTOM_PARTICIPANT_COLS, STANDARD_POSITIONS, SCRIMS_POSITIONS_COLS, \
    TOURNAMENT_GAME_ENDPOINT, SQL_LEAGUES_ENGINE, EXCEL_EXPORT_PATH_MERGED, EXPORTS_DIR, EXCEL_EXPORT_PATH, \
    RIFT_GAMES_QUEUES


class DataBase:
    def __init__(self, region, league):
        self.rw = RiotWatcher(API_KEY)
        self.region = region
        self.league = league
        self.mongo_cnx = MongoClient(MONGODB_CREDENTIALS)
        self.mongo_soloq_m_col = self.mongo_cnx.slds.soloq_m
        self.mongo_soloq_tl_col = self.mongo_cnx.slds.soloq_tl
        self.mongo_slo_m_col = self.mongo_cnx.slds.slo_m
        self.mongo_slo_tl_col = self.mongo_cnx.slds.slo_tl
        self.mongo_static_data = self.mongo_cnx.slds.static_data
        self.sql_leagues_cnx = pymysql.connect(**SQL_LEAGUES_CONN)

    def get_recent_game_ids(self, **kwargs):
        if self.league == 'SOLOQ':
            cursor = self.mongo_soloq_m_col.find({'platformId': self.region.upper()}, {'_id': 0, 'gameId': 1})
            current_game_ids = [gid['gameId'] for gid in cursor]

            acc_ids = self.get_account_ids(**kwargs)
            print('\t{} account ids found.'.format(len(acc_ids)))

            # New Solo Q game ids
            new_game_ids = self.get_game_ids(acc_ids=acc_ids, **kwargs)
            return current_game_ids, new_game_ids

    def get_account_ids(self, **kwargs):
        if kwargs['team_abbv'] is not None:
            print('\tLooking for account ids of {} players.'.format(kwargs['team_abbv'].replace(',', ' and ')))
            abbvs = kwargs['team_abbv'].split(',')
            if len(abbvs) == 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE team_abbv = {}'.format('\"' + abbvs[0] + '\"')
            elif len(abbvs) > 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE team_abbv IN {}'.format(tuple(abbvs))
            else:
                print('No abbreviations selected. Check help for more information.')
                return
        elif kwargs['competition'] is not None:
            print('\tLooking for account ids players competing in the {}.'.format(kwargs['competition']))
            competitions = kwargs['competition'].split(',')
            if len(competitions) == 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE competition_abbv = {}' \
                    .format('\"' + competitions[0] + '\"')
            elif len(competitions) > 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE competition_abbv IN {}' \
                    .format(tuple(competitions))
            else:
                print('\tNo names selected. Check help for more information.')
                return
        else:
            print('\tLooking for account ids of every player in the DB.')
            query = 'SELECT DISTINCT account_id FROM soloq'
        cursor = self.sql_leagues_cnx.cursor()
        cursor.execute(query)
        return [gid[0] for gid in cursor]

    @staticmethod
    def get_new_ids(old, new):
        return list(set(map(int, new)) - set(map(int, old)))

    def download_games(self, current_game_ids, new_game_ids):
        def tournament_match_to_dict(id1, hash1, tournament):
            with urllib.request.urlopen(TOURNAMENT_GAME_ENDPOINT.format(tr=tournament, id=id1, hash=hash1)) as url:
                match = json.loads(url.read().decode())
            with urllib.request.urlopen(TOURNAMENT_GAME_ENDPOINT.format(tr=tournament, id=id1, hash=hash1)) as url:
                tl = json.loads(url.read().decode())
            return match, tl
        ids_not_in_db = self.get_new_ids(current_game_ids, new_game_ids)
        print('\t{} new games to be downloaded.'.format(len(ids_not_in_db)))
        if ids_not_in_db:
            for item in tqdm(ids_not_in_db, desc='\tDownloading games'):
                try:
                    if LEAGUES_DATA_DICT[self.league][OFFICIAL_LEAGUE]:
                        pass
                    else:
                        match = self.rw.match.by_id(match_id=item, region=self.region)
                        timeline = self.rw.match.timeline_by_match(match_id=item, region=self.region)
                        data = {'match': match, 'timeline': timeline}
                        self.__save_match_raw_data(data=data)
                except HTTPError:
                    pass
        else:
            print('\tAll games already downloaded.')
        return None

    def get_game_ids(self, acc_ids, **kwargs):
        matchlist_kwargs = {k: kwargs[k] for k in ['begin_index', 'n_games']}
        matchlist_kwargs['queue'] = RIFT_GAMES_QUEUES
        matchlist_kwargs['region'] = self.region
        if matchlist_kwargs['n_games'] is not None and matchlist_kwargs['begin_index'] is not None:
            matchlist_kwargs['end_index'] = matchlist_kwargs['begin_index'] + matchlist_kwargs.pop('n_games')
        elif matchlist_kwargs['n_games'] is not None and matchlist_kwargs['begin_index'] is None:
            matchlist_kwargs['end_index'] = matchlist_kwargs.pop('n_games')
        elif matchlist_kwargs['n_games'] is None:
            matchlist_kwargs['end_index'] = matchlist_kwargs.pop('n_games')

        matches = list(chain.from_iterable(
            [self.rw.match.matchlist_by_account(account_id=acc, **matchlist_kwargs)['matches'] for acc in acc_ids]))
        result = list(set([m['gameId'] for m in matches]))
        return result

    def __save_match_raw_data(self, data, **kwargs):
        if isinstance(data, dict):
            game_id = str(data['match']['gameId'])
            platform_id = data['match']['platformId']
            data['timeline']['gameId'] = game_id
            data['timeline']['platformId'] = platform_id
            if self.league == SOLOQ:
                self.mongo_soloq_m_col.insert_one(data['match'])
                self.mongo_soloq_tl_col.insert_one(data['timeline'])
        else:
            raise TypeError('Dict expected at data param. Should be passed as shown here: {"match": match_dict, '
                            '"timeline": timeline_dict}.')

    def get_supported_leagues(self):
        query = 'SELECT DISTINCT league_abbv FROM soloq'
        cursor = self.sql_leagues_cnx.cursor()
        cursor.execute(query)
        return [abbv[0] for abbv in cursor]

    def get_supported_teams(self):
        query = 'SELECT DISTINCT team_abbv FROM soloq'
        cursor = self.sql_leagues_cnx.cursor()
        cursor.execute(query)
        return [abbv[0] for abbv in cursor]

    def concat_games(self, df):
        if self.league == 'SLO':
            return pd.concat([g2df(match=None,
                                   timeline=None,
                                   custom_positions=STANDARD_POSITIONS,
                                   team_names=list(g[1][['blue', 'red']]),
                                   week=g[1]['week'], database=self.mongo_static_data) for g in df.iterrows()])
        elif self.league == 'SCRIMS':
            return pd.concat([g2df(match=None,
                                   timeline=None,
                                   custom_positions=list(g[1][SCRIMS_POSITIONS_COLS]),
                                   team_names=list(g[1][['blue', 'red']]),
                                   custom_names=list(g[1][CUSTOM_PARTICIPANT_COLS]),
                                   custom=True, enemy=g[1]['enemy'], game_n=g[1]['game_n'], blue_win=g[1]['blue_win'],
                                   database=self.mongo_static_data
                                   ) for g in df.iterrows()])
        elif self.league == 'LCK':
            return pd.concat([g2df(match=None,
                                   timeline=None,
                                   week=g[1]['week'], custom=False,
                                   custom_positions=STANDARD_POSITIONS, database=self.mongo_static_data
                                   ) for g in df.iterrows()])
        elif self.league == 'SOLOQ':
            return pd.concat([g2df(match=self.mongo_soloq_m_col.find_one({'platformId': self.region,
                                                                          'gameId': int(gid)}, {'_id': 0}),
                                   timeline=self.mongo_soloq_tl_col.find_one({'platformId': self.region,
                                                                              'gameId': str(gid)}, {'_id': 0}),
                                   custom=False, database=self.mongo_static_data
                                   ) for gid in list(df.game_id)])

    def get_stored_game_ids(self, **kwargs):
        query = {}
        if kwargs['team_abbv'] is not None or kwargs['competition'] is not None:
            acc_ids = self.get_account_ids(**kwargs)
            query['participantIdentities.player.currentAccountId'] = {'$in': acc_ids}
        if kwargs['patch'] is not None:
            patch = kwargs['patch']
            print('\tLooking for games played on patch {}.'.format(patch))
            regex_patch = '^' + '{}'.format(patch).replace('.', r'\.')
            query['gameVersion'] = {'$regex': regex_patch}
        if kwargs['begin_time'] is not None:
            print('\tLooking for games past {} at 00:00:00.'.format(kwargs['begin_time']))
            timestamp = self.__str_date_to_timestamp(kwargs['begin_time'])
            query['gameCreation'] = {}
            query['gameCreation']['$gte'] = timestamp
        if kwargs['end_time'] is not None:
            print('\tLooking for games before {} at 23:59:59.'.format(kwargs['end_time']))
            td1 = timedelta(hours=23, minutes=59, seconds=59)
            timestamp = self.__str_date_to_timestamp(kwargs['end_time'], td1)
            try:
                query['gameCreation']['$lte'] = timestamp
            except KeyError:
                query['gameCreation'] = {}
                query['gameCreation']['$lte'] = timestamp

        games = self.mongo_soloq_m_col.find(query, {'_id': 0, 'gameId': 1})

        return [g['gameId'] for g in games]

    def close_connections(self):
        self.mongo_cnx.close()
        self.sql_leagues_cnx.close()

    @staticmethod
    def __str_date_to_timestamp(date, time_delta=None):
        if time_delta is not None:
            dt1 = dt.strptime(date, '%d-%m-%Y') + time_delta
        else:
            dt1 = dt.strptime(date, '%d-%m-%Y')
        return int(dt.timestamp(dt1) * 1e3)

    def generate_dataset(self):
        return None

    def save_static_data_files(self):
        versions = {'versions': self.rw.static_data.versions(region=self.region), '_id': 'versions'}
        champs = self.rw.static_data.champions(region=self.region, version=versions['versions'][0])
        items = self.rw.static_data.items(region=self.region, version=versions['versions'][0])
        summs = self.rw.static_data.summoner_spells(region=self.region, version=versions['versions'][0])
        runes = {'runes': get_runes_reforged_json(), '_id': 'runes_reforged'}
        champs['_id'], items['_id'], summs['_id'] = ['champions', 'items', 'summoner_spells']
        self.mongo_static_data.replace_one(filter={'_id': 'versions'}, replacement=versions, upsert=True)
        self.mongo_static_data.replace_one(filter={'_id': 'champions'}, replacement=champs, upsert=True)
        self.mongo_static_data.replace_one(filter={'_id': 'items'}, replacement=items, upsert=True)
        self.mongo_static_data.replace_one(filter={'_id': 'summoner_spells'}, replacement=summs, upsert=True)
        self.mongo_static_data.replace_one(filter={'_id': 'runes_reforged'}, replacement=runes, upsert=True)


def create_dirs():
    if not os.path.exists(EXPORTS_DIR):
        os.makedirs(EXPORTS_DIR)


def parse_args(args):
    create_dirs()
    kwargs = vars(args)
    region = REGIONS[args.region.upper()]
    league = args.league.upper()
    db = DataBase(region, league)
    try:
        if args.update_static_data:
            db.save_static_data_files()
            print('Static data updated.')

        if args.download:
            print('Downloading.')
            if league == 'SOLOQ':
                current_game_ids, new_game_ids = db.get_recent_game_ids(**kwargs)
                db.download_games(current_game_ids=current_game_ids, new_game_ids=new_game_ids)
                print("\tGames downloaded.")
            else:
                pass

        if args.export:
            print('Exporting.')
            if league == 'SOLOQ':
                stored_game_ids = db.get_stored_game_ids(**kwargs)
                print('\t{} games found.'.format(len(stored_game_ids)))
                df = pd.DataFrame(stored_game_ids).rename(columns={0: 'game_id'})
                concatenated_df = db.concat_games(df)
                final_df = concatenated_df

                # Merge Solo Q players info with data
                if args.merge_soloq:
                    engine = create_engine(SQL_LEAGUES_ENGINE)
                    cnx = engine.connect()
                    player_info_df = pd.read_sql_table(con=cnx, table_name='soloq')
                    final_df = final_df.merge(player_info_df, left_on='currentAccountId', right_on='account_id',
                                              how='left')
                    cnx.close()

                    final_df.to_excel(LEAGUES_DATA_DICT['SOLOQ'][EXCEL_EXPORT_PATH_MERGED])
                    print("\tGames merged and exported.")
                    return
                final_df.to_excel(LEAGUES_DATA_DICT['SOLOQ'][EXCEL_EXPORT_PATH])
                print("\tGames exported.")
            else:
                pass
    finally:
        db.close_connections()
