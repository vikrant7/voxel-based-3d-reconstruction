import numpy as np

filename = "foo.npy"

voxel_grid = np.load(filename)

x_size, y_size, z_size = voxel_grid.shape
points = np.empty((0,3), float)
voxel_grid[2][2][2] = 1
voxel_size = 2
x_min = -71.036
y_min = -21.105
z_min = -5.16
for i in range(x_size):
	for j in range(y_size):
		for k in range(z_size):
			if voxel_grid[i][j][k] == 1:
				x = (voxel_size * i) + x_min
				y = (voxel_size * j) + y_min
				z = (voxel_size * k) + z_min
				# index = index + 1
				point = [[x, y, z]]
				points = np.r_[points, point]
print(points.shape)
# Save the numpy array for visualization
np.save("voxel", points)