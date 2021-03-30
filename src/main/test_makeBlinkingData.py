PATH_DICT=dict(
    PATH_ATTO_NUP_PFA="/Users/wangjiahui/blinking_data/ATTO/NUP98/PFA/20210323",
    PATH_ATTO_NUP_M="/Users/wangjiahui/blinking_data/ATTO/NUP98/M/20210323",
    PATH_AF647_NUP_PFA="/Users/wangjiahui/blinking_data/AF647/NUP98/PFA",
    PATH_AF647_NUP_M="/Users/wangjiahui/blinking_data/AF647/NUP98/M"
    )
from fileIO.readFileInFolder import read_allfiles_infolder_toAdict

import time

def main():
    st = time.time()
    blinking_data_dict={}

    for name,path in PATH_DICT.items():
        blinking_data_dict[name] = read_allfiles_infolder_toAdict(path)
    end = time.time()

    print("total time consumed = {}".format(end-st))
    for name,dictionary in blinking_data_dict.items():
        print(name+ ", number of trajectory counted :{}".format(len(dictionary)))


    return blinking_data_dict



if __name__=="__main__":
    main()

