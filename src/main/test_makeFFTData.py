import main.test_makeBlinkingData as makeBlinkingData
from trajectory.trajectory_main import trajectory_processing_main_functions
from fft.trajectory_fft import trajectory_fft
import utils.utils as utils

def main():
    blinking_dict_data = makeBlinkingData.main()


    for name, trajectory_dict in blinking_dict_data.items():
        print(name)
        plane_ls_dict = {}
        fft_ls_dict = {}
        blinking_obj = trajectory_processing_main_functions(trajectory_dict)
        blinking_plane_dict = blinking_obj.return_trajectory_plane_dict()
        # blinking_pos_dict = blinking_obj.return_trajectory_pos_dict()

        for trajectory_idx, plane_ls in blinking_plane_dict.items():
            FFT_obj = trajectory_fft(plane_ls)
            fft_ls = FFT_obj.get_fft_ls()
            stem_ls = FFT_obj.get_stem_ls()
            plane_ls_dict[trajectory_idx] = stem_ls
            fft_ls_dict[trajectory_idx] = list(fft_ls)
        

        utils.write_dict(name+"_stem_dict",plane_ls_dict,"/Users/wangjiahui/wwk_apply/lnl660099/data/")
        utils.write_dict(name + "_fft_ls", fft_ls_dict, "/Users/wangjiahui/wwk_apply/lnl660099/data/")


import matplotlib.pyplot as plt

if __name__ == "__main__":
    main()


