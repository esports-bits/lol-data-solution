import os
import argparse
from connectors import filesystem, database
from config.constants import SUPPORTED_LEAGUES, SUPPORTED_CONNECTORS, SUPPORTED_TEAM_NAMES, SUPPORTED_TEAM_ABBVS


def parse_args():
    parser = argparse.ArgumentParser(description='LoL solution to generate datasets from leagues, scrims and solo Q LoL'
                                                 ' matches.')
    parser.add_argument('-L', '--league', help='Choose league. {}'.format(SUPPORTED_LEAGUES))
    parser.add_argument('-R', '--region', help='Choose region. [EUW1, NA, NA1...]')
    parser.add_argument('-e', '--export', help='Export dataset.', action='store_true')
    parser.add_argument('-d', '--download', help='Download new data if available.', action='store_true')
    parser.add_argument('-xlsx', help='Export dataset as XLSX.', action='store_true')
    parser.add_argument('-csv', help='Export dataset as CSV.', action='store_true')
    parser.add_argument('-usd', '--update_static_data', help='Update local files of static data.', action='store_true')
    parser.add_argument('-fu', '--force_update', help='Force the update of the exports datasets.', action='store_true')
    parser.add_argument('-ms', '--merge_soloq', help='Merge SoloQ dataset with info of players.', action='store_true')
    parser.add_argument('-ng', '--n_games', help='Set the number of games to download from Solo Q.')
    parser.add_argument('-C', '--connector', help='Selects between supported connectors such as '
                                                  'File System or Data Base. {}'.format(SUPPORTED_CONNECTORS))
    parser.add_argument('-bi', '--begin_index', help='Set the begin index of the Solo Q downloads.')
    parser.add_argument('-ta', '--team_abbv', help='Work with the data of one or more teams selected through his '
                                                   'abbreviation. Team abbreviations on DB: '
                                                   '{}'.format(SUPPORTED_TEAM_ABBVS))
    parser.add_argument('-tn', '--team_name', help='Work with the data of one or more teams selected through his '
                                                   'name. Team names on DB: '
                                                   '{}'.format(SUPPORTED_TEAM_ABBVS))
    return parser.parse_args()


def main():
    args = parse_args()
    league = args.league.upper()
    connector = args.connector.upper()
    if league not in SUPPORTED_LEAGUES:
        print('League {} is not currently supported. Check help for more information.'.format(args.league))
        return
    elif connector not in SUPPORTED_CONNECTORS:
        print('Connector {} is not currently supported. Check help for more information.'.format(args.league))
        return

    if connector == 'FS':
        filesystem.parse_args(args)
    elif connector == 'DB':
        database.parse_args(args)
    else:
        return


if __name__ == '__main__':
    main()
