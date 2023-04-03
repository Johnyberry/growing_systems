import rhinoscriptsyntax as rs


point = rs.AddPoint(5,5,5)

    
x, y, z = rs.PointCoordinates(point)

print(x, y, z)