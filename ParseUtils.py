def get_team_time_up_windows(score_timeline, at_home):
    team_a_score_idx = 1 if at_home else 0
    team_b_score_idx = 0 if at_home else 1
    time_up = []
    idx = -1
    w_start, w_end = None, None
    for period in score_timeline:
        time_up.append([])
        idx += 1
        for record in period:
            scores = record[1].split("-")
            if int(scores[team_a_score_idx]) > int(scores[team_b_score_idx]):
                if w_start is None:
                    w_start = record[0]
                w_end = None
            else:
                if w_end is None:
                    w_end = record[0]
                if w_start is not None:
                    time_up[idx].append((w_start, w_end))
                w_start = None
        #case when team finishes the quarter/period, and they are up
        if w_start is not None:
            time_up[idx].append((w_start, "0:00.0"))
            w_start = None
    return time_up

def get_player_time_on_windows(player_timeline):
    time_on = []
    idx = -1
    w_start, w_end = None, None
    for period in player_timeline:
        time_on.append([])
        idx += 1
        for record in period:
            if record[1] == "PRESENT":
                w_start = "12:00.0"
            elif record[1] == "SUB-OUT":
                w_end = record[0]
                time_on[idx].append((w_start, w_end))
                w_start = None
            elif record[1] == "SUB-IN":
                w_start = record[0]
        #case when player finishes the quarter/period and is still on
        if w_start is not None:
            time_on[idx].append((w_start, "0:00.0"))
    return time_on

def _get_player_time_up(team_time_up, player_time_on):
    def window_intersects(w1_, w2_):
        #get length of window in seconds
        def time_diff(t1, t2):
            t1_min, t1_sec = t1.split(":")
            t2_min, t2_sec = t2.split(":")
            t1_min, t1_sec, t2_min, t2_sec = int(t1_min), float(t1_sec), int(t2_min), float(t2_sec)
            t1_total_sec = t1_min*60 + t1_sec
            t2_total_sec = t2_min*60 + t2_sec
            return t1_total_sec - t2_total_sec
        #convert to float for comparison
        w1 = [float(x.replace('.','').replace(':','.')) for x in w1_]
        w2 = [float(x.replace('.','').replace(':','.')) for x in w2_]
        #window2 starts in-between or at same time as window1
        if w1[0] >= w2[0] and w1[1] < w2[0]:
            return time_diff(w2_[0], w1_[1] if w1[1] >= w2[1] else w2_[1])
        #window1 starts in-between window 2
        elif w1[0] <= w2[0] and w1[0] >= w2[1]:
            return time_diff(w1_[0], w1_[1] if w1[1] >= w2[1] else w2_[1])
        else:
            return 0

    time_up = 0
    for idx, period in enumerate(player_time_on):
        for p_wdow in period:
            for ttu_wdow in team_time_up[idx]:
                intersect = window_intersects(p_wdow, ttu_wdow)
                time_up += intersect
    return time_up

def get_player_time_up(score_timeline, player_timeline, at_home):
    ttu = get_team_time_up_windows(score_timeline, at_home)
    pto = get_player_time_on_windows(player_timeline)
    return _get_player_time_up(ttu, pto)




