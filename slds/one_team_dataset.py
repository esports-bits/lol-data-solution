import pandas as pd
import argparse
from config.constants import SUPPORTED_TEAM_ABBVS, LEAGUES_DATA_DICT, SOLOQ, CSV_EXPORT_PATH_MERGED


def parse_args():
    parser = argparse.ArgumentParser(description='LoL solution to generate datasets from leagues, scrims and solo Q LoL'
                                                 ' matches.')
    parser.add_argument('-a', '--abbreviation', help='Set the abreviation name of the desired teams. If more than one '
                                                     'split them using a comma like in the following example: '
                                                     'EDG,TSM,G2. Teams currently in DB: {}'
                        .format(SUPPORTED_TEAM_ABBVS))
    return parser.parse_args()


def main():
    args = parse_args()
    abbvs = [abbv.upper() for abbv in args.abbreviation.split(',')]
    if len(abbvs) == 1:
        abbv = abbvs[0]
        if abbv in SUPPORTED_TEAM_ABBVS:
            df = pd.read_csv(LEAGUES_DATA_DICT[SOLOQ][CSV_EXPORT_PATH_MERGED], index_col=0, encoding='ISO-8859-1')
            df.loc[df.team_abbv == abbv].to_excel('{}_soloq.xlsx'.format(abbv.lower()))
    elif len(abbvs) > 1:
        f_name = ''
        for abbv in abbvs:
            f_name = f_name + abbv.lower() + '_'
        df = pd.read_csv(LEAGUES_DATA_DICT[SOLOQ][CSV_EXPORT_PATH_MERGED], index_col=0, encoding='ISO-8859-1')
        df.loc[df.team_abbv.isin(abbvs)].to_excel('{}soloq.xlsx'.format(f_name))
    else:
        print('Team abbreviation not in the data base. Check help (-h, --help) for more information.')


if __name__ == '__main__':
    main()
