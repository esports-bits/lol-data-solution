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
from converters.data2frames import game_to_dataframe as g2df
from sqlalchemy import create_engine
from config.constants import LEAGUES_DATA_DICT, SQL_LEAGUES_CONN, MONGODB_CREDENTIALS, \
    OFFICIAL_LEAGUE, API_KEY, SOLOQ, REGIONS, CUSTOM_PARTICIPANT_COLS, STANDARD_POSITIONS, SCRIMS_POSITIONS_COLS, \
    TOURNAMENT_GAME_ENDPOINT, SQL_LEAGUES_ENGINE, EXCEL_EXPORT_PATH_MERGED, EXPORTS_DIR, EXCEL_EXPORT_PATH


class DataBase:
    def __init__(self, region, league):
        self.rw = RiotWatcher(API_KEY)
        self.region = region
        self.league = league
        self.mongo_cnx = MongoClient(MONGODB_CREDENTIALS)
        self.mongo_soloq_m_col = self.mongo_cnx.slds.soloq_m
        self.mongo_soloq_tl_col = self.mongo_cnx.slds.soloq_tl
        self.sql_leagues_cnx = pymysql.connect(**SQL_LEAGUES_CONN)

    def get_recent_game_ids(self, **kwargs):
        if self.league == 'SOLOQ':
            cursor = self.mongo_soloq_m_col.find({'platformId': self.region.upper()}, {'_id': 0, 'gameId': 1})
            current_game_ids = [gid['gameId'] for gid in cursor]

            acc_ids = self.get_account_ids(**kwargs)

            # New Solo Q game ids
            if 'n_games' in kwargs:
                n_games = kwargs['n_games']
            else:
                n_games = 20
            if 'begin_index' in kwargs:
                begin_index = kwargs['begin_index']
            else:
                begin_index = 0
            new_game_ids = self.get_soloq_game_ids(acc_ids=acc_ids, n_games=n_games, begin_index=begin_index)
            return current_game_ids, new_game_ids

    def get_account_ids(self, **kwargs):
        if 'team_abbv' in kwargs:
            print('Looking for account ids of {} players.'.format(kwargs['team_abbv']))
            abbvs = kwargs['team_abbv'].split(',')
            if len(abbvs) == 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE team_abbv = {}'.format('\"' + abbvs[0] + '\"')
            elif len(abbvs) > 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE team_abbv IN {}'.format(tuple(abbvs))
            else:
                print('No abbreviations selected. Check help for more information.')
                return
        elif 'competition' in kwargs:
            print('Looking for account ids players competing in the {}.'.format(kwargs['competition']))
            competitions = kwargs['competition'].split(',')
            if len(competitions) == 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE competition_abbv = {}' \
                    .format('\"' + competitions[0] + '\"')
            elif len(competitions) > 1:
                query = 'SELECT DISTINCT account_id FROM soloq WHERE competition_abbv IN {}' \
                    .format(tuple(competitions))
            else:
                print('No names selected. Check help for more information.')
                return
        else:
            print('Looking for account ids of every player in the DB.')
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
        if ids_not_in_db:
            for item in tqdm(ids_not_in_db, desc='Downloading games'):
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
            print('All games already downloaded.')
        return None

    def get_soloq_game_ids(self, acc_ids, **kwargs):
        if 'n_games' in kwargs:
            n_games = kwargs['n_games']
        else:
            n_games = 20

        if 'begin_index' in kwargs:
            begin_index = kwargs['begin_index']
        else:
            begin_index = 0
        matches = list(chain.from_iterable(
            [self.rw.match.matchlist_by_account(account_id=acc, begin_index=begin_index,
                                                end_index=int(begin_index)+int(n_games),
                                                region=self.region,
                                                queue=420)['matches'] for acc in acc_ids]))
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
                                   custom_names=list(g[1][CUSTOM_PARTICIPANT_COLS].T),
                                   custom_positions=STANDARD_POSITIONS,
                                   team_names=list(g[1][['blue', 'red']]),
                                   week=g[1]['week'], custom=True) for g in df.iterrows()])
        elif self.league == 'SCRIMS':
            return pd.concat([g2df(match=None,
                                   timeline=None,
                                   custom_positions=list(g[1][SCRIMS_POSITIONS_COLS]),
                                   team_names=list(g[1][['blue', 'red']]),
                                   custom_names=list(g[1][CUSTOM_PARTICIPANT_COLS]),
                                   custom=True, enemy=g[1]['enemy'], game_n=g[1]['game_n'], blue_win=g[1]['blue_win']
                                   ) for g in df.iterrows()])
        elif self.league == 'LCK':
            return pd.concat([g2df(match=None,
                                   timeline=None,
                                   week=g[1]['week'], custom=False,
                                   custom_positions=STANDARD_POSITIONS) for g in df.iterrows()])
        elif self.league == 'SOLOQ':
            return pd.concat([g2df(match=self.mongo_soloq_m_col.find_one({'platformId': self.region,
                                                                          'gameId': int(gid)}, {'_id': 0}),
                                   timeline=self.mongo_soloq_tl_col.find_one({'platformId': self.region,
                                                                              'gameId': str(gid)}, {'_id': 0}),
                                   custom=False
                                   ) for gid in list(df.game_id)])

    def get_stored_game_ids(self, **kwargs):
        acc_ids = self.get_account_ids(**kwargs)
        games = self.mongo_soloq_m_col.find({'participantIdentities.player.accountId': {'$in': acc_ids}},
                                            {'_id': 0, 'gameId': 1})
        return [obj['gameId'] for obj in games]

    def close_conections(self):
        self.mongo_cnx.close()
        self.sql_leagues_cnx.close()


def create_dirs():
    if not os.path.exists(EXPORTS_DIR):
        os.makedirs(EXPORTS_DIR)


def parse_args(args):
    create_dirs()
    region = REGIONS[args.region.upper()]
    league = args.league.upper()
    db = DataBase(region, league)
    try:
        if args.download:
            if league == 'SOLOQ':
                if args.n_games:
                    n_games = args.n_games
                else:
                    n_games = 20

                if args.team_abbv:
                    team_abbv = args.team_abbv
                    current_game_ids, new_game_ids = db.get_recent_game_ids(n_games=n_games, team_abbv=team_abbv)
                elif args.competition:
                    competition = args.competition
                    current_game_ids, new_game_ids = db.get_recent_game_ids(n_games=n_games, competition=competition)
                else:
                    current_game_ids, new_game_ids = db.get_recent_game_ids(n_games=n_games)
                db.download_games(current_game_ids=current_game_ids, new_game_ids=new_game_ids)
                print("Games downloaded.")
            else:
                pass

        if args.export:
            if league == 'SOLOQ':
                if args.team_abbv:
                    team_abbv = args.team_abbv
                    stored_game_ids = db.get_stored_game_ids(team_abbv=team_abbv)
                elif args.competition:
                    competition = args.competition
                    stored_game_ids = db.get_stored_game_ids(competition=competition)
                else:
                    stored_game_ids = db.get_recent_game_ids()
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
                    print("Games exported.")
                    return
                final_df.to_excel(LEAGUES_DATA_DICT['SOLOQ'][EXCEL_EXPORT_PATH])
                print("Games exported.")
            else:
                pass
    finally:
        db.close_conections()
