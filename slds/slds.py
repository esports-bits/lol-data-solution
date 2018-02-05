from riotwatcher import RiotWatcher
from converters.data2frames import game_to_dataframe as g2df


def main():
    rw = RiotWatcher(API_KEY)

    game = rw.match.by_id(match_id=3511957748, region="EUW1")

    c_names = ["Moryo", "RafaL0L", "Ripi", "Monk", "Tasteless", "Kektz", "Lamabear", "Pretty", "Sedrion", "Anthrax"]
    t_names = ["EMZ", "ASUS"]
    positions = ['TOP', 'JUNG', 'MID', 'ADC', 'SUPP', 'TOP', 'JUNG', 'MID', 'ADC', 'SUPP']

    g2df(game, custom_names=c_names, team_names=t_names, custom_positions=positions).T.drop_duplicates().T


if __name__ == '__main__':
    main()