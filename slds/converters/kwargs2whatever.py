def slo_game_kwargs(df, kwargs):
    if 'custom_names' in kwargs:
        df['player_name'] = kwargs['custom_names']

    if 'team_names' in kwargs:
        df.loc[:5, 'team_name'] = kwargs['team_names'][0]
        df.loc[5:10, 'team_name'] = kwargs['team_names'][1]

    if 'custom_positions' in kwargs:
        df['position'] = kwargs['custom_positions']

    if 'week' in kwargs:
        df['week'] = kwargs['week']

    return df
