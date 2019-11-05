import numpy as np
from connected_components import num_connected_components
import os
import math

def distance(point1, point2):
	return math.sqrt((point1[0]-point2[0])**2+ (point1[1]-point2[1])**2+ (point1[2]-point2[2])**2) 

def Bresenham3D(start, end):#, pg_voxel_index):
	x1 = start[0]
	y1 = start[1]
	z1 = start[2]
	x2 = end[0]
	y2 = end[1]
	z2 = end[2]
	ListOfPoints = []
	ListOfPoints.append((x1, y1, z1))
	dx = abs(x2 - x1)
	dy = abs(y2 - y1)
	dz = abs(z2 - z1)
	if (x2 > x1):
		xs = 1
	else:
		xs = -1
	if (y2 > y1):
		ys = 1
	else:
		ys = -1
	if (z2 > z1):
		zs = 1
	else:
		zs = -1

	# Driving axis is X-axis" 
	if (dx >= dy and dx >= dz):
		p1 = 2 * dy - dx
		p2 = 2 * dz - dx
		while (x1 != x2):
			x1 += xs
			if (p1 >= 0):
				y1 += ys
				p1 -= 2 * dx
			if (p2 >= 0):
				z1 += zs 
				p2 -= 2 * dx 
			p1 += 2 * dy 
			p2 += 2 * dz 
			ListOfPoints.append([x1, y1, z1]) 
  
	# Driving axis is Y-axis" 
	elif (dy >= dx and dy >= dz):        
		p1 = 2 * dx - dy 
		p2 = 2 * dz - dy 
		while (y1 != y2): 
			y1 += ys 
			if (p1 >= 0): 
				x1 += xs 
				p1 -= 2 * dy 
			if (p2 >= 0): 
				z1 += zs 
				p2 -= 2 * dy 
			p1 += 2 * dx 
			p2 += 2 * dz 
			ListOfPoints.append([x1, y1, z1]) 
  
	# Driving axis is Z-axis" 
	else:         
		p1 = 2 * dy - dz 
		p2 = 2 * dx - dz 
		while (z1 != z2): 
			z1 += zs 
			if (p1 >= 0): 
				y1 += ys 
				p1 -= 2 * dz 
			if (p2 >= 0): 
				x1 += xs 
				p2 -= 2 * dz 
			p1 += 2 * dy 
			p2 += 2 * dx
			ListOfPoints.append([x1, y1, z1]) 
	return ListOfPoints

def validation(start, end):
	return True


# dataset is implemented in form of numpy array. Different values determine determine types of voxel - p, g or background
# 1 = p voxel,  0 = background voxel, 2 = g-voxel
# data = pointcloud data imported. shape(data) = [N, 3] (N=number of points) (3 is the dimensions) (x, y, z)

# voxels are considered to be square of side = 'voxel_size'

data_path = os.path.join('data/')
data_file = data_path + 'house2-2.txt'
#	data_file = "voxel.npy"
print("Importing data  from file: " + data_file)
data = []
with open(data_file) as f:
	for line in f:
		line = line.rstrip()
		points = line.split(" ")
		for i in range(0,3):
			points[i]=float(points[i])
		points = np.array(points)
		data.append(points)
data = np.array(data)
data = data.reshape((-1, 3))
data = 30*data[:,:3]
voxel_size = 1 #taken input from the user
L = 5 # largest size of hole to be filled -- taken input from the user

# bounding_box = [x, y, z] size in x y and z direction
#nx = number of voxels in x-direction
#ny = number of voxels in y-direction
#nz = number of voxels in z-direction

bounding_box = [0]*3 #initialise with 0 length

bounding_box[0] = int(max(data[:, 0]) - min(data[:, 0]))
bounding_box[1] = int(max(data[:, 1]) - min(data[:, 1]))
bounding_box[2] = int(max(data[:, 2]) - min(data[:, 2]))

nx = int(bounding_box[0]/voxel_size) + 1
ny = int(bounding_box[1]/voxel_size) + 1
nz = int(bounding_box[2]/voxel_size) + 1

print("Number of voxels created in x y and z: %d %d %d" %((nx+4), (nx+4), (nx+4)))

#padding layer should be considered as neighbourhood of 5x5 is considered
voxel = np.zeros([nx+4, ny+4, nz+4]) # 3D array with dimensions of nx + 4, ny + 4 and nz + 4 due to padding for corner points
voxel_index = [] #list of indeces of voxel elements which represents surface

#marking all the p-voxels, voxel elements with value 1 = p-voxel and 0 = background voxel
x_min = min(data[:, 0])
y_min = min(data[:, 1])
z_min = min(data[:, 2])
for i in range(len(data)):
	voxel_idx = int((data[i][0]-x_min)/voxel_size) + 2  # From 2(0) to nx+1(nx-1)
	voxel_idy = int((data[i][1]-y_min)/voxel_size) + 2  # From 2(0) to ny+1(ny-1)
	voxel_idz = int((data[i][2]-z_min)/voxel_size) + 2  # From 2(0) to nz+1(nz-1)
	if voxel[voxel_idx][voxel_idy][voxel_idz] != 1:
		voxel[voxel_idx][voxel_idy][voxel_idz] = 1
		voxel_index.append([voxel_idx, voxel_idy, voxel_idz])

# Gap fillig algorithm
# pg_voxel and b_voxel are voxels consisting of p,g-voxels and boundary voxels repectively
# both are initialized to p_voxels initially

pg_voxel = voxel
pg_voxel_index = voxel_index #list of indices of voxel elements which are p-voxels or g-voxels
b_voxel = voxel
b_voxel_index = voxel_index #list of indices of voxel elements which are boundary voxels
# value of -1 used to define boundary voxel and -2 for outermost boundary


# keep only boundary and remove others form b_voxel
print("Creating boundary and p-g voxelised representation")
i = 0
while(i<len(b_voxel_index)):
	x = b_voxel_index[i][0]
	y = b_voxel_index[i][1]
	z = b_voxel_index[i][2]
	#definition of NFC3, NBC3 and NBC5 remaining
	#checking conditions on pg_voxel
	# nfc3 = NFC3(pg_voxel[pg_voxel[x-1:x+2, y-1:y+2, z-1:z+2]])
	# nbc5 = NBC5(pg_voxel[pg_voxel[x-2:x+3, y-2:y+3, z-2:z+3]])
	nfc3 = num_connected_components(pg_voxel[x-1:x+2, y-1:y+2, z-1:z+2], is_foreground=1, size=3) # passing the neighbourhood of 3x3
	nbc5 = num_connected_components(pg_voxel[x-2:x+3, y-2:y+3, z-2:z+3], is_foreground=1, size=5) # passing the neighbourhood of 5x5
	
	if(nfc3>1 or nfc3==0):
		b_voxel[x][y][z] = -1 # mark as boundary voxel
	elif(nfc3 == 1 and nbc5 == 1):
		b_voxel[x][y][z] = -1 # mark as boundary voxel
	else:
		b_voxel[x][y][z] = 0  # mark as background voxel
		# print(len(b_voxel_index))
		b_voxel_index.remove(b_voxel_index[i]) # remove the index from the set of boundary indices
		i -= 1
	i += 1

#filling the holes with g-voxels
print("Inserting Points to fill gap.....Sit back and relax!!!...")
boundary_size = len(b_voxel_index)
for i in range(boundary_size):
	if(i%500 == 0):
		print("%.2f%% of the process complete..." %((i*100)/boundary_size))
	for j in range(i+1, boundary_size):
		if(distance(b_voxel_index[i], b_voxel_index[j])>L):
			continue
		listofpoints = Bresenham3D(b_voxel_index[i], b_voxel_index[j])#, pg_voxel_index)
		for idx in range(len(listofpoints)):
			if(listofpoints[idx] not in pg_voxel_index):
				#print("point inserted", i,j)
				pg_voxel_index.append(listofpoints[idx])
				b_voxel_index.append(listofpoints[idx])

for idx in range(len(pg_voxel_index)):
	if(pg_voxel[pg_voxel_index[idx][0]][pg_voxel_index[idx][1]][pg_voxel_index[idx][2]] != 1):
		pg_voxel[pg_voxel_index[idx][0]][pg_voxel_index[idx][1]][pg_voxel_index[idx][2]] = 1

x_size, y_size, z_size = pg_voxel.shape
points = np.empty((0,3), float)
voxel_size = 0.1
for i in range(x_size):
	for j in range(y_size):
		for k in range(z_size):
			if pg_voxel[i][j][k] == 1:
				x = (voxel_size * i) + x_min
				y = (voxel_size * j) + y_min
				z = (voxel_size * k) + z_min
				# index = index + 1
				point = [[x, y, z]]
				points = np.r_[points, point]
print("Number of final points: %d" %points.shape[0])
# Save the numpy array for visualization
print("Saving the points in .npy format...run voxel.py to visualise...")
np.save("voxel", points)