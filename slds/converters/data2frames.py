import pandas as pd
import datetime
from time import strftime


def game_to_dataframe(match, timeline, custom_names=None, team_names=None, custom_positions=None):
    def get_readable_timestamp(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return "{h}:{m}:{s}".format(h=int(h), m=int(m), s=int(s))

    participants = match.pop('participants')
    participant_ids = match.pop('participantIdentities')
    teams = match.pop('teams')
    m_df = pd.DataFrame(match, index=range(0, 10))
    ps_ids_df = game_participant_ids_to_dataframe(participant_ids)
    ps_df = game_participants_to_dataframe(participants)
    t_df = game_teams_to_dataframe(teams)
    tl_df = timeline_relevant_stats_to_dataframe(timeline)
    df_result = pd.concat([m_df, ps_ids_df, ps_df, t_df, tl_df], axis=1)
    df_result.to_csv('df_result.csv')

    if custom_names:
        df_result['player_name'] = custom_names

    if team_names:
        df_result.loc[:5, 'team_name'] = team_names[0]
        df_result.loc[5:10, 'team_name'] = team_names[1]

    if custom_positions:
        df_result['position'] = custom_positions

    df_result.gameCreation = df_result.gameCreation.apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1e3).strftime('%Y-%m-%d %H:%M:%S'))
    df_result.gameDuration = df_result.gameDuration.apply(get_readable_timestamp)
    return df_result


def game_participants_to_dataframe(participants):
    stats = [p.pop('stats') for p in participants]
    timeline = [p.pop('timeline') for p in participants]
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


def game_teams_to_dataframe(teams):
    t1bans = [i['championId'] for i in teams[0].pop('bans')]
    t2bans = [i['championId'] for i in teams[1].pop('bans')]
    t1 = pd.DataFrame(teams[0], index=range(0, 5))
    t2 = pd.DataFrame(teams[1], index=range(5, 10))
    t1['ban1'], t1['ban2'], t1['ban3'], t1['ban4'], t1['ban5'] = [t1bans for i in range(0, 5)]
    t2['ban1'], t2['ban2'], t2['ban3'], t2['ban4'], t2['ban5'] = [t2bans for i in range(0, 5)]
    t1.columns = [c + '_team' for c in t1.columns]
    t2.columns = [c + '_team' for c in t2.columns]
    return pd.concat([t1, t2])


def timeline_participant_stats_to_dataframe(timeline):
    tl_frames = timeline['frames']
    tl_participants = [frame['participantFrames'] for frame in tl_frames]
    tl_ps_df = pd.concat(
        [pd.DataFrame(stats, index=(i,)) for i, p in enumerate(tl_participants) for p_id, stats in p.items()])
    return tl_ps_df.reset_index().rename(columns={'index': 'frame'})


def timeline_relevant_stats_to_dataframe(timeline):
    def time_to_stats_from_participant(p):
        l4k = list(p.loc[p.totalGold >= 4000].head(1).frame)
        l7k = list(p.loc[p.totalGold >= 7000].head(1).frame)
        l50cs = list(p.loc[p.minionsKilled >= 50].head(1).frame)
        l100cs = list(p.loc[p.minionsKilled >= 100].head(1).frame)
        l50jcs = list(p.loc[p.jungleMinionsKilled >= 50].head(1).frame)
        l100jcs = list(p.loc[p.jungleMinionsKilled >= 100].head(1).frame)
        l50ccs = list(p.loc[p.minionsKilled + p.jungleMinionsKilled >= 50].head(1).frame)
        l100ccs = list(p.loc[p.minionsKilled + p.jungleMinionsKilled >= 100].head(1).frame)
        l6lvl = list(p.loc[p.level >= 6].head(1).frame)
        l11lvl = list(p.loc[p.level >= 11].head(1).frame)
        return {'tt4kgold': l4k[0] if l4k else None, 'tt7kgold': l7k[0] if l7k else None,
                'tt50cs': l50cs[0] if l50cs else None, 'tt100cs': l100cs[0] if l100cs else None,
                'tt50jcs': l50jcs[0] if l50jcs else None, 'tt100jcs': l100jcs[0] if l100jcs else None,
                'tt50ccs': l50ccs[0] if l50ccs else None, 'tt100ccs': l100ccs[0] if l100ccs else None,
                'ttlvl6': l6lvl[0] if l6lvl else None, 'ttlvl11': l11lvl[0] if l11lvl else None}

    stats = timeline_participant_stats_to_dataframe(timeline)
    ps = [stats.loc[stats.participantId == p_id] for p_id in range(1, 11)]
    return pd.concat([pd.DataFrame(time_to_stats_from_participant(p), index=(i,)) for i, p in enumerate(ps)])
