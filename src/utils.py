import pickle
from PIL import Image
import json

def write_ls(name,ls_to_write,folder_name = "./"):
    with open(folder_name+str(name)+".txt", 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(ls_to_write, filehandle)

def read_ls(name):
    with open(str(name)+".txt", 'rb') as filehandle:
        # read the data as binary data stream
        placesList = pickle.load(filehandle)
    return placesList

def same_img(image_array,name,image_type="tif"):
    # save tif or png
    im = Image.fromarray(image_array)
    if image_type=="tif":

        im.save("{}.tif".format(name))
    else:
        im.save("{}.png".format(name))

def write_dict(name,dict_to_write,folder_name="./"):
    with open(folder_name+'dict_data/{}.txt'.format(name), 'w') as outfile:
        json.dump(dict_to_write, outfile)

def read_dict(name,folder_name="./"):
    with open(folder_name+'dict_data/{}.txt'.format(name)) as json_file:
        data = json.load(json_file)
    return data


def reconstruct_trajectory_ontime_of_pixel_dict(idx_to_pixel_dict,idx_to_trajectory_dict,idx_to_plane_dict):
    trajectory_ontime_of_pixel_dict={}
    for idx,pixel in idx_to_pixel_dict.items():
        pixel_idx=(pixel[0],pixel[1])
        trajectory_ls_temp = idx_to_trajectory_dict[idx]
        plane_ls_temp = idx_to_plane_dict[idx]
        trajectory_ontime_of_pixel_dict[pixel_idx]= list(zip(plane_ls_temp,trajectory_ls_temp))
    return trajectory_ontime_of_pixel_dict
