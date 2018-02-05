import pandas as pd


def game_to_dataframe(game, custom_names=None, team_names=None, custom_positions=None):
    ps_ids_df = game_participant_ids_to_dataframe(game['participantIdentities'])
    ps_df = game_participants_to_dataframe(game['participants'])
    df_result = pd.concat([ps_ids_df, ps_df], axis=1)

    if custom_names:
        df_result['player_name'] = custom_names

    if team_names:
        df_result.loc[:5, 'team_name'] = team_names[0]
        df_result.loc[5:10, 'team_name'] = team_names[1]

    if custom_positions:
        df_result['position'] = custom_positions

    return df_result


def game_participants_to_dataframe(participants):
    stats = [p['stats'] for p in participants]
    timeline = [p['timeline'] for p in participants]
    [p.pop('stats') for p in participants]  # remove stats
    [p.pop('timeline') for p in participants]  # remove timeline
    df1 = pd.concat([pd.DataFrame(p, index=(i,)) for i, p in enumerate(participants)])
    df2 = pd.concat([pd.DataFrame(s, index=(i,)) for i, s in enumerate(stats)])
    df3 = pd.concat([game_timeline_to_dataframe(t) for i, t in enumerate(timeline)])
    return pd.concat([df1, df2, df3], axis=1)


def game_participant_ids_to_dataframe(participant_ids):
    return pd.concat([pd.DataFrame(p_id, index=(i,)) for i, p_id in enumerate(participant_ids)])


def game_timeline_to_dataframe(timeline):
    columns = ["lane", "role", "participantId", "cspm0_10", "cspm10_20", "cspm20_30", "cspm30_end",
               "csdiffpm0_10", "csdiffpm10_20", "csdiffpm20_30", "csdiffpm30_end", "dmgtpm0_10",
               "dmgtpm10_20", "dmgtpm20_30", "dmgtpm30_end", "dmgtdiffpm0_10", "dmgtdiffpm10_20",
               "dmgtdiffpm20_30", "dmgtdiffpm30_end", "xppm0_10", "xppm10_20", "xppm20_30",
               "xppm30_end", "xpdiffpm0_10", "xpdiffpm10_20", "xpdiffpm20_30", "xpdiffpm30_end"]
    participant_id = timeline["participantId"]
    tl_df = pd.DataFrame(index=(participant_id - 1,), columns=columns)
    try:
        tl_df["cspm0_10"] = timeline["creepsPerMinDeltas"]["0-10"]
    except:
        tl_df["cspm0_10"] = None
    try:
        tl_df["cspm10_20"] = timeline["creepsPerMinDeltas"]["10-20"]
    except:
        tl_df["cspm10_20"] = None
    try:
        tl_df["cspm20_30"] = timeline["creepsPerMinDeltas"]["20-30"]
    except:
        tl_df["cspm20_30"] = None
    try:
        tl_df["cspm30_end"] = timeline["creepsPerMinDeltas"]["30-end"]
    except:
        tl_df["cspm30_end"] = None
    try:
        tl_df["csdiffpm0_10"] = timeline["csDiffPerMinDeltas"]["0-10"]
    except:
        tl_df["csdiffpm0_10"] = None
    try:
        tl_df["csdiffpm10_20"] = timeline["csDiffPerMinDeltas"]["10-20"]
    except:
        tl_df["csdiffpm10_20"] = None
    try:
        tl_df["csdiffpm20_30"] = timeline["csDiffPerMinDeltas"]["20-30"]
    except:
        tl_df["csdiffpm20_30"] = None
    try:
        tl_df["csdiffpm30_end"] = timeline["csDiffPerMinDeltas"]["30-end"]
    except:
        tl_df["csdiffpm30_end"] = None
    try:
        tl_df["dmgtpm0_10"] = timeline["damageTakenPerMinDeltas"]["0-10"]
    except:
        tl_df["dmgtpm0_10"] = None
    try:
        tl_df["dmgtpm10_20"] = timeline["damageTakenPerMinDeltas"]["10-20"]
    except:
        tl_df["dmgtpm10_20"] = None
    try:
        tl_df["dmgtpm20_30"] = timeline["damageTakenPerMinDeltas"]["20-30"]
    except:
        tl_df["dmgtpm20_30"] = None
    try:
        tl_df["dmgtpm30_end"] = timeline["damageTakenPerMinDeltas"]["30-end"]
    except:
        tl_df["dmgtpm30_end"] = None
    try:
        tl_df["dmgtdiffpm0_10"] = timeline["damageTakenDiffPerMinDeltas"]["0-10"]
    except:
        tl_df["dmgtdiffpm0_10"] = None
    try:
        tl_df["dmgtdiffpm10_20"] = timeline["damageTakenDiffPerMinDeltas"]["10-20"]
    except:
        tl_df["dmgtdiffpm10_20"] = None
    try:
        tl_df["dmgtdiffpm20_30"] = timeline["damageTakenDiffPerMinDeltas"]["20-30"]
    except:
        tl_df["dmgtdiffpm20_30"] = None
    try:
        tl_df["dmgtdiffpm30_end"] = timeline["damageTakenDiffPerMinDeltas"]["30-end"]
    except:
        tl_df["dmgtdiffpm30_end"] = None
    try:
        tl_df["gpm0_10"] = timeline["goldPerMinDeltas"]["0-10"]
    except:
        tl_df["gpm0_10"] = None
    try:
        tl_df["gpm10_20"] = timeline["goldPerMinDeltas"]["10-20"]
    except:
        tl_df["gpm10_20"] = None
    try:
        tl_df["gpm20_30"] = timeline["goldPerMinDeltas"]["20-30"]
    except:
        tl_df["gpm20_30"] = None
    try:
        tl_df["gpm30_end"] = timeline["goldPerMinDeltas"]["30-end"]
    except:
        tl_df["gpm30_end"] = None
    try:
        tl_df["xppm0_10"] = timeline["xpPerMinDeltas"]["0-10"]
    except:
        tl_df["xppm0_10"] = None
    try:
        tl_df["xppm10_20"] = timeline["xpPerMinDeltas"]["10-20"]
    except:
        tl_df["xppm10_20"] = None
    try:
        tl_df["xppm20_30"] = timeline["xpPerMinDeltas"]["20-30"]
    except:
        tl_df["xppm20_30"] = None
    try:
        tl_df["xppm30_end"] = timeline["xpPerMinDeltas"]["30-end"]
    except:
        tl_df["xppm30_end"] = None
    try:
        tl_df["xpdiffpm0_10"] = timeline["xpDiffPerMinDeltas"]["0-10"]
    except:
        tl_df["xpdiffpm0_10"] = None
    try:
        tl_df["xpdiffpm10_20"] = timeline["xpDiffPerMinDeltas"]["10-20"]
    except:
        tl_df["xpdiffpm10_20"] = None
    try:
        tl_df["xpdiffpm20_30"] = timeline["xpDiffPerMinDeltas"]["20-30"]
    except:
        tl_df["xpdiffpm20_30"] = None
    try:
        tl_df["xpdiffpm30_end"] = timeline["xpDiffPerMinDeltas"]["30-end"]
    except:
        tl_df["xpdiffpm30_end"] = None
    tl_df["lane"] = timeline["lane"]
    tl_df["role"] = timeline["role"]
    tl_df["participantId"] = participant_id

    return tl_df