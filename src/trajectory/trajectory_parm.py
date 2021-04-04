from trajectory.trajectory_functions import onState_analysis, offState_analysis, localization_analysis
from fft.trajectory_fft import trajectory_fft
from trajectoryProcessingFunctions import *
import collections
import numpy as np

class trajectory_parm_maker():
    def __init__(self, trajectory_plane_dict, trajectory_pos_dict):
        self.trajectory_plane_dict = trajectory_plane_dict
        self.trajectory_pos_dict = trajectory_pos_dict

    def make_parm_array(self):
        parm_ls_ls = []
        pos_ls_dict = {}
        cnt = 1
        for trajectory_id in self.trajectory_plane_dict.keys():
            if cnt % 500 == 0:
                print(cnt)
            pos_ls = self.trajectory_pos_dict[trajectory_id]
            x_ls, y_ls = zip(*pos_ls)
            pos_ls_dict[trajectory_id] = list(x_ls) + list(y_ls)
            parm_ls = []
            first_frame, on_state_parm_dict, off_state_parm_dict = self.make_on_off_state_dict(trajectory_id)
            pos_parm_dict = self.make_localization_info_dict(trajectory_id)
            FFT_parm_dict = self.make_FFT_info_dict(trajectory_id)

            parm_ls.append(first_frame)
            parm_ls.append(len(self.trajectory_plane_dict[trajectory_id]))
            for k, v in on_state_parm_dict.items():
                parm_ls.append(v)
            for k, v in off_state_parm_dict.items():
                parm_ls.append(v)
            for k, v in pos_parm_dict.items():
                parm_ls.append(v)
            for k, v in FFT_parm_dict.items():
                parm_ls.append(v)
            parm_ls_ls.append(parm_ls)
            cnt += 1
        return np.array(parm_ls_ls), pos_ls_dict

    def make_parm_name_ls(self):
        parm_name_ls = ["first frame time", "number_of_events"]
        for trajectory_id in self.trajectory_plane_dict.keys():
            first_frame, on_state_parm_dict, off_state_parm_dict = self.make_on_off_state_dict(trajectory_id)
            pos_parm_dict = self.make_localization_info_dict(trajectory_id)
            FFT_parm_dict = self.make_FFT_info_dict(trajectory_id)
            for k, v in on_state_parm_dict.items():
                parm_name_ls.append("on_" + k)
            for k, v in off_state_parm_dict.items():
                parm_name_ls.append("off_" + k)
            for k, v in pos_parm_dict.items():
                parm_name_ls.append("pos_" + k)
            for k, v in FFT_parm_dict.items():
                parm_name_ls.append("fft_" + k)
            break
        return parm_name_ls

    def make_on_off_state_dict(self, key):
        trajectory = self.trajectory_plane_dict[key]

        cnt_ls = trajectory_processing_functions.findContinuityPlanes(trajectory)
        off_length_ls = trajectory_processing_functions.find_off_gap_length(cnt_ls)

        on_state_obj = onState_analysis(cnt_ls)
        off_state_obj = offState_analysis(off_length_ls)

        on_state_parm_dict = self.get_env_vars(on_state_obj)
        off_state_parm_dict = self.get_env_vars(off_state_obj)
        first_frame = cnt_ls[0]

        return first_frame, on_state_parm_dict, off_state_parm_dict

    def make_localization_info_dict(self, key):
        pos_ls = self.trajectory_pos_dict[key]
        pos_obj = localization_analysis(pos_ls)
        pos_parm_dict = self.get_env_vars(pos_obj)
        return pos_parm_dict

    def make_FFT_info_dict(self, key):
        FFT_ls = self.trajectory_plane_dict[key]
        FFT_obj = trajectory_fft(FFT_ls)
        FFT_parm_dict = self.get_env_vars(FFT_obj)
        return FFT_parm_dict

    def get_env_vars(self, cls):
        env_dict = collections.OrderedDict()
        # print(dir(cls))
        for name in dir(cls):
            attr = getattr(cls, name)
            # print(attr)
            if isinstance(attr, int):
                env_dict[name] = attr
            if isinstance(attr, float):
                env_dict[name] = attr
        return env_dict
