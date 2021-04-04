
"""
* relation ship of first frame and
* on state :
    * percentage of on frame / all fame
    * mean length of on frame
    * number of on event
    * last frame - first frame


"""
from common.common_analysis import duration_analysis
from common.common_analysis import localization_analysis

class onState_analysis(duration_analysis):
    def __init__(self, cnt_ls):
        self.start_ls = cnt_ls[::2]
        super().__init__(cnt_ls[1::2])
        self.trajectory_duration = self.trajectory_durationf()
        self.duty_cycle_over1 = sum(self.duration_ls) / self.trajectory_duration
        #print("duty cycle over trajectory ", self.duty_cycle_over1)
        assert self.duty_cycle_over1 <= 1


    def trajectory_durationf(self):
        last_frame = self.start_ls[-1] + self.duration_ls[-1] - 1
        first_frame = self.start_ls[0] - self.duration_ls[0] - 1
        return  last_frame- first_frame + 1

class offState_analysis(duration_analysis):
    def __init__(self,gap_length_ls):
        super().__init__(gap_length_ls)


class position_analysis(localization_analysis):
    def __init__(self, postion_ls):
        self.position_ls = postion_ls
        super().__init__(postion_ls)

