
import numpy as np
import src.utils as utils

def reconstruct_from_trajectory_ontime_of_pixel_dict(img,trajectory_ontime_of_pixel_dict):
    cnt=0
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        pixy,pixx= pixel
        if img[pixy,pixx]==0:
            cnt+=1
        img[pixy,pixx] += len(pixel_info)
    utils.same_img(img, "reconstructed_image")
    print("total_pixel_number : {}".format(cnt))
    return img



def reconstruct_image_from_trajectory_index(idx_ls,trajectory_pos_dict,info_dict,name):
    img = np.zeros([info_dict["image_height"] * 8, info_dict["image_width"] * 8])
    for trajectory_idx,pos_ls in trajectory_pos_dict.items():
        if trajectory_idx in idx_ls:
            for pos in pos_ls:
                posx, posy = pos[0], pos[1]
                pixx = round(posx / (93 / 8))
                pixy = round(posy / (93 / 8))
                img[pixy, pixx] += 1
    utils.same_img(img,name)



def reconstruct_subimage_from_trajectory_ontime_of_pixel_dict(img,trajectory_ontime_of_pixel_dict,pixel_ls,which_region=""):
    cnt=0
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        if pixel in pixel_ls:
            pixy,pixx= pixel
            if img[pixy,pixx]==0:
                cnt+=1
            img[pixy,pixx] += len(pixel_info)
        else:
            pass
    utils.same_img(img, "reconstructed_image_"+which_region)
    print("total_pixel_number_{}: {}".format(which_region,cnt))
    return img



def reconstruct_image(objc,trajectory_ontime_of_pixel_dict,pixel_idx_ls=[],sub_name=None):

    img = np.zeros([objc.height * 8, objc.width * 8])

    if not pixel_idx_ls and not sub_name:
        img=reconstruct_from_trajectory_ontime_of_pixel_dict(img,trajectory_ontime_of_pixel_dict)
    else:
        img=reconstruct_subimage_from_trajectory_ontime_of_pixel_dict(img,trajectory_ontime_of_pixel_dict,pixel_idx_ls,sub_name)

    return img


def full_trajectory_heat_dict(img,trajectory_ontime_of_pixel_dict):
    trajectory_heat_dict = {}
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        plane_info, trajectory_info = zip(*pixel_info)
        pixy, pixx = pixel
        trajectory_heat_dict[pixel] = len(set(trajectory_info))
        img[pixy, pixx] += trajectory_heat_dict[pixel]

    utils.same_img(img, "heat_image_of_trajactory")
    return trajectory_heat_dict




def subRegion_trajectory_heat_dict(img,trajectory_ontime_of_pixel_dict,pixel_ls,sub_name):
    trajectory_heat_dict = {}
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        if pixel in pixel_ls:
            plane_info, trajectory_info = zip(*pixel_info)
            pixy, pixx = pixel
            trajectory_heat_dict[pixel] = len(set(trajectory_info))
            img[pixy, pixx] += trajectory_heat_dict[pixel]
        else:
            pass

    utils.same_img(img, "heat_image_of_trajactory_"+sub_name)
    return trajectory_heat_dict


def heat_image_of_trjactory(objc,trajectory_ontime_of_pixel_dict,pixel_ls=[],subname=""):

    img=np.zeros([objc.height * 8, objc.width * 8])

    if not pixel_ls and not subname:
        trjectory_heat_dict=full_trajectory_heat_dict(img,trajectory_ontime_of_pixel_dict)
    else:
        trjectory_heat_dict = subRegion_trajectory_heat_dict(img, trajectory_ontime_of_pixel_dict,pixel_ls,subname)

    count_ls=[]
    for pixel,cnt in trjectory_heat_dict.items():
        count_ls.append(cnt)
    utils.write_ls("count of trajectory in each pixel" +subname,count_ls)
