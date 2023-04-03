

import rhinoscriptsyntax as rs
from random import uniform
from random import randint
import math
import Rhino
import random 
#libraries
import viewport_tools as vt
import center_cube as cc

def random_color(object):
    red = uniform(0
    ,object)
    green = uniform(153 ,object)
    blue = uniform(51,object)
    opacity = 80
    
    
    color = rs.CreateColor(red,green,blue)
    return color
def assign_material_color(object, color):
    rs.AddMaterialToObject(object)
    index = rs.ObjectMaterialIndex (object)
    rs.MaterialColor(index, color)
    
def modular_unit(x_n, y_n z_n):
    
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
                    center_box = cc.center_cube((x, y, z), 16)
                else:
                    box = cc.center_cube((x, y, z), 16)
                points.append(point)
    if center_box:
        rs.DeleteObject(center_box)
    return points

def building_unit(center, height, radius):
    plane_1 = rs.WorldXYPlane()
    plane_2 = rs.MovePlane(plane_1, center)
    plane_3 = rs.MovePlane(plane_2, center)
    #rs.AddCone(plane_2, height, radius)
    x, y, z = rs.PointCoordinates(center)
    cube = cc.center_cube((x,y,z),radius)
    color = random_color(255)
    assign_material_color(cube, color)


def building_unit_sphere(center, height, radius):
    plane_1 = rs.WorldXYPlane()
    plane_2 = rs.MovePlane(plane_1, center)
    plane_3 = rs.MovePlane(plane_2, center)
    #rs.AddCone(plane_2, height, radius)
    x, y, z = rs.PointCoordinates(center)
    sphere = rs.AddSphere(center, radius)
    color = random_color(255)
    assign_material_color(sphere, color)


def polygon(center, edges, size, angle):
    tempCircle = rs.AddCircle(center, size)
    tempPoints = rs.DivideCurve(tempCircle, edges, create_points=False, return_points=True)
    tempPoints.append(tempPoints[0])
    tempHexago = rs.AddPolyline(tempPoints)
    tempReturn = rs.RotateObject(tempHexago, center, angle, axis=None, copy=False)
    rs.DeleteObject(tempCircle)
    return tempReturn

"""
def brain_link(HexCenter, edges ):

    userPt = HexCenter
    pt = rs.AddPoint(userPt)
    pts = []
    pts.append(pt)
        ##### ---- number of objects ---######
        ###########-----     ------#######

    while len(pts) <= 5:
        x = random.uniform(-3, 3.0)
        y = random.uniform(-3, 3.0)
        z = random.uniform(0.0, 5)
        vect = (x, y, z)
        newPt = rs.CopyObject(pts[-1],vect)
        distance = rs.Distance(newPt, pts[-1])
        if distance > 5:
            plane = rs.WorldXYPlane()
            new_plane = rs.MovePlane(plane, newPt)
            building_unit_sphere(newPt, y, z)
            #rs.InsertBlock("building", newPt)
            pts.append(newPt)
            print(len(pts))
            my_polyline = rs.AddPolyline(pts)
        else:
            rs.DeleteObject(newPt)
    return my_polyline
"""
###cube ###
def brain_link(HexCenter, edges ):

    userPt = HexCenter
    pt = rs.AddPoint(userPt)
    pts = []
    pts.append(pt)
        ##### ---- number of objects ---######
        ###########-----     ------#######

    while len(pts) <= 4:
        x = 10*random.uniform(0, 1.0)
        y = 10*random.uniform(0, 1.0)
        z = 10*random.uniform(0.0, 6)
        vect = (x, y, z)
        newPt = rs.CopyObject(pts[-1],vect)
        distance = rs.Distance(newPt, pts[-1])
        if distance > 16:
            plane = rs.WorldXYPlane()
            new_plane = rs.MovePlane(plane, newPt)
            building_unit(newPt, 16, 16)
            #rs.InsertBlock("building", newPt)
            pts.append(newPt)
            print(len(pts))
            my_polyline = rs.AddPolyline(pts)
        else:
            rs.DeleteObject(newPt)
    return my_polyline


def cull_with_brep(points, brep, boolean=False):
    brep_object = rs.coercebrep(brep)
    new_points = []
    for i in points:
        point = rs.AddPoint(i)
        new_point = rs.coerce3dpoint(point)
        if brep_object.IsPointInside(new_point, 0.1, False) == True:
            point = i
            new_points.append(i)

    return new_points


def Hex_grid( HexCenter, HexExtend, HexSize, HexAngle, edges, brep):
    rs.AddPoint(HexCenter)
    hexGrid = []
    formula = 2 * math.sqrt((HexSize * HexSize) - ((HexSize / 2) * (HexSize / 2)))

    for i in range(0, HexExtend):
        tempSize = formula * (i + 1)
        dut = polygon(HexCenter, edges, tempSize, 30 + HexAngle)
        temp = rs.DivideCurve(dut, (i+1) * edges, create_points=False, return_points=True)
        rs.DeleteObject(dut)
        hexGrid.extend(temp)
    points = []   
    for i in range(0, len(hexGrid)):
        polygon(hexGrid[i], edges, HexSize, HexAngle)
        point = rs.AddPoint(hexGrid[i])
        points.append(point)
        new_points = cull_with_brep(points, brep)
        #x, y, z = rs.PointCoordinates(point)
    for p in new_points:
        #brain_link(p,(edges/4))
        modular_unit(5, 5, 5)
        
        
        
        #cube = brain_link((x, y ,z), (edges/4))
        #sphere = rs.AddSphere(point, (edges/2))
        #color = random_color(255)
        #assign_material_color(cube, color)


        #cube = cc.center_cube((x, y ,z), (edges/4))





def polyobject():
    rs.EnableRedraw(True)
    # Prompt user to enter the number of vertices
    num_vertices = rs.RealBox("Enter the number of vertices between 3 and 5", None, "Count")
    vertices = []
    for i in range(int(num_vertices)):
        message = "Pick location for vertex {0}:".format(i+1)
        vertex = rs.GetPoint(message)
        if vertex is None:
            print("User cancelled the operation")
            return
        vertices.append(vertex)
        rs.AddPoint(vertex)
        rs.Redraw()
    vertices.append(vertices[0])
    rs.AddPolyline(vertices)
    rs.EnableRedraw(False)
    # select a curve to extrude
    curve = rs.GetObjects("Select curve to extrude", rs.filter.curve)
    # extrude the curve
    height = 10  # change the extrusion height
    rs.ExtrudeCurveStraight(curve, (0, 0, 0), (0, 0, height))





def image ():
    rs.EnableRedraw (False)
    view_name = "axo"
    vt.create_parallel_view("axo", (800, 800))
    vt.set_axon_view(90,0, view_name)
    rs.EnableRedraw (True)
    vt.zoom_scale (.75, view_name)
    vt.set_display_mode(view_name, "Rendered")
    image = rs.GetString("Save image as png?", "No", ["Yes", "No"])
    animation = rs.GetString("Save animation?", "No", ["Yes", "No"])
    if image == "Yes" :
        file_name = rs.GetString("Please Provide a file name.", "image")
        folder_name = file_name + "folder"
        resolution = rs.GetInteger ("Please provide a scalar for the image")
        for i in range (1): 
            rs.Sleep (1)
            vt.set_axon_view (1,0, view_name)
            animate_name = file_name + str("%04d"%i)
            vt.set_display_mode(view_name, "Rendered")
            vt.capture_view(resolution, animate_name, folder_name)
        vt.capture_view (resolution, file_name, folder_name)
        #vt.capture_view (2.0, file_name, "Modular Intelligence ")
    else:
        pass




def main():

    obj = rs.GetObject("Select an object to use its center point as the center of the hexagonal grid")
    HexCenter = rs.GetPoint()

    #HexCenter = rs.GetPoint("Specify center point")
    HexExtend = rs.GetInteger("Enter the number of radial levels", 2, 2)
    HexSize = rs.GetReal("Edge size of hexagons", 10.0)
    HexAngle = rs.GetReal("Rotation angle of hexagons", 45.0)
    edges = rs.GetReal("How many edges", 4)
    
    Hex_grid( HexCenter, HexExtend, HexSize, HexAngle, edges, obj)
    
    #rs.DeleteObject(brep)






#polyobject()
#rs.Sleep(0)

main()


