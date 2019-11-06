#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def Bresenham3D(first_point, second_point):
    first_point_x = first_point[0]
    first_point_y = first_point[1]
    first_point_z = first_point[2]
    second_point_x = second_point[0]
    second_point_y = second_point[1]
    second_point_z = second_point[2]
    
    FinalPoints = []
    FinalPoints.append((first_point_x, first_point_y, first_point_z))
    
    slope_x = abs(second_point_x - first_point_x)
    slope_y = abs(second_point_y - first_point_y)
    slope_z = abs(second_point_z - first_point_z)
    
    if (second_point_x > first_point_x):
        delta_x = 1
    else:
        delta_x = -1
    if (second_point_y > first_point_y):
        delta_y = 1
    else:
        delta_y = -1
    if (second_point_z > first_point_z):
        delta_z = 1
    else:
        delta_z = -1

    if (slope_x >= slope_y and slope_x >= slope_z):
        error_1 = 2 * slope_y - slope_x
        error_2 = 2 * slope_z - slope_x
        while (first_point_x != second_point_x):
            first_point_x += delta_x
            if (error_1 >= 0):
                first_point_y += delta_y
                error_1 -= 2 * slope_x
            if (error_2 >= 0):
                first_point_z += delta_z 
                error_2 -= 2 * slope_x 
            error_1 += 2 * slope_y 
            error_2 += 2 * slope_z 
            FinalPoints.append([first_point_x, first_point_y, first_point_z]) 

    elif (slope_y >= slope_x and slope_y >= slope_z):        
        error_1 = 2 * slope_x - slope_y 
        error_2 = 2 * slope_z - slope_y 
        while (first_point_y != second_point_y): 
            first_point_y += delta_y 
            if (error_1 >= 0): 
                first_point_x += delta_x 
                error_1 -= 2 * slope_y 
            if (error_2 >= 0): 
                first_point_z += delta_z 
                error_2 -= 2 * slope_y 
            error_1 += 2 * slope_x 
            error_2 += 2 * slope_z 
            FinalPoints.append([first_point_x, first_point_y, first_point_z]) 

    else:         
        error_1 = 2 * slope_y - slope_z 
        error_2 = 2 * slope_x - slope_z 
        while (first_point_z != second_point_z): 
            first_point_z += delta_z 
            if (error_1 >= 0): 
                first_point_y += delta_y 
                error_1 -= 2 * slope_z 
            if (error_2 >= 0): 
                first_point_x += delta_x 
                error_2 -= 2 * slope_z 
            error_1 += 2 * slope_y 
            error_2 += 2 * slope_x
            FinalPoints.append([first_point_x, first_point_y, first_point_z]) 
    
    return FinalPoints

