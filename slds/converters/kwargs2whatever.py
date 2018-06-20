def export_dataset_kwargs(df, kwargs):
    if 'custom_names' in kwargs:
        df['player_name'] = kwargs['custom_names']

    if 'team_names' in kwargs:
        df.loc[:4, 'team_name'] = kwargs['team_names'][0]
        df.loc[5:10, 'team_name'] = kwargs['team_names'][1]

    if 'custom_positions' in kwargs:
        df['position'] = kwargs['custom_positions']

    if 'week' in kwargs:
        df['week'] = kwargs['week']

    if 'enemy' in kwargs:
        df['enemy'] = kwargs['enemy']

    if 'game_n' in kwargs:
        df['game_n'] = kwargs['game_n']

    if 'blue_win' in kwargs:
        df['blue_win'] = kwargs['blue_win']

    return df
