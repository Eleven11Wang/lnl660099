def pixel_neighbor(pixel):
    neighbor_ls = []
    pixx, pixy = pixel
    for i in range(-1,2):
        for j in range(-1,2):
            newx = pixx+i
            newy = pixy+j
            neighbor_ls.append((in_range(newx), in_range(newy)))
    neighbor_ls= list(set(neighbor_ls))
    return neighbor_ls

from scipy import signal
import numpy as np
def make_kernel():
    """
    todo input kernel size, return kernel
    :return:
    """
    scharr = np.array([[ 1, 1,  1],
                    [1, 1, 1],
                    [ 1, 1,  1]])
    return scharr
def in_range(newx,low_limit=0,up_limit=4096):
    newx = max(low_limit, newx)
    newx = min(up_limit, newx)
    return newx

def find_overlap_method1(img1,img2):

    """
    todo check whether this function give the right output
    :param img1:
    :param img2:
    :return:
    """
    over_laped_region_ls_img1 = help_find_overlap1(img1,img2)
    over_laped_region_ls_img2 = help_find_overlap1(img2,img1)
    return over_laped_region_ls_img1,over_laped_region_ls_img2


def help_find_overlap1(img1,img2):
    x_lim, y_lim = img1.shape
    img2_with_neighbor =signal.convolve2d(img2, make_kernel(), boundary='symm', mode='same')
    over_laped_region_ls =[]
    for x in range(x_lim):
        for y in range(y_lim):
            if img1[x,y] > 0 and img2_with_neighbor[x,y] > 0:
                over_laped_region_ls.append((x,y))
    return over_laped_region_ls


