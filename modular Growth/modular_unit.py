import rhinoscriptsyntax as rs
from random import uniform
from random import randint
import math
import Rhino
import random 
#libraries
import viewport_tools as vt
import center_cube as cc


def center_cube(center, radius):
    cx, cy, cz = center
    
    #lower 4 points
    p1 = (cx - radius, cy - radius, cz - radius)
    p2 = (cx + radius, cy - radius, cz - radius)
    p3 = (cx + radius, cy + radius, cz - radius)
    p4 = (cx - radius, cy + radius, cz - radius)
    
    #upper 4 points
    p5 = (cx - radius, cy - radius, cz + radius)
    p6 = (cx + radius, cy - radius, cz + radius)
    p7 = (cx + radius, cy + radius, cz + radius)
    p8 = (cx - radius, cy + radius, cz + radius)
    
    points = [p1, p2, p3, p4, p5, p6, p7, p8]
    
    cube = rs.AddBox(points)
    return(cube)






def modular_unit(x_n, y_n, z_n, center=None):
    if center is None:
        cx = (x_n - 1) * 16
        cy = (y_n - 1) * 16
        cz = (z_n - 1) * 16
        center = (cx, cy, cz)

    points = []
    center_box = None
    for i in range(x_n):
        for j in range(y_n):
            for p in range(z_n):
                x, y, z = center[0] + (i - (x_n-1)/2)*32, center[1] + (j - (y_n-1)/2)*32, center[2] + (p - (z_n-1)/2)*32
                point = rs.AddPoint(x, y, z)
                if i == x_n//2 and j == y_n//2 and p == z_n//2:
                    center_box = center_cube((x, y, z), 16)
                else:
                    box = center_cube((x, y, z), 16)
                points.append(point)
    if center_box:
        rs.DeleteObject(center_box)
    return points




def multiple_units(x_n, y_n, z_n):
    start_point = rs.GetPoint("Select start point:")
    points = []
    for i in range(x_n):
        for j in range(y_n):
            for p in range(z_n):
                x, y, z = start_point[0] + i*96, start_point[1] + j*96, start_point[2] + p*64
                point = rs.AddPoint(x, y, z)
                modular_unit(3, 3, 1, center=(x, y, z))
                points.append(point)
    return points

def cull_with_brep(points, breps):
    new_points = []
    for i in points:
        point = rs.AddPoint(i)
        new_points.append(point)
        new_point = rs.coerce3dpoint(point)
        for brep in breps:
            brep_object = rs.coercebrep(brep)
            if brep_object.IsPointInside(new_point, .01, True) == True:
                rs.DeleteObject(point)
    return(new_points)

def random_spheres(points, radius, number):
    spheres = []
    for i in range(number):
        max = len(points) - 1
        index = random.randint(0,max)
        sphere = rs.AddSphere(points[index], radius)
        spheres.append(sphere)
    return spheres
    
points = multiple_units(3, 3, 3)

