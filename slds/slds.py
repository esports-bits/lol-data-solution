import os
import argparse
from connectors import filesystem, database
from config.constants import SUPPORTED_LEAGUES, SUPPORTED_CONNECTORS, REGIONS


def parse_args():
    parser = argparse.ArgumentParser(description='LoL solution to generate datasets from leagues, scrims and solo Q LoL'
                                                 ' matches.')
    parser.add_argument('-l', '--league', help='Choose league. {}'.format(SUPPORTED_LEAGUES))
    parser.add_argument('-r', '--region', help='Choose region. {}'.format(REGIONS.keys()))
    subparsers = parser.add_subparsers(dest='connector')

    # Subparsers
    parser_filesystem = subparsers.add_parser('fs', help='File system related commands.')
    parser_databases = subparsers.add_parser('db', help='Data bases system related commands.')

    # FS commands parser
    parser_filesystem.add_argument('-e', '--export', help='Export dataset.', action='store_true')
    parser_filesystem.add_argument('-d', '--download', help='Download new data if available.', action='store_true')
    parser_filesystem.add_argument('-usd', '--update_static_data', help='Update static data information.',
                                   action='store_true')
    parser_filesystem.add_argument('-ng', '--n_games', help='Set the number of games to download from Solo Q.',
                                   type=int)
    parser_filesystem.add_argument('-bi', '--begin_index', help='Set the begin index of the Solo Q downloads.',
                                   type=int)
    parser_filesystem.add_argument('-xlsx', help='Export dataset as XLSX.', action='store_true')
    parser_filesystem.add_argument('-csv', help='Export dataset as CSV.', action='store_true')
    parser_filesystem.add_argument('-fu', '--force_update', help='Force the update of the exports datasets.',
                                   action='store_true')
    parser_filesystem.add_argument('-ms', '--merge_soloq', help='Merge SoloQ dataset with info of players.',
                                   action='store_true')

    # DB commands parser
    parser_databases.add_argument('-d', '--download', help='Download new data if available.', action='store_true')
    parser_databases.add_argument('-e', '--export', help='Export dataset.', action='store_true')
    parser_databases.add_argument('-usd', '--update_static_data', help='Update static data information.',
                                  action='store_true')
    parser_databases.add_argument('-ng', '--n_games', help='Set the number of games to download from Solo Q.', type=int)
    parser_databases.add_argument('-bi', '--begin_index', help='Set the begin index of the Solo Q downloads.', type=int)
    parser_databases.add_argument('-ta', '--team_abbv', help='Work with the data of one or more teams selected through '
                                                             'his abbreviation.')
    parser_databases.add_argument('-tn', '--team_name', help='Work with the data of one or more teams selected through '
                                                             'his name.')

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        if not args.region:
            print('No region selected. Please, use -r or --region and select a region to work on from the following '
                  'list: {}'.format(REGIONS.keys()))
            return
        elif args.region.upper() not in REGIONS.keys():
            print('Region {} not supported. Try one of these: {}'.format(args.region.upper(), REGIONS.keys()))
            return
    except AttributeError:
        print('Please, use -r or --region and select a region to work on from the following list: {}'
              .format(REGIONS.keys()))
        return

    if not args.league:
        print('No league selected. Please, use -l or --league and select a league to work on from the following list: '
              '{}'.format(SUPPORTED_LEAGUES))
        return
    elif args.league.upper() not in SUPPORTED_LEAGUES:
        print('League {} not supported. Please, use -l or --league and select a league to work on from the following '
              'list: {}'.format(args.league.upper(), SUPPORTED_LEAGUES))

    if not args.connector:
        print('No connector selected. To select a connector write down one of the following names just after the '
              'script call with region and league parameters set: {}. Something like that: \"python program.py '
              '-r EUW -l SOLOQ {}\"'.format(SUPPORTED_CONNECTORS, SUPPORTED_CONNECTORS[0]))
        return
    elif args.connector.upper() == 'FS':
        filesystem.parse_args(args)
    elif args.connector.upper() == 'DB':
        database.parse_args(args)
    else:
        print('That connector is not supported.')
        return


if __name__ == '__main__':
    main()
