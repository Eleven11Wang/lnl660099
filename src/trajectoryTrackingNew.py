from src.readLocalizationText import dataPoints

class dataTrajectory(dataPoints):
    def __init__(self, name):
        dataPoints.__init__(self, name)
        self.traceDict = {}
        self.lastPositionLs = []
        self.nextIdx = 0
        self.trajectory_distance=40
        print("lens pf planeDict")
        print(len(self.planeDict))
        self.first_key = min(self.planeDict.keys())


    def isSameSource(self, loc1, loc2):
        dis = (loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2
        if dis < self.trajectory_distance * self.trajectory_distance:
            return True
        else:
            return False

    def init_Trace(self):

        initPosInfo = self.planeDict[self.first_key]
        for initInfo in initPosInfo[1:]:
            pos, intensity = initInfo
            self.lastPositionLs.append(pos)
            self.traceDict[self.nextIdx] = []
            self.traceDict[self.nextIdx].append(((1, pos, intensity)))
            self.nextIdx += 1

        # print(self.lastPositionLs)




    def find_Trace(self):
        trajectory_idx=1
        last_pos_ls=[]
        initPosInfo = self.planeDict[self.first_key]
        for initInfo in initPosInfo:
            pos, intensity = initInfo
            self.traceDict[trajectory_idx] = []
            self.traceDict[trajectory_idx].append((1, pos, intensity))
            last_pos_ls.append((trajectory_idx, 1, pos))
            trajectory_idx += 1

        for plane, posInfoLs in self.planeDict.items():
            if plane ==1:
                continue
            if plane % 5000 == 0:
                print(str(plane) + "/" + str(self.planes))
            for i,posInfo in enumerate(posInfoLs):


                (pos, intensity) = posInfo
                append_ls=[]
                match =0
                for idx,info in enumerate(last_pos_ls):
                    trajectory_idx_last,last_plane,last_pos=info
                    if plane-last_plane > 50:
                        last_pos_ls.pop(idx)
                        continue

                    if self.isSameSource(last_pos, pos):
                        match =1
                        self.traceDict[trajectory_idx_last].append((plane, pos, intensity))
                        last_pos_ls[idx] = (trajectory_idx_last,plane,pos)
                        break

                if match ==0 :
                    self.traceDict[trajectory_idx]=[]
                    self.traceDict[trajectory_idx].append((plane,pos,intensity))
                    append_ls.append((trajectory_idx,plane,pos))
                    trajectory_idx+=1

                last_pos_ls.extend(append_ls)
        print(trajectory_idx)

