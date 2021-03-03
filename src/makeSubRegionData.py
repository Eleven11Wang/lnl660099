import numpy as np
#from informationDict import  info_dict
def crop_region(dipoint,angle):
    point1,point3=dipoint
    x1,y1=point1
    x3,y3=point3
    t1=np.tan( angle/180 * 3.14)
    t2=-1/t1
    c1=y1-t1*x1
    c2=y3-t1*x3
    c3=y1-t2*x1
    c4=y3-t2*x3
    if c1 > c2:
        c1,c2=c2,c1
    if c3 > c4:
        c3,c4=c4,c3
    return [t1,t2,c1,c2,c3,c4]


def is_in_region(x,y,idx_ls,height):
    # dc is the instance of imported data
    t1,t2,c1,c2,c3,c4=idx_ls
    y=height*8-y
    if ((y-t1*x) > c1 ) and ((y-t1*x) < c2):
        if ((y-t2*x) > c3)  and ((y-t2*x) < c4):
            return True
    return False

def find_rectangle_info(diagraph_point,angle):
    # dc is the instance of imported data
    height=info_dict["image_height"]
    rectangle_info=crop_region([(diagraph_point[0][0],height*8-diagraph_point[0][1]),
                    (diagraph_point[1][0],height*8-diagraph_point[1][1])],angle)
    return rectangle_info


def crop_pixcel_from_full(rectangle_info, trajectory_ontime_of_pixel_dict):
    sample_idx = []
    height = info_dict["image_height"]
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        ypos, xpos = pixel
        if is_in_region(xpos , ypos , rectangle_info,height):
            sample_idx.append(pixel)
    return sample_idx

def trajectory_idx_of_region(pixcel_region_ls,trajectory_ontime_of_pixel_dict):
    """
    return trajectory_idx of each source
    :param pixcel_region_ls:
    :param trajectory_ontime_of_pixel_dict:
    :return: list [trajectory_idx]
    """
    trajectory_idx_ls=[]
    for pixel, pixel_info in trajectory_ontime_of_pixel_dict.items():
        if pixel in pixcel_region_ls:
            plane_info, trajectory_info = zip(*pixel_info)
            trajectory_idx_ls.extend(list(set(trajectory_info)))

    return list(set(trajectory_idx_ls))

# def make_region_data(point_region,angle,pos_data):
#     idx_ls=find_idx_ls(point_region,angle)
#     trajectory_idx_region=cropSample_new(idx_ls,pos_data)
#     return trajectory_idx_region
