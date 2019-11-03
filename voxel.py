from __future__ import division
import numpy as np
from config import config as cfg
import math
import mayavi.mlab as mlab
import cv2

def draw_lidar(lidar, is_grid=False, is_axis = True, is_top_region=True, fig=None):

	pxs=lidar[:,0]
	pys=lidar[:,1]
	pzs=lidar[:,2]
	#prs=lidar[:,3]

	if fig is None: fig = mlab.figure(figure=None, bgcolor=(0,0,0), fgcolor=None, engine=None, size=(1000, 500))

	mlab.points3d(
		pxs, pys, pzs, #prs,
		mode='point',  # 'point'  'sphere'
		colormap='gnuplot',  #'bone',  #'spectral',  #'copper',
		scale_factor=1,
		figure=fig)

	#draw grid
	if is_grid:
		mlab.points3d(0, 0, 0, color=(1,1,1), mode='sphere', scale_factor=0.2)

		for y in np.arange(-50,50,1):
			x1,y1,z1 = -50, y, 0
			x2,y2,z2 =  50, y, 0
			mlab.plot3d([x1, x2], [y1, y2], [z1,z2], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)

		for x in np.arange(-50,50,1):
			x1,y1,z1 = x,-50, 0
			x2,y2,z2 = x, 50, 0
			mlab.plot3d([x1, x2], [y1, y2], [z1,z2], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)

	#draw axis
	if is_axis:
		mlab.points3d(0, 0, 0, color=(1,1,1), mode='sphere', scale_factor=0.2)

		axes=np.array([
			[2.,0.,0.,0.],
			[0.,2.,0.,0.],
			[0.,0.,2.,0.],
		],dtype=np.float64)
		fov=np.array([  ##<todo> : now is 45 deg. use actual setting later ...
			[20., 20., 0.,0.],
			[20.,-20., 0.,0.],
		],dtype=np.float64)


		mlab.plot3d([0, axes[0,0]], [0, axes[0,1]], [0, axes[0,2]], color=(1,0,0), tube_radius=None, figure=fig)
		mlab.plot3d([0, axes[1,0]], [0, axes[1,1]], [0, axes[1,2]], color=(0,1,0), tube_radius=None, figure=fig)
		mlab.plot3d([0, axes[2,0]], [0, axes[2,1]], [0, axes[2,2]], color=(0,0,1), tube_radius=None, figure=fig)
		mlab.plot3d([0, fov[0,0]], [0, fov[0,1]], [0, fov[0,2]], color=(1,1,1), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([0, fov[1,0]], [0, fov[1,1]], [0, fov[1,2]], color=(1,1,1), tube_radius=None, line_width=1, figure=fig)

	#draw top_image feature area
	if is_top_region:
		x1 = cfg.xrange[0]
		x2 = cfg.xrange[1]
		y1 = cfg.xrange[0]
		y2 = cfg.xrange[1]
		mlab.plot3d([x1, x1], [y1, y2], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([x2, x2], [y1, y2], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([x1, x2], [y1, y1], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([x1, x2], [y2, y2], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)

	mlab.orientation_axes()
	mlab.view(azimuth=180,elevation=None,distance=50,focalpoint=[ 12.0909996 , -1.04700089, -2.03249991])#2.0909996 , -1.04700089, -2.03249991

	return fig

def draw_voxel(voxel_coords, lidar, is_grid=False, is_axis = True, is_top_region=True, fig=None):

	pxs=voxel_coords[:,0]
	pys=voxel_coords[:,1]
	pzs=voxel_coords[:,2]
	#prs=lidar[:,3]
	#prs=prs[:pzs.shape[0],]

	if fig is None: fig = mlab.figure(figure=None, bgcolor=(0,0,0), fgcolor=None, engine=None, size=(10000, 50000))

	mlab.points3d(
		pxs, pys, pzs, #prs,
		mode="cube",  # 'point'  'sphere'
		colormap='cool',  #'bone',  #'spectral',  #'copper',
		scale_factor=1,
		figure=fig)

	#draw grid
	# if is_grid:
	# 	mlab.points3d(0, 0, 0, color=(1,1,1), mode='sphere', scale_factor=0.2)

	# 	for y in np.arange(-50,50,1):
	# 		x1,y1,z1 = -50, y, 0
	# 		x2,y2,z2 =  50, y, 0
	# 		mlab.plot3d([x1, x2], [y1, y2], [z1,z2], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)

	# 	for x in np.arange(-50,50,1):
	# 		x1,y1,z1 = x,-50, 0
	# 		x2,y2,z2 = x, 50, 0
	# 		mlab.plot3d([x1, x2], [y1, y2], [z1,z2], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)

	# #draw axis
	# if is_grid:
	# 	mlab.points3d(0, 0, 0, color=(1,1,1), mode='sphere', scale_factor=0.2)

	# 	axes=np.array([
	# 		[2.,0.,0.,0.],
	# 		[0.,2.,0.,0.],
	# 		[0.,0.,2.,0.],
	# 	],dtype=np.float64)
	# 	fov=np.array([  ##<todo> : now is 45 deg. use actual setting later ...
	# 		[20., 20., 0.,0.],
	# 		[20.,-20., 0.,0.],
	# 	],dtype=np.float64)


	# 	mlab.plot3d([0, axes[0,0]], [0, axes[0,1]], [0, axes[0,2]], color=(1,0,0), tube_radius=None, figure=fig)
	# 	mlab.plot3d([0, axes[1,0]], [0, axes[1,1]], [0, axes[1,2]], color=(0,1,0), tube_radius=None, figure=fig)
	# 	mlab.plot3d([0, axes[2,0]], [0, axes[2,1]], [0, axes[2,2]], color=(0,0,1), tube_radius=None, figure=fig)
	# 	mlab.plot3d([0, fov[0,0]], [0, fov[0,1]], [0, fov[0,2]], color=(1,1,1), tube_radius=None, line_width=1, figure=fig)
	# 	mlab.plot3d([0, fov[1,0]], [0, fov[1,1]], [0, fov[1,2]], color=(1,1,1), tube_radius=None, line_width=1, figure=fig)

	#draw top_image feature area
	if is_top_region:
		x1 = cfg.xrange[0]
		x2 = cfg.xrange[1]
		y1 = cfg.xrange[0]
		y2 = cfg.xrange[1]
		mlab.plot3d([x1, x1], [y1, y2], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([x2, x2], [y1, y2], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([x1, x2], [y1, y1], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)
		mlab.plot3d([x1, x2], [y2, y2], [0,0], color=(0.5,0.5,0.5), tube_radius=None, line_width=1, figure=fig)

	mlab.orientation_axes()
	mlab.view(azimuth=180,elevation=None,distance=50,focalpoint=[ 12.0909996 , -1.04700089, -2.03249991])#2.0909996 , -1.04700089, -2.03249991

	return fig

def preprocess(lidar):
	T=35

	# voxel size
	vd = 0.02
	vh = 0.02
	vw = 0.02

	# points cloud range
	x_range = (-0.05, 3)
	y_range = (-0.01, 5.5)
	z_range = (0.1, 5.5)
	W = math.ceil((x_range[1] - x_range[0]) / vw)
	H = math.ceil((y_range[1] - y_range[0]) / vh)
	D = math.ceil((z_range[1] - z_range[0]) / vd)
	print(W, H, D)
	# shuffling the points
	#snp.random.shuffle(lidar)

	voxel_coords = ((lidar[:, :] - np.array([x_range[0], y_range[0], z_range[0]])) / (
					vw, vh, vd)).astype(np.int32)

	# convert to  (D, H, W)
	voxel_coords = voxel_coords[:,[2,1,0]]
	voxel_coords, inv_ind, voxel_counts = np.unique(voxel_coords, axis=0, \
											  return_inverse=True, return_counts=True)
	#print(voxel_coords, len(inv_ind), len(voxel_counts))
	voxel_features = []

	for i in range(len(voxel_coords)):
		voxel = np.zeros((T, 6), dtype=np.float32)
		pts = lidar[inv_ind == i]
		if voxel_counts[i] > T:
			pts = pts[:T, :]
			voxel_counts[i] = T
		# augment the points
		voxel[:pts.shape[0], :] = np.concatenate((pts, pts[:, :3] - np.mean(pts[:, :3], 0)), axis=1)
		voxel_features.append(voxel)
	return np.array(voxel_features), voxel_coords


def test():
	import os
	import glob
	import matplotlib.pyplot as plt

	data_path = os.path.join('data/')
	data_file = data_path + 'house2-1.txt'
	print("Processing: ", data_file)
	data = []
	with open(data_file) as f:
		for line in f:
			line = line.rstrip()
			points = line.split(" ")
			for i in range(0,3):
				points[i]=float(points[i])
			points = np.array(points)
			data.append(points)
	#lidar = np.fromfile(data, dtype=np.float32)
	data = np.array(data)
	data = data.reshape((-1, 3))
	print('x_min', min(data[:,0]))
	print('y_min', min(data[:,1]))
	print('z_min', min(data[:,2]))
	print('x_max', max(data[:,0]))
	print('y_max', max(data[:,1]))
	print('z_max', max(data[:,2]))
	lidar_features, voxel_coords = preprocess(data)
	fig = draw_lidar(data, is_grid=False, is_top_region=True)
	mlab.show()
	print(lidar_features.shape)
	print(voxel_coords.shape)
	fig = draw_voxel(voxel_coords, data)
	mlab.show()
	

if __name__ == '__main__':
	test()
