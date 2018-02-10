from riotwatcher import RiotWatcher
from converters.data2frames import game_to_dataframe as g2df
from converters.data2files import write_json, read_json
from config.constants import SLO_MATCHES_FILE_PATH, SLO_DATA_DTYPES, SLO_MATCHES_DATA_P_COLS, SLO_CUSTOM_POSITIONS, \
    API_KEY, SLO_GAMES_DIR, SLO_DATASETS_DIR
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm
import os


class Slds:
    def __init__(self, region):
        self.rw = RiotWatcher(API_KEY)
        self.region = region

    def generate_dataset(self, read_dir):
        df = pd.read_csv(SLO_MATCHES_FILE_PATH, dtype=SLO_DATA_DTYPES)
        df_result = pd.concat([g2df(match=read_json(save_dir=read_dir,
                                                    file_name=self.__get_file_names_from_match_id(m_id=g[1]['game_id'],
                                                                                                  save_dir=read_dir)
                                                    ['match_filename']),
                                    custom_names=list(g[1][SLO_MATCHES_DATA_P_COLS].T),
                                    custom_positions=SLO_CUSTOM_POSITIONS,
                                    team_names=list(g[1][['blue', 'red']])) for g in df.iterrows()])
        return df_result.reset_index(drop=True)

    def download_games(self, ids, save_dir):
        file_names = os.listdir(save_dir)
        curr_ids = list(set([f.split('.')[0].split('_')[1] for f in file_names]))
        new_ids = list(set(map(int, ids)) - set(map(int, curr_ids)))
        if new_ids:
            for item in tqdm(new_ids, desc='Downloading games'):
                match = self.rw.match.by_id(match_id=item, region=self.region)
                timeline = self.rw.match.timeline_by_match(match_id=item, region=self.region)
                data = {'match': match, 'timeline': timeline}
                self.__save_match_raw_data(data=data, save_dir=save_dir)
        else:
            print('All games already downloaded.')

    @staticmethod
    def __save_match_raw_data(data, save_dir):
        if isinstance(data, dict):
            game_id = data['match']['gameId']
            game_creation = dt.strftime(dt.fromtimestamp(data['match']['gameCreation'] / 1e3), '%d-%m-%y')
            write_json(data['match'], save_dir=save_dir, file_name='{date}_{id}'.format(date=game_creation, id=game_id))
            write_json(data['timeline'], save_dir=save_dir, file_name='{date}_{id}_tl'
                       .format(date=game_creation, id=game_id))
        else:
            raise TypeError('Dict expected at data param. Should be passed as shown here: {"match": match_dict, '
                            '"timeline": timeline_dict}.')

    @staticmethod
    def get_slo_games_ids():
        df = pd.read_csv(SLO_MATCHES_FILE_PATH, dtype=SLO_DATA_DTYPES)
        return list(df.game_id)

    @staticmethod
    def __get_file_names_from_match_id(m_id, save_dir):
        file_names = os.listdir(save_dir)
        match_filename = [val for val in file_names if str(m_id) in val and 'tl' not in val][0]
        tl_filename = [val for val in file_names if str(m_id) in val and 'tl' in val][0]
        return {'match_filename': match_filename.split('.')[0], 'tl_filename': tl_filename.split('.')[0]}


def main():
    slds = Slds(region='EUW1')
    ids = slds.get_slo_games_ids()
    slds.download_games(ids=ids, save_dir=SLO_GAMES_DIR)
    df = slds.generate_dataset(read_dir=SLO_GAMES_DIR)
    df.to_excel('{}dataset_test.xlsx'.format(SLO_DATASETS_DIR))
    df.to_csv('{}dataset_test.csv'.format(SLO_DATASETS_DIR))


if __name__ == '__main__':
    main()
