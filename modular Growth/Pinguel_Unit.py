import rhinoscriptsyntax as rs


def four_units(origin):
    
    origin = (0, 0, 0)
    origin_exterior_box = (0,-3.33333,0)
    box = rs.AddRectangle(origin, 5, 5)
    
    points = rs.DivideCurve(box, 12,True)
    
    move_point = points[7]
    
    vector = rs.VectorCreate(move_point, origin)
    
    box_2 = rs.CopyObject(box, vector)
    
    points2 = rs.DivideCurve(box_2, 12,True)
    
    move_point2 = points2[4]
    
    #rs.AddPoint(points[9])
    #rs.AddPoint(move_point2)
    
    vector2 = rs.VectorCreate(move_point2, points2[9])
    
    box_3 = rs.CopyObject(box_2, vector2)
    
    points3 = rs.DivideCurve(box_3, 12, True)
    
    move_point3 = points3[1]
    
    vector3 = rs.VectorCreate(move_point3, points3[6])
    
    box_4 = rs.CopyObject(box_3, vector3)
    points4 = rs.DivideCurve(box_4, 12, True)
    exterior_box = rs.AddRectangle(origin_exterior_box, 13.33, 13.33)
    points_exterior = rs.DivideCurve(exterior_box, 16, True)




def multiple_units ():
    origin = (0, 0, 0)
    origin_exterior_box = (0,-3.33333,0)
    initial_unit= four_units((0,0,0))
    points = rs.DivideCurve(origin_exterior_box, 12,True)
    move_point = points[7]
    vector = rs.VectorCreate(move_point, origin)
    unit_2 = rs.CopyObject(initial_unit, vector)

multiple_units ()