
import numpy as np
import scipy as sp
import scipy.optimize
from trajectory.trajectoryProcessingFunctions import trajectory_processing_functions


class trajectory_fft():
    def __init__(self, ls,lim=2 ** 10):

        self.plane_ls = ls
        self.fft_lim = lim
        #self.main()
        minx = min(self.plane_ls)
        new_plane_ls = [x - minx for x in self.plane_ls]
        stem_ls = trajectory_processing_functions.frame_ls2_stemls(new_plane_ls)
        self.stem_ls = stem_ls
        Yp = np.fft.fft(stem_ls,self.fft_lim )
        fft_ls = abs(Yp)[0:len(Yp) // 2]
        self.fft_ls = fft_ls

    def model_func(self,t, A, K, C):

        return A * np.exp(-K * t) + C

    def fit_exp_nonlinear(self,t, y):

        try:
            opt_parms, parm_cov = sp.optimize.curve_fit(self.model_func, t, y, maxfev=500)
            A, K, C = opt_parms
        except:
            A, K, C = -10, -10, -10
        return A, K, C


    def fit_decay_ratio_all(self,fft_data):

        dataToFit = fft_data
        dataToFit = [x / max(dataToFit) for x in dataToFit]
        t = np.linspace(0, 1, len(dataToFit))
        A, K, C = self.fit_exp_nonlinear(t, dataToFit)
        # fit_y = model_func(t, A, K, C)
        return K

    def fit_decay_ratio_choice(self,fft_data):
        # ! parm =10
        dataToFit = fft_data[::10]
        dataToFit = [x / max(dataToFit) for x in dataToFit]
        t = np.linspace(0, 1, len(dataToFit))
        A, K, C = self.fit_exp_nonlinear(t, dataToFit)
        # fit_y = model_func(t, A, K, C)
        return K

    def main(self):
        self.std_fft = np.std(self.fft_ls)
        self.decay_all = self.fit_decay_ratio_all(self.fft_ls)
        self.decay_select = self.fit_decay_ratio_choice(self.fft_ls)

    def get_fft_ls(self):
        return self.fft_ls

    def get_stem_ls(self):
        return self.stem_ls

