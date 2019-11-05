import numpy as np

def check_background(voxel, segment_voxel_list):
	"""
	voxel : 3d array having 0 at positions of background voxels
	voxel_list : list of index of voxels
	seg_voxel_list - list of vexels in line segment
	"""
	is_background = True
	l = len(segment_voxel_list)
	for i in range(1,l-1):
		# Not considering 1st and last voxel index
		voxel_index = segment_voxel_list[i]
		x = voxel_index[0]
		y = voxel_index[1]
		z = voxel_index[2]
		if voxel[x][y][z] == 0:
			# It is background 
			pass
		else:
			is_background = False
			break

	return is_background

def validation(voxel, voxel_list, segment_voxel_list):
	valid = False 
	# Check conditon for background voxels
	background_check = check_background(voxel, segment_voxel_list)
	boundary_check = check_boundary(voxel, voxel_list, segment_voxel_list)
	if background_check and boundary_check:
		valid = True

	return valid

def check_boundary(voxel, voxel_list, segment_voxel_list):
	# boundary voxels are marked as -1
	start_voxel = segment_voxel_list[0]
	x = start_voxel[0]
	y = start_voxel[1]
	z = start_voxel[2]
	assert voxel[x][y][z] == -1  # Should be boundary voxel
	# Add code to get boundary length
	
	


