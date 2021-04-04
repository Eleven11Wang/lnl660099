
import math
import numpy as np

class basic_math:
    # 求极差
    @staticmethod
    def range(l):
        return max(l) - min(l);

    # 求平均数
    @staticmethod
    def avg(l):
        return float(sum(l)) / len(l);

    # 求中位数
    @staticmethod
    def median(l):
        l = sorted(l);  # 先排序
        if len(l) % 2 == 1:
            return l[len(l) // 2];
        else:
            return (l[len(l) // 2 - 1] + l[len(l) // 2]) / 2.0;

    # 求众数
    @staticmethod
    def mode(l):
        # 统计list中各个数值出现的次数
        count_dict = {};
        for i in l:
            if i in count_dict:
                count_dict[i] += 1;
            else:
                count_dict[i] = 1;
        # 求出现次数的最大值
        max_appear = 0
        for v in count_dict.values():
            if v > max_appear:
                max_appear = v;

        for k, v in count_dict.items():
            if v == max_appear:
                return k
        return 0

    # 求方差
    @staticmethod
    def variance(l):  # 平方的期望-期望的平方
        s1 = 0;
        s2 = 0;
        for i in l:
            s1 += i ** 2;
            s2 += i;
        return float(s1) / len(l) - (float(s2) / len(l)) ** 2;

    # 求方差2
    @staticmethod
    def variance2(l):  # 平方-期望的平方的期望
        ex = float(sum(l)) / len(l);
        s = 0;
        for i in l:
            s += (i - ex) ** 2;
        return float(s) / len(l);




class duration_analysis():
    def __init__(self, duration_ls):

        self.duration_ls = duration_ls
        if not duration_ls:
            self.number_of_event = 0
            self.max_length_of_duration = 0
            self.average_length_of_event = 0
            self.variance_of_length_of_events = 0
            self.mode_of_length_of_events = 0
            self.median_of_length_of_events = 0
            self.range_of_length_of_events = 0
        else:
            self.number_of_event = len(duration_ls)
            self.max_length_of_duration = max(duration_ls)
            self.average_length_of_event = basic_math.avg(duration_ls)
            self.variance_of_length_of_events = basic_math.variance2(duration_ls)
            self.mode_of_length_of_events = basic_math.mode(duration_ls)
            self.median_of_length_of_events = basic_math.median(duration_ls)
            self.range_of_length_of_events = basic_math.range(duration_ls)


class localization_analysis():
    def __init__(self,position_ls):
        self.position_ls = position_ls
        locx_ls ,locy_ls = zip(*position_ls)
        self.locx_ls = locx_ls
        self.locy_ls = locy_ls
        self.norm1_distance = abs(max(locx_ls)-min(locx_ls)) + abs(max(locy_ls)-min(locy_ls))
        self.norm2_distance = ((max(locx_ls)-min(locx_ls))**2+  (max(locy_ls)-min(locy_ls))**2) **0.5
        self.sample_mean_x = np.mean(locx_ls)
        self.sample_mean_y = np.mean(locy_ls)
        self.sample_stdev_x = np.var(locx_ls) ** 0.5
        self.sample_stdev_y = np.var(locy_ls) ** 0.5
        # Calculate standard error
        self.std_error_x = self.sample_stdev_x / (len(locx_ls)) ** 0.5
        self.std_error_y = self.sample_stdev_y / (len(locx_ls)) ** 0.5
