import collections
import numpy as np
from trajectory.trajectoryProcessingFunctions import trajectory_processing_functions



class trajectory_processing_main_functions():

    def __init__(self, trajectory_dict):
        self.trajectory_dict = trajectory_dict
        self.trajectory_plane_dict= []
        self.trajectory_pos_dict =[]
        self.trajectory_dict2plane_and_pos_dict(trajectory_dict)

    def return_trajectory_plane_dict(self):
        return self.trajectory_plane_dict

    def return_trajectory_pos_dict(self):
        return self.trajectory_pos_dict


    def trajectory_dict2plane_and_pos_dict(self,data_dict,dump_length =0):
        # used
        trajectory_plane_dict = {}
        trajectory_pos_dict = {}
        for trajectory_idx, data_ls in data_dict.items():
            plane_ls = []
            pos_ls = []
            for info in data_ls:
                plane, pos, intensity = info
                plane_ls.append(plane)
                pos_ls.append(pos)
            # ! parm =2
            if len(plane_ls) <= dump_length:
                pass
            else:
                trajectory_plane_dict[trajectory_idx] = plane_ls
                trajectory_pos_dict[trajectory_idx] = pos_ls
        self.trajectory_plane_dict = trajectory_plane_dict
        self.trajectory_pos_dict = trajectory_pos_dict
