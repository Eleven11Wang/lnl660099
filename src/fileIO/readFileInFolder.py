import glob
import os
from trajectory.trajectoryTrackingNew import dataTrajectory


def read_allfiles_infolder(path = '/some/path/to/file'):
    print("doc of data_trajectory: ",dataTrajectory.__doc__)
    data_trajectory_dict_ls = []
    file_name_ls=[]
    for filename in glob.glob(os.path.join(path, '*.txt')):
        print(filename)
        filename = os.path.join(os.getcwd(), filename)
        ob_data=dataTrajectory(filename)
        data_trajectory_dict = ob_data.get_trajectory_dict()
        print(ob_data.get_info())
        print("\n")
        data_trajectory_dict_ls.append(data_trajectory_dict)
        file_name_ls.append(filename)
    return data_trajectory_dict_ls


def read_allfiles_infolder_toAdict(path = '/some/path/to/file'):
    print("doc of data_trajectory: ",dataTrajectory.__doc__)
    trajectory_dataDict={}
    file_name_ls=[]
    global_idx_num = 1
    for filename in glob.glob(os.path.join(path, '*.txt')):
        print(filename)
        filename = os.path.join(os.getcwd(), filename)
        ob_data=dataTrajectory(filename)
        data_trajectory_dict = ob_data.get_trajectory_dict()
        print(ob_data.get_info())
        print("\n")
        for k,v in data_trajectory_dict.items():
            trajectory_dataDict[global_idx_num]=v
            global_idx_num+=1
        file_name_ls.append(filename)
    return trajectory_dataDict

def read_a_expample_file_in_folder(path):
    print("doc of data_trajectory: ", dataTrajectory.__doc__)
    filename_ls = glob.glob(os.path.join(path, '*.txt'))
    print(filename_ls)
    filename = filename_ls[0]
    print(filename)
    filename = os.path.join(os.getcwd(), filename)
    ob_data = dataTrajectory(filename)
    data_trajectory_dict = ob_data.get_trajectory_dict()

    print(ob_data.get_info())
    print("\n")
    return data_trajectory_dict
