

import utils.utils as utils

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



def make_trajectory_pixel_exchange_dict(trajectory_ontime_of_pixel_dict,folder_name="./",idx_num=0):
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
    utils.write_dict("{}_idx_to_pixel_dict".format(idx_num), idx_pixel_dict, folder_name=folder_name)
    utils.write_dict("{}_idx_to_trajectory_dict".format(idx_num), idx_trajectory_dict, folder_name=folder_name)
    utils.write_dict("{}_idx_to_plane_dict".format(idx_num), idx_plane_dict, folder_name=folder_name)
    utils.write_dict("{}_trajectory_to_pixel_dict".format(idx_num), trajectory_to_pixel_dict, folder_name=folder_name)
    return pixel_to_trajecyory_dict,trajectory_to_pixel_dict