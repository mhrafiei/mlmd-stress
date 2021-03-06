# -*- coding: utf-8 -*-
"""pclass_mlmd.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p_lJxGPimS9lWwmeqLhPxxGQ2KjnKwjp
"""

import h5py
import numpy as np
from keras.models import load_model

cos  = np.cos 
sin  = np.sin
pi   = np.pi
sqrt = np.sqrt
acos = np.arccos

class MLMD():
    def __init__(self,theta_i, radia_local_j, alpha_local_j, theta_j):
      self.theta_i       = theta_i
      self.theta_j       = theta_j
      self.radia_local_j = alpha_local_j
      self.alpha_local_j = alpha_local_j

    def fun_slxx(a,r):
        slxx = -(3*sin(a)-2*sin(a)**3)/r
        return slxx

    def fun_slxy(a,r):
        slxy = -(1*cos(a)-2*cos(a)**3)/r
        return slxy

    def fun_slyy(a,r):
        slyy = +(1*sin(a)-2*sin(a)**3)/r
        return slyy

    def fun_sgxx(a,r,t):
        sgxx = MLMD.fun_slxx(a,r)*cos(t)**2+1*MLMD.fun_slyy(a,r)*sin(t)**2-2*MLMD.fun_slxy(a,r)*sin(t)*cos(t)
        return sgxx

    def fun_sgxy(a,r,t):
        sgxy = -(MLMD.fun_slyy(a,r)-MLMD.fun_slxx(a,r))*sin(t)*cos(t)+(MLMD.fun_slxy(a,r))*(cos(t)**2-sin(t)**2)
        return sgxy

    def fun_sgyy(a,r,t):
        sgyy = 1*MLMD.fun_slxx(a,r)*sin(t)**2+1*MLMD.fun_slyy(a,r)*cos(t)**2+2*MLMD.fun_slxy(a,r)*sin(t)*cos(t)
        return sgyy
        
    def fun_sgxxi(a,sgxx,t):
        rlj = (sin(t)**2*(sin(a) - 2*sin(a)**3) - cos(t)**2*(3*sin(a) - 2*sin(a)**3) + 2*cos(t)*sin(t)*(cos(a) - 2*cos(a)**3))/r
        return rlj

    def fun_sgxyi(a,sgxy,t):
        rlj = -((cos(t)**2 - sin(t)**2)*(cos(a) - 2*cos(a)**3) + cos(t)*sin(t)*(4*sin(a) - 4*sin(a)**3))/r
        return rlj

    def fun_sgyyi(a,sgyy,t):
        rlj = -(sin(t)**2*(3*sin(a) - 2*sin(a)**3) - cos(t)**2*(sin(a) - 2*sin(a)**3) + 2*cos(t)*sin(t)*(cos(a) - 2*cos(a)**3))/r
        return rlj

    def fun_scale(x,lb=0,ub=1):
        return ((x-np.min(x,axis=0))/(np.max(x,axis=0)-np.min(x,axis=0)))*(ub-lb) + lb

    def fun_scaleback(x,lb,ub):
        delta_val = ub-lb
        return x*delta_val + lb

    def fun_fg(a,r,g,t):
      return (cos(3*a - 2*g + 2*t) + cos(a - 2*g + 2*t))/(2*r);
    
    def fun_wrapTo2pi(x):
        xwrap = np.remainder(x, 2*pi)
        idx = np.abs(xwrap) > 2*pi
        xwrap[idx] -= 2*pi * np.sign(xwrap[idx]);
        return xwrap

    def fun_mlmd_force(alpha_local_j, radia_local_j, theta_j, theta_i):
      force_max         = 1.338688085676038e+09
      model             = load_model('model_force.h5')
      dict_info         = np.load('model_force_info.npy', allow_pickle = True) 
      radia_logarith_lb = dict_info[0]['radia_logarith_lb']
      radia_logarith_ub = dict_info[0]['radia_logarith_ub']

      radia_local_j     = np.log10(radia_local_j)

      radia_logarith_lb = np.ones((1,1))*radia_logarith_lb
      radia_logarith_ub = np.ones((1,1))*radia_logarith_ub

      #print(radia_logarith_ub)
      #print(radia_logarith_lb)

      r_all             = np.concatenate((radia_logarith_lb, radia_logarith_ub, radia_local_j), axis = 0)
      r_scl             = MLMD.fun_scale(r_all,0,1)
      a_scl             = alpha_local_j/(2*np.pi)
      g_scl             = theta_j/(2*np.pi)
      t_scl             = theta_i/(2*np.pi)

      if np.int(r_scl[0]) != 0 | np.int(r_scl[1]) !=1:
        print('error! diclocations are not within the scaled limits; look into model_force_info.npy')
        dataes_scl = None
        dataes_raw = None
      else:
        r_scl      = r_scl[2:]
        datain_scl = np.concatenate((t_scl, a_scl, r_scl, g_scl), axis = 1)
        dataes_scl = model.predict(datain_scl)
        dataes_raw = dataes_scl * force_max

      return dataes_raw

    def fun_mlmd_stress(alpha_local_j, radia_local_j, theta_i):
      sigxx_max = +1.893190846550328e+09;
      sigyy_max = +1.893190846550328e+09;
      sigxy_max = +1.338688085676038e+09;

      model             = load_model('model_stress.h5')
      dict_info         = np.load('model_stress_info.npy', allow_pickle = True) 
      radia_logarith_lb = dict_info[0]['radia_logarith_lb']
      radia_logarith_ub = dict_info[0]['radia_logarith_ub']

      radia_local_j     = np.log10(radia_local_j)

      radia_logarith_lb = np.ones((1,1))*radia_logarith_lb
      radia_logarith_ub = np.ones((1,1))*radia_logarith_ub

      #print(radia_logarith_ub)
      #print(radia_logarith_lb)

      r_all             = np.concatenate((radia_logarith_lb, radia_logarith_ub, radia_local_j), axis = 0)
      r_scl             = MLMD.fun_scale(r_all,0,1)
      a_scl             = alpha_local_j/(2*np.pi)
      t_scl             = theta_i/(2*np.pi)

      if np.int(r_scl[0]) != 0 | np.int(r_scl[1]) !=1:
        print("error! some of j's points are not within the scaled limits; look into model_stress_info.npy")
        dataes_scl = None
        dataes_raw = None
      else:
        r_scl      = r_scl[2:]
        datain_scl = np.concatenate((t_scl, a_scl, r_scl), axis = 1)
        dataes_scl = model.predict(datain_scl)
        dataes_raw = dataes_scl
        dataes_raw[:,0] = dataes_raw[:,0] * sigxx_max
        dataes_raw[:,1] = dataes_raw[:,1] * sigyy_max
        dataes_raw[:,2] = dataes_raw[:,2] * sigxy_max

      return dataes_raw

## stress example

#alpha_local_j = np.ones((10,1)) * np.pi/4 *np.random.rand(10,1)
#radia_local_j = np.ones((10,1)) * 3e-9 
#theta_i       = np.ones((10,1)) * 0 
#dataes_raw    = MLMD.fun_mlmd_stress(alpha_local_j, radia_local_j, theta_i)
#dataou_raw    = np.concatenate((MLMD.fun_sgxx(alpha_local_j, radia_local_j, theta_i), 
#                                MLMD.fun_sgyy(alpha_local_j, radia_local_j, theta_i), 
#                                MLMD.fun_sgxy(alpha_local_j, radia_local_j, theta_i)), axis = 1)

#print("$$ Order is sigma_xx, sigma_yy, and sigma_xy $$")
#print("   ")
#for i0 in range(dataou_raw.shape[0]):
#  print('real = {} | estmation = {} | error = {}'.format(dataou_raw[i0], dataes_raw[i0] , np.abs(dataou_raw[i0] - dataes_raw[i0])))

## force example

#alpha_local_j = np.ones((10,1)) * np.pi/4 *np.random.rand(10,1)
#radia_local_j = np.ones((10,1)) * 3e-9 
#theta_j       = np.ones((10,1)) * np.pi/4*np.random.rand(10,1)
#theta_i       = np.ones((10,1)) * 0 
#dataes_raw    = MLMD.fun_mlmd_force(alpha_local_j, radia_local_j, theta_j, theta_i)
#dataou_raw    = MLMD.fun_fg(alpha_local_j, radia_local_j, theta_j, theta_i)

#for i0 in range(dataou_raw.shape[0]):
#  print('real = {} | estmation = {} | error = {}'.format(dataou_raw[i0], dataes_raw[i0] , np.abs(dataou_raw[i0] - dataes_raw[i0])))