import numpy as np

API_KEY = ""

WORK_DIR = '../'
SLO_DATA_DIR = WORK_DIR + 'slo_data/'
SLO_GAMES_DIR = WORK_DIR + 'slo_games/'
SLO_DATASETS_DIR = WORK_DIR + 'slo_datasets/'
STATIC_DATA_DIR = WORK_DIR + 'static_data/'
SLO_MATCHES_FILE_PATH = SLO_DATA_DIR + 'partidas_split_1.csv'
SLO_DATASET_CSV = SLO_DATASETS_DIR + 'dataset_test.csv'
SLO_DATASET_XLSX = SLO_DATASETS_DIR + 'dataset_test.xlsx'

DATA_DRAGON_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/{endpoint}'
DD_LANGUAGE = 'en_US'
DD_RUNES_REFORGED = 'runesReforged.json'

SLO_DATA_DTYPES = {'datetime': str, 'series_id': str, 'week': int, 'event': str, 'game': int,
                   'game_id': np.int64, 'blue': str, 'red': str, 'blue_win': int, 'p_1': str, 'p_2': str,
                   'p_3': str, 'p_4': str, 'p_5': str, 'p_6': str, 'p_7': str, 'p_8': str, 'p_9': str,
                   'p_10': str}

SLO_MATCHES_DATA_P_COLS = ['p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'p_6', 'p_7', 'p_8', 'p_9', 'p_10']
SLO_CUSTOM_POSITIONS = ['TOP', 'JUNG', 'MID', 'ADC', 'SUPP', 'TOP', 'JUNG', 'MID', 'ADC', 'SUPP']
STATIC_DATA_RELEVANT_COLS = ['id', 'name']
CHAMP_COLS = ["championId"]
RUNES_COLS = ["perk0", "perk1", "perk2", "perk3", "perk4", "perk5", "perkPrimaryStyle", "perkSubStyle"]
ITEMS_COLS = ["item0", "item1", "item2", "item3", "item4", "item5", "item6"]
SUMMS_COLS = ['spell1Id', 'spell2Id']
BANS_COLS = ['ban1_team', 'ban2_team', 'ban3_team', 'ban4_team', 'ban5_team']
