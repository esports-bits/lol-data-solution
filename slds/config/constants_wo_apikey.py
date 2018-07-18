from numpy import int64
import re

API_KEY = ""
MONGODB_USER = ''
MONGODB_PASS = ''
MONGODB_URL = ''
MONGODB_CREDENTIALS = {'user': MONGODB_USER, 'password': MONGODB_PASS, 'url': MONGODB_URL}

WORK_DIR = '../'
LEAGUES_DATA_DIR = WORK_DIR + 'leagues_data/'
MATCHES_RAW_DATA_DIR = WORK_DIR + 'matches_raw_data/'
SLO_GAMES_DIR = MATCHES_RAW_DATA_DIR + 'slo_games/'
LCK_GAMES_DIR = MATCHES_RAW_DATA_DIR + 'lck_games/'
SOLOQ_GAMES_DIR = MATCHES_RAW_DATA_DIR + 'soloq/'
SCRIMS_GAMES_DIR = MATCHES_RAW_DATA_DIR + 'scrims/'
EXPORTS_DIR = WORK_DIR + 'exports/'
STATIC_DATA_DIR = WORK_DIR + 'static_data/'

SLO_MATCHES_FILE_PATH = LEAGUES_DATA_DIR + 'slo_spring_S8.csv'
LCK_MATCHES_FILE_PATH = LEAGUES_DATA_DIR + 'lck_spring_S8.csv'
SCRIMS_MATCHES_FILE_PATH = LEAGUES_DATA_DIR + 'scrims.csv'
SOLOQ_MATCHES_FILE_PATH = LEAGUES_DATA_DIR + 'soloq.csv'
SLO_DATASET_CSV = EXPORTS_DIR + 'slo_dataset.csv'
SLO_DATASET_XLSX = EXPORTS_DIR + 'slo_dataset.xlsx'
LCK_DATASET_CSV = EXPORTS_DIR + 'lck_dataset.csv'
LCK_DATASET_XLSX = EXPORTS_DIR + 'lck_dataset.xlsx'
SCRIMS_DATASET_CSV = EXPORTS_DIR + 'scrims_dataset.csv'
SCRIMS_DATASET_XLSX = EXPORTS_DIR + 'scrims_dataset.xlsx'
SOLOQ_DATASET_CSV = EXPORTS_DIR + 'soloq_dataset.csv'
SOLOQ_DATASET_XLSX = EXPORTS_DIR + 'soloq_dataset.xlsx'

DATA_DRAGON_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/{endpoint}'
DD_LANGUAGE = 'en_US'
DD_RUNES_REFORGED = 'runesReforged.json'

CUSTOM_PARTICIPANT_COLS = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']
STANDARD_POSITIONS = ['TOP', 'JUNG', 'MID', 'ADC', 'SUPP', 'TOP', 'JUNG', 'MID', 'ADC', 'SUPP']
SCRIMS_POSITIONS_COLS = ['pos_1', 'pos_2', 'pos_3', 'pos_4', 'pos_5', 'pos_6', 'pos_7', 'pos_8', 'pos_9', 'pos_10']
STATIC_DATA_RELEVANT_COLS = ['id', 'name']
CHAMP_COLS = ["championId"]
RUNES_COLS = ["perk0", "perk1", "perk2", "perk3", "perk4", "perk5", "perkPrimaryStyle", "perkSubStyle"]
ITEMS_COLS = ["item0", "item1", "item2", "item3", "item4", "item5", "item6"]
SUMMS_COLS = ['spell1Id', 'spell2Id']
BANS_COLS = ['ban1_team', 'ban2_team', 'ban3_team', 'ban4_team', 'ban5_team']

LCK = 'LCK'
SLO = 'SLO'
SCRIMS = 'SCRIMS'
SOLOQ = 'SOLOQ'
RAW_DATA_PATH = 'raw_data_path'
IDS_FILE_PATH = 'ids_file_path'
DTYPES = 'dtypes'
EXCEL_EXPORT_PATH = 'excel_export_path'
CSV_EXPORT_PATH = 'csv_export_path'
OFFICIAL_LEAGUE = 'official_league'
CSV_EXPORT_PATH_MERGED = 'csv_export_path_merged'
EXCEL_EXPORT_PATH_MERGED = 'excel_export_path_merged'
LEAGUES_DATA_DICT = {
    LCK: {
        IDS_FILE_PATH: LCK_MATCHES_FILE_PATH,
        RAW_DATA_PATH: LCK_GAMES_DIR,
        OFFICIAL_LEAGUE: True,
        DTYPES: {},
        CSV_EXPORT_PATH: LCK_DATASET_CSV,
        EXCEL_EXPORT_PATH: LCK_DATASET_XLSX},
    SLO: {
        IDS_FILE_PATH: SLO_MATCHES_FILE_PATH,
        RAW_DATA_PATH: SLO_GAMES_DIR,
        OFFICIAL_LEAGUE: False,
        DTYPES: {'datetime': str, 'series_id': str, 'week': int, 'event': str, 'game': int,
                 'game_id': int64, 'blue': str, 'red': str, 'blue_win': int, 'p_1': str,
                 'p_2': str, 'p_3': str, 'p_4': str, 'p_5': str, 'p_6': str, 'p_7': str,
                 'p_8': str, 'p_9': str, 'p_10': str},
        CSV_EXPORT_PATH: EXPORTS_DIR + SLO_DATASET_CSV,
        EXCEL_EXPORT_PATH: EXPORTS_DIR + SLO_DATASET_XLSX},
    SCRIMS: {
        IDS_FILE_PATH: SCRIMS_MATCHES_FILE_PATH,
        RAW_DATA_PATH: SCRIMS_GAMES_DIR,
        OFFICIAL_LEAGUE: False,
        DTYPES: {'date': str, 'enemy': str, 'game_id': int64, 'match_history': str,
                 'blue': str, 'red': str, 'pos_1': str, 'pos_2': str, 'pos_3': str, 'pos_4': str,
                 'pos_5': str,'pos_6': str, 'pos_7': str, 'pos_8': str, 'pos_9': str, 'pos_10': str,
                 'p_1': str, 'p_2': str, 'p_3': str, 'p_4': str, 'p_5': str, 'p_6': str,'p_7': str,
                 'p_8': str, 'p_9': str, 'p_10': str},
        CSV_EXPORT_PATH: SCRIMS_DATASET_CSV,
        EXCEL_EXPORT_PATH: SCRIMS_DATASET_XLSX},
    SOLOQ: {
        IDS_FILE_PATH: SOLOQ_MATCHES_FILE_PATH,
        RAW_DATA_PATH: SOLOQ_GAMES_DIR,
        OFFICIAL_LEAGUE: False,
        DTYPES: {},
        CSV_EXPORT_PATH: SOLOQ_DATASET_CSV,
        EXCEL_EXPORT_PATH: SOLOQ_DATASET_XLSX,
        CSV_EXPORT_PATH_MERGED: EXPORTS_DIR + 'soloq_dataset_merged.csv',
        EXCEL_EXPORT_PATH_MERGED: EXPORTS_DIR + 'soloq_dataset_merged.xlsx'
    }
}

FS = 'FS'
DB = 'DB'
CONNECTORS_DATA_DICT = {
    FS: {},
    DB: {}
}
SUPPORTED_LEAGUES = list(LEAGUES_DATA_DICT.keys())
SUPPORTED_CONNECTORS = list(CONNECTORS_DATA_DICT.keys())

EXPORTS_DB_NAME = 'exports'
LEAGUES_DB_NAME = 'leagues_info'
SQL_EXPORTS_CONN = {'user': '', 'password': '', 'host': '127.0.0.1', 'database': EXPORTS_DB_NAME}
SQL_LEAGUES_CONN = {'user': '', 'password': '', 'host': '127.0.0.1', 'database': LEAGUES_DB_NAME}
SQL_LEAGUES_ENGINE = 'mysql+pymysql://{user}:{password}@localhost/{db}'.format(user='', password='', db=LEAGUES_DB_NAME)
SQL_EXPORTS_ENGINE = 'mysql+pymysql://{user}:{password}@localhost/{db}'.format(user='', password='', db=EXPORTS_DB_NAME)
MONGODB_CONN = 'mongodb+srv://{user}:{password}@{url}'.format(**MONGODB_CREDENTIALS)

REGIONS = {
    'BR': 'BR1',
    'EUNE': 'EUNE1',
    'EUW': 'EUW1',
    'JP': 'JP1',
    'KR': 'KR',
    'LAN': 'LA1',
    'LAS': 'LA2',
    'NA': ['NA1', 'NA'],
    'OCE': 'OC1',
    'TR': 'TR1',
    'RU': 'RU',
    'PBE': 'PBE1'
}

DEFAULT_REGION = REGIONS['EUW']

TOURNAMENT_GAME_ENDPOINT = 'https://acs.leagueoflegends.com/v1/stats/game/{tr}/{id}?gameHash={hash}'
TOURNAMENT_TL_ENDPOINT = 'https://acs.leagueoflegends.com/v1/stats/game/{tr}/{id}/timeline?gameHash={hash}'

PATCH_PATTERN = re.compile(r'^[0-9]{1,2}\.[0-9]{1,2}(\.[0-9]*){0,2}$')

NORMAL_DRAFT_QUEUE_ID = 400
SOLOQ_QUEUE_ID = 420
NORMAL_BLIND_QUEUE_ID = 430
FLEX_QUEUE_ID = 440
RIFT_GAMES_QUEUES = [NORMAL_DRAFT_QUEUE_ID, SOLOQ_QUEUE_ID, NORMAL_BLIND_QUEUE_ID, FLEX_QUEUE_ID]

DB_ITEMS = ['players', 'teams', 'competitions']
DB_CHANGE_TYPE = ['add', 'edit', 'remove']
