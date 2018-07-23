import pickle
from itertools import chain
import pandas as pd
import datetime
from converters.kwargs2whatever import export_dataset_kwargs
from config.constants import STATIC_DATA_RELEVANT_COLS, STATIC_DATA_DIR, ITEMS_COLS, SUMMS_COLS, RUNES_COLS, BANS_COLS
from converters.data2files import read_json


def game_to_dataframe(match, timeline, **kwargs):
    def timestamp_to_readable_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return "{h}:{m}:{s}".format(h=int(h), m=int(m), s=int(s))

    def ids_to_names(df, database=None):
        # Champions
        if database is None:
            champs = champs_to_dataframe(read_json(save_dir=STATIC_DATA_DIR, file_name='champions'))
            items = items_to_dataframe(read_json(save_dir=STATIC_DATA_DIR, file_name='items'))
            summs = summs_to_dataframe(read_json(save_dir=STATIC_DATA_DIR, file_name='summoners'))
            runes = runes_reforged_to_dataframe()
        else:
            champs = champs_to_dataframe(database.find_one({'_id': 'champions'}, {'_id': 0}))
            items = items_to_dataframe(database.find_one({'_id': 'items'}, {'_id': 0}))
            summs = summs_to_dataframe(database.find_one({'_id': 'summoner_spells'}, {'_id': 0}))
            runes = runes_reforged_to_dataframe(data=database.find_one({'_id': 'runes_reforged'}, {'_id': 0})['runes'])
        df1 = df.merge(
            champs.rename(columns={'name': 'champ_name'}), left_on='championId', right_on='id').drop('id', axis=1)
        # Items
        df2 = df1
        for name in ITEMS_COLS:
            df2 = df2.merge(items.rename(columns={'name': '{}_name'.format(name)}), left_on='{}'.format(name),
                            right_on='id', how='left').drop('id', axis=1)
        # Summoner spells
        df3 = df2
        for name in SUMMS_COLS:
            df3 = df3.merge(summs.rename(columns={'name': '{}_name'.format(name)}), left_on='{}'.format(name),
                            right_on='id', how='left').drop('id', axis=1)
        # Runes
        df4 = df3
        try:
            for name in RUNES_COLS:
                df4 = df4.merge(runes.rename(columns={'name': '{}_name'.format(name)}), left_on='{}'.format(name),
                                right_on='id', how='left').drop('id', axis=1)
        except KeyError:
            pass
        # Bans
        df5 = df4
        for name in BANS_COLS:
            df5 = df5.merge(champs.rename(columns={'name': '{}_name'.format(name)}), left_on='{}'.format(name),
                            right_on='id', how='left').drop('id', axis=1)

        return df5

    # def calculate_diffs(df):
    participants = match.pop('participants')
    participant_ids = match.pop('participantIdentities')
    teams = match.pop('teams')
    m_df = pd.DataFrame(match, index=range(0, 10))
    ps_ids_df = game_participant_ids_to_dataframe(participant_ids, custom=kwargs['custom'])
    ps_df = game_participants_to_dataframe(participants)
    t_df = game_teams_to_dataframe(teams)
    tl_df = timeline_relevant_stats_to_dataframe(timeline)

    df_concat = pd.concat([m_df, ps_ids_df, ps_df, t_df, tl_df], axis=1)

    if kwargs:
        df_result = export_dataset_kwargs(df_concat, kwargs)
    else:
        df_result = df_concat

    df_result.gameCreation = df_result.gameCreation.apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1e3).strftime('%Y-%m-%d %H:%M:%S'))
    df_result['game_duration_time'] = df_result.gameDuration.apply(timestamp_to_readable_time)
    if 'database' in kwargs:
        df_result2 = ids_to_names(df_result, database=kwargs['database'])
    else:
        df_result2 = ids_to_names(df_result)
    return df_result2.T.reset_index().drop_duplicates(subset='index', keep='first').set_index('index').T


def game_participants_to_dataframe(participants):
    stats = [p.pop('stats') for p in participants]
    timeline = [p.pop('timeline') for p in participants]

    # Old matches
    for p in participants:
        try:
            _ = p.pop('masteries')
        except KeyError:
            pass
        try:
            _ = p.pop('runes')
        except KeyError:
            pass

    df1 = pd.concat([pd.DataFrame(p, index=(i,)) for i, p in enumerate(participants)])
    df2 = pd.concat([pd.DataFrame(s, index=(i,)) for i, s in enumerate(stats)])
    df3 = pd.concat([game_timeline_to_dataframe(t) for i, t in enumerate(timeline)])
    return pd.concat([df1, df2, df3], axis=1)


def game_participant_ids_to_dataframe(participant_ids, custom):
    if not custom:
        # Not good. Have to change it to support and adapt to further changes.
        try:
            return pd.concat([pd.DataFrame({'participantId': p['participantId'],
                                            'summonerName': p['player']['summonerName'],
                                            'accountId': p['player']['accountId'],
                                            'currentAccountId': p['player']['currentAccountId'],
                                            'summonerId': p['player']['summonerId']},
                                           index=(i,)) for i, p in enumerate(participant_ids)])
        except KeyError:
            pass
        try:
            return pd.concat([pd.DataFrame({'participantId': p['participantId'],
                                            'summonerName': p['player']['summonerName']},
                                           index=(i,)) for i, p in enumerate(participant_ids)])
        except KeyError:
            pass
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
    while len(t1bans) < 5:
        t1bans.append(0)
    while len(t2bans) < 5:
        t2bans.append(0)
    t1 = pd.DataFrame(teams[0], index=range(0, 5))
    t2 = pd.DataFrame(teams[1], index=range(5, 10))
    t1['ban1'], t1['ban2'], t1['ban3'], t1['ban4'], t1['ban5'] = t1bans
    t2['ban1'], t2['ban2'], t2['ban3'], t2['ban4'], t2['ban5'] = t2bans
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
    def timeto_stats_from_participant(p):
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
        f5 = p.loc[p.frame == 5]
        f10 = p.loc[p.frame == 10]
        f15 = p.loc[p.frame == 15]
        f20 = p.loc[p.frame == 20]
        g5 = list(f5.totalGold)
        g10 = list(f10.totalGold)
        g15 = list(f15.totalGold)
        g20 = list(f20.totalGold)
        ccs5 = list(f5.minionsKilled + f5.jungleMinionsKilled)
        ccs10 = list(f10.minionsKilled + f10.jungleMinionsKilled)
        ccs15 = list(f15.minionsKilled + f15.jungleMinionsKilled)
        ccs20 = list(f20.minionsKilled + f20.jungleMinionsKilled)
        return {'tt4kgold': l4k[0] if l4k else None, 'tt7kgold': l7k[0] if l7k else None,
                'tt50cs': l50cs[0] if l50cs else None, 'tt100cs': l100cs[0] if l100cs else None,
                'tt50jcs': l50jcs[0] if l50jcs else None, 'tt100jcs': l100jcs[0] if l100jcs else None,
                'tt50ccs': l50ccs[0] if l50ccs else None, 'tt100ccs': l100ccs[0] if l100ccs else None,
                'ttlvl6': l6lvl[0] if l6lvl else None, 'ttlvl11': l11lvl[0] if l11lvl else None,
                'gold_at_5': g5[0] if g5 else None, 'gold_at_10': g10[0] if g10 else None,
                'gold_at_15': g15[0] if g15 else None, 'gold_at_20': g20[0] if g20 else None,
                'ccs_at_5': ccs5[0] if ccs5 else None, 'ccs_at_10': ccs10[0] if ccs10 else None,
                'ccs_at_15': ccs15[0] if ccs15 else None, 'ccs_at_20': ccs20[0] if ccs20 else None}

    def get_wards_placed_killed(tl):
        events = list(chain.from_iterable([f['events'] for f in tl['frames']]))
        ward_cols = ['yellow_trinkets', 'control_wards', 'undefined', 'sight_wards', 'blue_trinkets']
        placed_cols = [col + '_placed' for col in ward_cols]
        killed_cols = [col + '_killed' for col in ward_cols]

        placed_ward_events = [event for event in events if event['type'] == 'WARD_PLACED']
        killed_ward_events = [event for event in events if event['type'] == 'WARD_KILL']

        if placed_ward_events:
            df_placed = pd.DataFrame(
                [(event['creatorId'], event['wardType'], event['timestamp']) for event in placed_ward_events]).groupby(
                [0, 1], as_index=False).count()
            df_placed.rename(columns={0: 'participant_id', 1: 'ward_type', 2: 'count'}, inplace=True)
            df_placed.set_index('participant_id', inplace=True)
            yt_p, cw_p, un_p, sw_p, bt_p = df_placed.loc[df_placed['ward_type'] == 'YELLOW_TRINKET'], df_placed.loc[
                df_placed['ward_type'] == 'CONTROL_WARD'], df_placed.loc[df_placed['ward_type'] == 'UNDEFINED'], \
                df_placed.loc[df_placed['ward_type'] == 'SIGHT_WARD'], \
                df_placed.loc[df_placed['ward_type'] == 'BLUE_TRINKET']
            df1 = pd.concat([yt_p, cw_p, un_p, sw_p, bt_p], axis=1).drop('ward_type', axis=1)
            df1.columns = placed_cols
            df1.reset_index(inplace=True)
            df1 = df1.loc[df1.participant_id != 0]
            df1.participant_id = df1.participant_id - 1
            df1.set_index('participant_id', inplace=True)

        if killed_ward_events:
            df_killed = pd.DataFrame(
                [(event['killerId'], event['wardType'], event['timestamp']) for event in killed_ward_events]).groupby(
                [0, 1], as_index=False).count()
            df_killed.rename(columns={0: 'participant_id', 1: 'ward_type', 2: 'count'}, inplace=True)
            df_killed.set_index('participant_id', inplace=True)
            yt_k, cw_k, un_k, sw_k, bt_k = df_killed.loc[df_killed['ward_type'] == 'YELLOW_TRINKET'], df_killed.loc[
                df_killed['ward_type'] == 'CONTROL_WARD'], df_killed.loc[df_killed['ward_type'] == 'UNDEFINED'],\
                df_killed.loc[df_killed['ward_type'] == 'SIGHT_WARD'], \
                df_killed.loc[df_killed['ward_type'] == 'BLUE_TRINKET']
            df2 = pd.concat([yt_k, cw_k, un_k, sw_k, bt_k], axis=1).drop('ward_type', axis=1)
            df2.columns = killed_cols
            df2.reset_index(inplace=True)
            df2 = df2.loc[df2.participant_id != 0]
            df2.participant_id = df2.participant_id - 1
            df2.set_index('participant_id', inplace=True)

        if placed_ward_events and killed_ward_events:
            return pd.concat([df1, df2], axis=1).fillna(0).astype(int)
        elif placed_ward_events:
            return df1
        elif killed_ward_events:
            return df2
        else:
            return pd.DataFrame()

    stats = timeline_participant_stats_to_dataframe(timeline)
    ps = [stats.loc[stats.participantId == p_id] for p_id in range(1, 11)]
    df_result = pd.concat([pd.DataFrame(timeto_stats_from_participant(p), index=(i,)) for i, p in enumerate(ps)])
    wards = get_wards_placed_killed(timeline)
    return pd.concat([df_result, wards], axis=1)


def runes_reforged_to_dataframe(data=None):
    if data:
        runes = data
    else:
        runes = read_json(save_dir=STATIC_DATA_DIR, file_name='runes_reforged')
    runes1 = pd.DataFrame(runes)[STATIC_DATA_RELEVANT_COLS]
    slots = [path['slots'] for path in runes]
    runes2 = pd.concat(
        [pd.DataFrame(slot[i]['runes'])[STATIC_DATA_RELEVANT_COLS] for slot in slots for i in range(0, len(slot))])
    return pd.concat([runes1, runes2]).reset_index(drop=True)


def items_to_dataframe(items):
    return pd.DataFrame(items['data']).T.reset_index(drop=True)[STATIC_DATA_RELEVANT_COLS]


def champs_to_dataframe(champs):
    return pd.DataFrame(champs['data']).T.reset_index(drop=True)[STATIC_DATA_RELEVANT_COLS]


def summs_to_dataframe(summs):
    return pd.DataFrame(summs['data']).T.reset_index(drop=True)[STATIC_DATA_RELEVANT_COLS]


def get_soloq_dataframe(players_db):
    def transform_soloq_player_data_for_dataframe(player):
        player.pop('_id')
        comp_info = player.pop('comp_info')
        try:
            player['competition_abbv'] = comp_info[0]['key']
            player['competition_name'] = comp_info[0]['name']
        except IndexError:
            pass

        team_info = player.pop('team_info')
        try:
            player['team_abbv'] = team_info[0]['key']
            player['team_name'] = team_info[0]['name']
        except IndexError:
            pass

        return player

    cursor = players_db.aggregate([
        {'$lookup': {'from': 'teams', 'localField': 'team_abbv', 'foreignField': 'key', 'as': 'team_info'}},
        {'$lookup': {'from': 'competitions', 'localField': 'team_info.competition', 'foreignField': 'key',
                     'as': 'comp_info'}}
    ])
    return pd.concat([pd.DataFrame(p, index=(0,)) for p in
                      [transform_soloq_player_data_for_dataframe(player) for player in cursor]]).rename(
        columns={'key': 'player_name'})


# def get_slo_dataframe(slo_db):
#
