class trajectory_processing_functions:
    """

    function processing a single trajectory
    findContinuityPLanes : from framels to (start, duration) list, and return on state_len
    cnt_ls2_framels : from (start duration) list to frame_ls
    frame_ls2_stemls :from frame_ls to stem_ls (if blink 0, if not blink 1)
    link_frame_ls: link on state event in frame_ls(dealing fast blinking events)
    filter_continuity_planes: remove long stuck events in trajectory
    find_off_gap_length: find the length of gap
    """

    def __init__(self, trajectory):
        self.trajectory = trajectory

    @staticmethod
    def findContinuityPlanes(ls):
        """
        :param List [plane 1 ,plane 2,plane n]
        :return:[plane start,cnt,plane start,cnt]
        """
        ls = sorted(ls)
        dl = [ls[i] - ls[i - 1] for i in range(1, len(ls))]
        dl.append(-1)
        cntLs = []
        cnt = 0
        st = -1
        for idx, x in enumerate(dl):
            if cnt == 0:
                st = ls[idx]
                if x == 1:
                    cnt += 1

                else:
                    cntLs.extend([st, 1])
            else:
                if x == 1:
                    cnt += 1
                else:
                    cnt += 1
                    cntLs.extend([st, cnt])
                    cnt = 0
        return cntLs

    def cnt_ls2_framels(self, cntls):
        start_pos = cntls[::2]
        on_state_len = cntls[1::2]
        frame_ls = []

        for idx, start_pos in enumerate(start_pos):
            continueLens = on_state_len[idx]
            frame_ls.extend(list(range(start_pos, start_pos + continueLens, 1)))
        return frame_ls

    @staticmethod
    def frame_ls2_stemls(framels, last_pos=1024 - 1):
        if last_pos == -1:
            last_pos = framels[-1]
        data = [0] * (last_pos + 1)
        for x in framels:
            if x > last_pos:
                break
            data[x] = 1
        return data

    def link_frame_ls(cntLs, linklength):
        # 1 2 4 3 11 1 18 1
        stEvent = cntLs[::2]
        lastingLens = cntLs[1::2]
        edEvent = [stEvent[i] + lastingLens[i] - 1 for i in range(len(stEvent))]
        stp = stEvent[0]
        endp = edEvent[0]
        newCntLs = []
        for i in range(1, len(stEvent)):
            nextstp = stEvent[i]
            if nextstp - endp < linklength:
                endp = edEvent[i]

            else:
                newCntLs.extend([stp, endp - stp + 1])
                stp = stEvent[i]
                endp = edEvent[i]
        newCntLs.extend([stp, endp - stp + 1])
        return newCntLs

    def filterContinuityPlanes(cntLs, cutVal=100):
        eventLs = list(map(int, cntLs[::2]))
        cntLs = list(map(int, cntLs[1::2]))
        filtedLs = []
        for idx, event in enumerate(eventLs):
            cnt = cntLs[idx]
            if cnt > cutVal:
                pass
            else:
                filtedLs.append(event)
                filtedLs.append(cnt)
        return filtedLs

    @staticmethod
    def find_off_gap_length(ls):
        """
        todo cheak thsi function
        :param ls: [st_pos,len]
        :return: [t_oof_1,t_off_2]
        2,3,7,4->2,3,4,_5_,_6_,7,8,9,10-> gap len=2 2+3=5 7-5=2
        """
        off_state_len = []
        st = 0
        while st < len(ls) - 2:
            st_pos = ls[st]
            duration = ls[st + 1]
            next_pos = ls[st + 2]
            off_len = next_pos - st_pos - duration
            off_state_len.append(off_len)
            st += 2

        return off_state_len
