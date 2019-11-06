from __future__ import division
import numpy as np
import math
import mayavi.mlab as mlab
import cv2

def draw_voxel(voxel_coords, is_grid=False, is_axis = True, fig=None):

	pxs=voxel_coords[:,0]
	pys=voxel_coords[:,1]
	pzs=voxel_coords[:,2]

	if fig is None: fig = mlab.figure(figure=None, bgcolor=(0,0,0), fgcolor=None, engine=None, size=(10000, 50000))

	mlab.points3d(
		pxs, pys, pzs, #prs,
		mode="cube",  # 'point'  'sphere'
		colormap='cool',  #'bone',  #'spectral',  #'copper',
		scale_factor=1,
		figure=fig)
	mlab.orientation_axes()
	mlab.view(azimuth=180,elevation=None,distance=100,focalpoint=[ 0 , 0, 0])#2.0909996 , -1.04700089, -2.03249991

	return fig

def test():
	import os
	import glob
	import matplotlib.pyplot as plt

	data_file = "voxel5.npy"
	print("Processing: ", data_file)
	data = np.load(data_file)
	data = data.reshape((-1, 3))
	data = data - np.array([min(data[:,0]), min(data[:,1]), min(data[:,2])])
	print('x_min', min(data[:,0]))
	print('y_min', min(data[:,1]))
	print('z_min', min(data[:,2]))
	print('x_max', max(data[:,0]))
	print('y_max', max(data[:,1]))
	print('z_max', max(data[:,2]))
	fig = draw_voxel(data, is_grid=False)
	mlab.show()
	

if __name__ == '__main__':
	test()