import numpy as np

API_KEY = ""

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

CUSTOM_PARTICIPANT_COLS = ['p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'p_6', 'p_7', 'p_8', 'p_9', 'p_10']
STANDARD_POSITIONS = ['TOP', 'JUNG', 'MID', 'ADC', 'SUPP', 'TOP', 'JUNG', 'MID', 'ADC', 'SUPP']
SCRIMS_POSITIONS_COLS = ['pos_1', 'pos_2', 'pos_3', 'pos_4', 'pos_5', 'pos_6', 'pos_7', 'pos_8', 'pos_9', 'pos_10']
STATIC_DATA_RELEVANT_COLS = ['id', 'name']
CHAMP_COLS = ["championId"]
RUNES_COLS = ["perk0", "perk1", "perk2", "perk3", "perk4", "perk5", "perkPrimaryStyle", "perkSubStyle"]
ITEMS_COLS = ["item0", "item1", "item2", "item3", "item4", "item5", "item6"]
SUMMS_COLS = ['spell1Id', 'spell2Id']
BANS_COLS = ['ban1_team', 'ban2_team', 'ban3_team', 'ban4_team', 'ban5_team']

LEAGUES_DATA_DICT = {'LCK': {'matches_file_path': LCK_MATCHES_FILE_PATH,
                             'games_path': LCK_GAMES_DIR,
                             'official': True,
                             'dtypes': {},
                             'csv_path': LCK_DATASET_CSV,
                             'excel_path': LCK_DATASET_XLSX},
                     'SLO': {'matches_file_path': SLO_MATCHES_FILE_PATH,
                             'games_path': SLO_GAMES_DIR,
                             'official': False,
                             'dtypes': {'datetime': str, 'series_id': str, 'week': int, 'event': str, 'game': int,
                                        'game_id': np.int64, 'blue': str, 'red': str, 'blue_win': int, 'p_1': str,
                                        'p_2': str, 'p_3': str, 'p_4': str, 'p_5': str, 'p_6': str, 'p_7': str,
                                        'p_8': str, 'p_9': str, 'p_10': str},
                             'csv_path': SLO_DATASET_CSV,
                             'excel_path': SLO_DATASET_XLSX},
                     'SCRIMS': {'matches_file_path': SCRIMS_MATCHES_FILE_PATH,
                                'games_path': SCRIMS_GAMES_DIR,
                                'official': False,
                                'dtypes': {'date': str, 'enemy': str, 'game_id': np.int64, 'match_history': str,
                                           'blue': str, 'red': str,
                                           'pos_1': str, 'pos_2': str, 'pos_3': str, 'pos_4': str, 'pos_5': str,
                                           'pos_6': str, 'pos_7': str, 'pos_8': str, 'pos_9': str, 'pos_10': str,
                                           'p_1': str, 'p_2': str, 'p_3': str, 'p_4': str, 'p_5': str, 'p_6': str,
                                           'p_7': str, 'p_8': str, 'p_9': str, 'p_10': str},
                                'csv_path': SCRIMS_DATASET_CSV,
                                'excel_path': SCRIMS_DATASET_XLSX},
                     'SOLOQ': {'matches_file_path': None,
                               'games_path': SOLOQ_GAMES_DIR,
                               'official': False,
                               'dtypes': {},
                               'csv_path': SOLOQ_DATASET_CSV,
                               'excel_path': SOLOQ_DATASET_XLSX}
                     }
SUPPORTED_LEAGUES = list(LEAGUES_DATA_DICT.keys())