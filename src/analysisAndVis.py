import numpy as np
#from informationDict import info_dict
import src.visualFunctions as visualFunctions
import src.utils as utils
import src.fft_ as fft_
import src.makeSubRegionData as makeSubRegionData

def analysis_dict(data_dict):

    trajectory_plane_dict={}
    trajectory_pos_dict={}
    for trajectory_idx,data_ls in data_dict.items():
        plane_ls=[]
        pos_ls=[]
        for info in data_ls:
            plane, pos, intensity = info
            plane_ls.append(plane)
            pos_ls.append(pos)
        #! parm =2
        if len(plane_ls)<=2:
            pass
        else:
            trajectory_plane_dict[trajectory_idx]=plane_ls
            trajectory_pos_dict[trajectory_idx]=pos_ls
    return trajectory_plane_dict,trajectory_pos_dict

def max_distance_in_trajectory(trajectory_pos_dict,folder_name="./"):
    distance_dict={}
    for trajectory_idx,pos_ls in trajectory_pos_dict.items():
        x_ls,y_ls= zip(*pos_ls)
        dx=max(x_ls)-min(x_ls)
        dy=max(y_ls)-min(y_ls)
        distance_dict[trajectory_idx] = (dx,dy)

    utils.write_dict("max distance between each trajectory",distance_dict,folder_name=folder_name)
    return distance_dict



def trajectory_on_time_analysis(trajectory_pos_dict,trajectory_plane_dict,folder_name="./"):
    """
    :param trajectory_pos_dict:
    :param trajectory_plane_dict:
    :return:
    dict {key : pixel(x,y), val : (time,trajectory_id) }

    how many trajectory on each pixel and info of each trajectory
    """
    trajectory_ontime_of_pixel_dict = {}
    for trajectory_idx,pos_ls in trajectory_pos_dict.items():
        plane_ls=trajectory_plane_dict[trajectory_idx]
        for idx,pos in enumerate(pos_ls):
            posx,posy = pos[0],pos[1]
            pixx= round(posx/(93/8))
            pixy=round(posy/(93/8))
            pixel=(pixy,pixx)
            if pixel not in trajectory_ontime_of_pixel_dict:
                trajectory_ontime_of_pixel_dict[pixel]=[]
            trajectory_ontime_of_pixel_dict[pixel].append((plane_ls[idx],trajectory_idx))
    #utils.write_dict("trajectory_ontime_of_pixel_dict",trajectory_ontime_of_pixel_dict,folder_name=folder_name)
    return trajectory_ontime_of_pixel_dict



def number_of_onframes_of_each_trajectory(trajectory_plane_dict,folder_name="./"):
    number_of_onframes_of_each_trajectory_dict={}
    for trajectory_idx,plane_ls in trajectory_plane_dict.items():
        number_of_onframes_of_each_trajectory_dict[trajectory_idx]=len(set(plane_ls))
    utils.write_dict("number_of_onframes_of_each_trajectory",number_of_onframes_of_each_trajectory_dict,folder_name=folder_name)

def first_blast_time_of_trajectory(trajectory_plane_dict,folder_name="./"):
    first_blast_time_of_trajectory_dict={}
    for trajectory_idx,plane_ls in trajectory_plane_dict.items():
        first_blast_time_of_trajectory_dict[trajectory_idx]=plane_ls[0]
    utils.write_dict("first_blast_time_of_trajectory_dict",first_blast_time_of_trajectory_dict,folder_name=folder_name)

def make_trajectory_pixel_exchange_dict(trajectory_ontime_of_pixel_dict,folder_name="./"):
    pixel_to_trajecyory_dict ={}
    pixel_to_plane_dict ={}
    trajectory_to_pixel_dict ={}
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        plane_info, trajectory_info = zip(*pixel_info)
        trajectory_list=list(set(trajectory_info))
        pixel_to_trajecyory_dict[pixel]= trajectory_list
        pixel_to_plane_dict[pixel] = plane_info
        for trajectory_idx in trajectory_list:
            if trajectory_idx not in trajectory_to_pixel_dict:
                trajectory_to_pixel_dict[trajectory_idx]=[]
            trajectory_to_pixel_dict[trajectory_idx].append(pixel)
    pixel_idx=0
    idx_pixel_dict={}
    idx_trajectory_dict={}
    idx_plane_dict ={}
    for pixel,trajectory_ls in pixel_to_trajecyory_dict.items():
        idx_pixel_dict[pixel_idx]=pixel
        idx_trajectory_dict[pixel_idx]=trajectory_ls
        idx_plane_dict[pixel_idx]=pixel_to_plane_dict[pixel]
        pixel_idx+=1
    utils.write_dict("idx_to_pixel_dict",idx_pixel_dict,folder_name=folder_name)
    utils.write_dict("idx_to_trajectory_dict", idx_trajectory_dict,folder_name=folder_name)
    utils.write_dict("idx_to_plane_dict", idx_plane_dict,folder_name=folder_name)
    utils.write_dict("trajectory_to_pixel_dict",trajectory_to_pixel_dict,folder_name=folder_name)
    return pixel_to_trajecyory_dict,trajectory_to_pixel_dict

def number_of_trajectory_sharing_same_pixel(pixel_to_trajecyory_dict, trajectory_to_pixel_dict,folder_name="./"):
    trajectory_sharing_dict={}
    for trajectory_idx,pixel_ls in trajectory_to_pixel_dict.items():
        common_trajectory=[]
        for pixel in pixel_ls:
            common_trajectory.extend(pixel_to_trajecyory_dict[pixel])
        trajectory_sharing_dict[trajectory_idx] = common_trajectory
    utils.write_dict("trajectory_sharing_same_pixel",trajectory_sharing_dict,folder_name)
    return trajectory_sharing_dict

def crop_subregion_idx_from_full(diagraph_point, angle, dataTrace_N,trajectory_ontime_of_pixel_dict,name,folder_name="./"):
    rectangle_of = makeSubRegionData.find_rectangle_info(diagraph_point, angle)
    pixel_ls = makeSubRegionData.crop_pixcel_from_full(rectangle_of, trajectory_ontime_of_pixel_dict)
    trajectory_idx_ls = makeSubRegionData.trajectory_idx_of_region(pixel_ls,
                                                                        trajectory_ontime_of_pixel_dict)  # trajectory_idx of each source
    utils.write_ls(name+"_trajectory_idx",trajectory_idx_ls,folder_name)
    utils.write_ls(name + "_pixel_idx", pixel_ls,folder_name)
    return pixel_ls,trajectory_idx_ls


def analysis_imported_data(data_dict,diagraph_point_atto=None,diagraph_point_af647=None, angle=None,folder_name="./"):
    """

    :return:
    """
    print("number of trajectory of imported image : {}".format(len(data_dict)))
    trajectory_plane_dict,trajectory_pos_dict=analysis_dict(data_dict)  #1.trajectory idx
    distance_dict=max_distance_in_trajectory(trajectory_pos_dict,folder_name=folder_name)  #2.distance in pixel
    number_of_onframes_of_each_trajectory(trajectory_plane_dict,folder_name=folder_name)  #3.number of onframe
    trajectory_ontime_of_pixel_dict=trajectory_on_time_analysis(trajectory_pos_dict,trajectory_plane_dict) # trajectory on each pixel
    pixel_to_trajecyory_dict, trajectory_to_pixel_dict=make_trajectory_pixel_exchange_dict(trajectory_ontime_of_pixel_dict,folder_name=folder_name) # trajectory to pixel exchange dict
    trajectory_sharing_dict = number_of_trajectory_sharing_same_pixel(pixel_to_trajecyory_dict,trajectory_to_pixel_dict,folder_name=folder_name) #4. number of trajectory on same pixel

    normalized_trajectory_plane_dict = fft_.norm_trajectory_data(trajectory_plane_dict, trajectory_pos_dict,folder_name=folder_name) # normalize preparing fft transfer
    filled_normalized_trajectory_plane_dict = fft_.fill_in_normalized_trajectory_data(normalized_trajectory_plane_dict) # to 1 0 signal
    fft_dict = fft_.fft_transfer_of_filled_plane_dict(filled_normalized_trajectory_plane_dict) # calculate fft
    std_fft_dict = fft_.calculate_std_of_fft_dict(fft_dict,folder_name=folder_name) # std of fft transfered signal
    decay_fft_dict = fft_.calculate_decay_of_fft_dict(fft_dict,folder_name=folder_name) # decay ratio of fft transfered signal

    if diagraph_point_af647:
        _, _ = crop_subregion_idx_from_full(diagraph_point_af647, angle, data_dict, trajectory_ontime_of_pixel_dict, "af647")
    if diagraph_point_atto:
        _, _ = crop_subregion_idx_from_full(diagraph_point_atto, angle, data_dict, trajectory_ontime_of_pixel_dict,
                                            "atto")



