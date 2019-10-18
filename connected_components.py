import numpy as np
import queue

"""
The code finds the NFC and NBC parameters for a voxel background
"""

def num_connected_components(voxel_neighbourhood, is_foreground, size):
	# Assume that each voxel has data associated with it and it is 1 for foregraound voxel
	# and 0 for background voxel
	num = 0
	if is_foreground:
		connectivity = 18
		# Set central voxel to background voxel
		central_index = int((size - 1) / 2)
		voxel_neighbourhood[central_index][central_index][central_index] = 0
		# Get relevent neighbourhood
		relevent_neighbourhood = []
		for i in range(size):
			for j in range(size):
				for k in range(size):
					if voxel_neighbourhood[i][j][k] == 1:
						relevent_neighbourhood.append([i, j, k])

	else : 
		connectivity = 6
		for i in range(size):
			for j in range(size):
				for k in range(size):
					if voxel_neighbourhood[i][j][k] == 0:
						relevent_neighbourhood.append([i, j, k])

	# Get initial object voxel
	while len(relevent_neighbourhood)!=0:
		object_voxel = relevent_neighbourhood[0]
		connected_component = get_connected_components(relevent_neighbourhood, object_voxel, connectivity)
		# remove connected componnets from relevent neighbourhood
		num += 1
		relevent_neighbourhood = [x for x in relevent_neighbourhood if x not in connected_component]

	return num

def get_connected_components(neighbourhood, object_voxel, connectivity):
	# voxel_neighbourhood list of array of coordinates
	# of voxels under consideraton 
	result = []
	result.append(object_voxel)
	visited = []
	num_voxels = len(neighbourhood)
	# Setting visited flag for each voxel
	for voxel in neighbourhood:
		if voxel == object_voxel:
			visited.append(1)
		else:
			visited.append(0)

	Q = queue.Queue(maxsize=num_voxels)
	Q.put(object_voxel)

	while not Q.empty():
		x = Q.get()
		for i in range(num_voxels):
			voxel = neighbourhood[i]
			if is_connected(x, voxel, connectivity) and not visited[i]:
				result.append(voxel)
				visited[i] = 1
				Q.put(voxel)

	return result

def is_connected(x, voxel, connectivity):
	connected = False
	if connectivity == 18:
		out = np.asarray(x) - np.asarray(voxel)
		if 0 in out:
			connected = True
	elif connectivity == 6:
		out = np.asarray(x) - np.asarray(voxel)
		num_zeros = 0
		for element in out:
			if element == 0:
				num_zeros += 1
		if num_zeros >=2:
			connected = True

	return connected

if __name__ == '__main__':
	x = np.ones((3,3,3))
	num = num_connected_components(x, is_foreground=1, size=3)
	print(num)