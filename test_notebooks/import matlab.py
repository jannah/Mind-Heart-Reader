
# coding: utf-8

# In[1]:

'''This code shows how to import .mat file (MATLAB format) into dictionary using scipy.io'''

# First we will import the scipy.io
import scipy.io
mat_file = '../sensor_data/HMJ/Results-HMJ-18-Oct-2014-00-24-17.mat'
# load .mat file into dictionary x
data = scipy.io.loadmat(mat_file)
print data
# easymatfile.mat contains 3 matlab variables
# a: [10x30]
# b: [20x100]
# c: [1x1]
