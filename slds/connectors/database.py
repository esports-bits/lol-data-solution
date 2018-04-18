import pandas as pd
import os
import mysql.connector as mariadb
from pymongo import MongoClient
from config.constants import RAW_DATA_PATH, EXCEL_EXPORT_PATH, CSV_EXPORT_PATH_MERGED, EXCEL_EXPORT_PATH_MERGED, \
    LEAGUES_DATA_DICT, CSV_EXPORT_PATH, IDS_FILE_PATH, SQL_EXPORTS_CONN, SQL_LEAGUES_CONN, MONGODB_CREDENTIALS


class DataBase:
    def __init__(self, region, league):
        self.region = region
        self.league = league
        self.mongo_conn = MongoClient(MONGODB_CREDENTIALS)
        self.mongo_db = self.mongo_conn.slds
        self.sql_exports_conn = mariadb.connect(**SQL_EXPORTS_CONN)
        self.sql_leagues_conn = mariadb.connect(**SQL_LEAGUES_CONN)

    def get_league_game_ids(self, **kwargs):
        if self.league == 'SOLOQ':
            soloq_m_coll = self.mongo_db.soloq_m
            soloq_tl_coll = self.mongo_db.soloq_tl
            cursor = soloq_m_coll.find({}, {'_id': 0, 'gameId': 1})
            ids = [gid['gameId'] for gid in cursor]
        return None

    @staticmethod
    def get_new_ids(old, new):
        return list(set(map(int, new)) - set(map(int, old)))

    def get_new_game_ids(self):
        league = self.league
        if league == ' SOLOQ':
            soloq_m_coll = self.mongo_db.soloq_m
            cursor = soloq_m_coll.find({}, {'_id': 0, 'gameId': 1})
            old = [gid['gameId'] for gid in cursor]
        else:
            return


def parse_args(args):
    league = args.league.upper()
    region = args.region.upper()
    db = DataBase(region, league)
    if args.download:
        if league == 'SOLOQ':
            if args.n_games:
                n_games = args.n_games
            else:
                n_games = 20
            ids = db.get_league_game_ids(n_games=n_games)
        else:
            ids = db.get_league_game_ids()
        db.download_games(ids=ids, save_dir=LEAGUES_DATA_DICT[league][RAW_DATA_PATH])
        print("Games downloaded.")

    if args.update_static_data:
        db.save_static_data_files()
        print("Static data updated.")

    if args.export:
        if league == 'SOLOQ':
            files = os.listdir(LEAGUES_DATA_DICT[league][RAW_DATA_PATH])
            l1 = [f.split('_')[1] for f in files]
            ids = list(map(int, set([i.split('.')[0] for i in l1])))
            df = db.generate_dataset(read_dir=LEAGUES_DATA_DICT[league][RAW_DATA_PATH],
                                     force_update=args.force_update, game_ids=ids)
        else:
            df = db.generate_dataset(read_dir=LEAGUES_DATA_DICT[league][RAW_DATA_PATH],
                                     force_update=args.force_update)

        if df is not None:
            if args.xlsx:
                df.to_excel('{}'.format(LEAGUES_DATA_DICT[league][EXCEL_EXPORT_PATH]))
            if args.csv:
                df.to_csv('{}'.format(LEAGUES_DATA_DICT[league][CSV_EXPORT_PATH]))
            if not args.csv and not args.xlsx:
                df.to_excel('{}'.format(LEAGUES_DATA_DICT[league][EXCEL_EXPORT_PATH]))
                df.to_csv('{}'.format(LEAGUES_DATA_DICT[league][CSV_EXPORT_PATH]))
            print("Export finished.")
        else:
            print("No export done.")

    if args.merge_soloq and league == 'SOLOQ':
        df1 = pd.read_csv(LEAGUES_DATA_DICT['SOLOQ'][IDS_FILE_PATH], encoding='ISO-8859-1',
                          dtype=LEAGUES_DATA_DICT['SOLOQ']['dtypes'])
        df2 = pd.read_csv(LEAGUES_DATA_DICT['SOLOQ'][CSV_EXPORT_PATH], index_col=0, encoding='ISO-8859-1')
        df3 = df2[pd.notnull(df2.currentAccountId)]
        df3.currentAccountId = df3.currentAccountId.map(int)
        df4 = df3.merge(df1, left_on='currentAccountId', right_on='account_id', how='left')
        df4.to_csv(LEAGUES_DATA_DICT['SOLOQ'][CSV_EXPORT_PATH_MERGED])
        df4.to_excel(LEAGUES_DATA_DICT['SOLOQ'][EXCEL_EXPORT_PATH_MERGED])
        print("Solo Q data merged with pro players data.")
