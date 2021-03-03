import numpy as np
import src.utils as utils
import src.analysisAndVis as analysisAndVis
#from informationDict import info_dict
import scipy as sp
import scipy.optimize


def norm_trajectory_data(trajectory_plane_dict,trajectory_pos_dict,folder_name="./"):
    trajectory_len_ls=[]
    trajectory_event_count_ls=[]
    long_lasting_ls_length=[]
    long_lasting_ls_idx=[]
    normalized_trajectory_plane_dict={}
    for trajectory_id, plane_info in trajectory_plane_dict.items():
        duration = max(plane_info)-min(plane_info)+1
        trajectory_len_ls.append(duration)
        trajectory_event_count_ls.append(len(set(plane_info)))
        if len(set(plane_info)) > 0.5 * duration and duration > 50:
            long_lasting_ls_length.append(len(plane_info))
            long_lasting_ls_idx.append(trajectory_id)
        else:
            minx=min(plane_info)
            new_plane_info=[x-minx for x in plane_info]
            normalized_trajectory_plane_dict[trajectory_id]=new_plane_info

    # utils.write_ls("length of each trajectory",trajectory_len_ls)
    # utils.write_ls("number of event in each trajectory", trajectory_event_count_ls)
    # utils.write_ls("long_lasting_ls_length", long_lasting_ls_length)
    # analysisAndVis.reconstruct_image_from_trajectory_index(long_lasting_ls_idx, trajectory_pos_dict, info_dict, "long lasting location")
    return normalized_trajectory_plane_dict

def fill_in_normalized_trajectory_data(normalized_trajectory_plane_dict):
    trajectory_length = 2 ** 10
    filled_normalized_trajectory_plane_dict={}
    for trajectory_idx, plane_info in normalized_trajectory_plane_dict.items():
        filled_plane_info_ls=[0] * trajectory_length
        for idx in plane_info:
            if idx < trajectory_length:
                filled_plane_info_ls[idx]=1
            else:
                break
        filled_normalized_trajectory_plane_dict[trajectory_idx]=filled_plane_info_ls
    return filled_normalized_trajectory_plane_dict


def fft_transfer_of_filled_plane_dict(filled_normalized_trajectory_plane_dict):
    fft_dict={}
    for trajectory_idx,filled_plane_info_ls in filled_normalized_trajectory_plane_dict.items():
        Yp = np.fft.fft(filled_plane_info_ls, 2 ** 10)
        fft_dict[trajectory_idx]=abs(Yp)[0:len(Yp) // 2]
    #utils.write_dict("fft_dict",fft_dict)
    return fft_dict

def calculate_std_of_fft_dict(fft_dict,folder_name="./"):
    std_fft_dict={}
    for trajectory_idx,fft_ls in fft_dict.items():
        std_fft_dict[trajectory_idx]=np.std(fft_ls)
    utils.write_dict("std_fft_dict",std_fft_dict,folder_name=folder_name)
    return std_fft_dict



def model_func(t, A, K, C):
    return A * np.exp(-K * t) + C


def fit_exp_nonlinear(t, y):
    try:
        opt_parms, parm_cov = sp.optimize.curve_fit(model_func, t, y,maxfev=5000)
        A, K, C = opt_parms
    except:
        A,K,C=-10,-10,-10
    return A, K, C

def fit_decay_ratio_all(fft_data):
    dataToFit = fft_data
    dataToFit = [x / max(dataToFit) for x in dataToFit]
    t = np.linspace(0, 1, len(dataToFit))
    A, K, C = fit_exp_nonlinear(t, dataToFit)
    #fit_y = model_func(t, A, K, C)
    return K

def fit_decay_ratio_choice(fft_data):
    #! parm =10
    dataToFit = fft_data[::10]
    dataToFit = [x / max(dataToFit) for x in dataToFit]
    t = np.linspace(0, 1, len(dataToFit))
    A, K, C = fit_exp_nonlinear(t, dataToFit)
    #fit_y = model_func(t, A, K, C)
    return K


def calculate_decay_of_fft_dict(fft_dict,folder_name="./"):
    decay_fft_dict_all = {}
    decay_fft_dict_choice = {}
    for trajectory_idx,fft_ls in fft_dict.items():
        decay_fft_dict_all[trajectory_idx]=fit_decay_ratio_all(fft_ls)
        decay_fft_dict_choice[trajectory_idx] = fit_decay_ratio_choice(fft_ls)
    utils.write_dict("decay_fft_dict_all",decay_fft_dict_all,folder_name=folder_name)
    utils.write_dict("decay_fft_dict_choice", decay_fft_dict_choice,folder_name=folder_name)
    return decay_fft_dict_all,decay_fft_dict_choice


def subregion_fit_decay(trajectory_idx_ls,decay_fft_dict,name):
    subregion_dict = {}
    for trajectory_idx,decay_ratio in decay_fft_dict.items():
        if trajectory_idx in trajectory_idx_ls:
            subregion_dict[trajectory_idx]=decay_ratio
    utils.write_dict(name, subregion_dict)


def subregion_fft_std(trajectory_idx_ls,std_fft_dict,name):
    subregion_dict={}
    for trajectory_idx,std_val in std_fft_dict.items():
        if trajectory_idx in trajectory_idx_ls:
            subregion_dict[trajectory_idx]=std_val
    utils.write_dict(name,subregion_dict)





