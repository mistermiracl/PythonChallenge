import sys
import math


#CONSTANT DECLARATION
PRISONER = 'Prisoner'
CITIZEN = 'Citizen'

X = 0
Y = 1

#FUNCTION USED TO FIND DISTANCE BETWEEN 2 POINTS
def distance(point1, point2):
    return math.sqrt((point1[X] - point2[X]) ** 2 + (point1[Y] - point2[Y]) ** 2)

#FUNCTION USED TO CHECK WETHER A POINT IS BETWEEN 2 OTHERS
def is_between(point, a, b):
    rel_tol = 1e-09
    abs_tol = 0.0

    dist_1 = distance(a, point) + distance(point, b)
    dist_2 = distance(a, b)

    #ABS AND MAX TO COMPARE FLOATS
    return abs(dist_1 - dist_2) <= max(rel_tol * max(abs(dist_1), abs(dist_2)), abs_tol)

#CHECK WETHER THE POINT IS IN THE BORDER OF THE POLYGON OR NOT
def point_on_border(point, poly):
    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[-n+i+1]
        if is_between(point, p1, p2):
            return True
    return False

#FUNCTION USE IN is_in_polygon FUNCTION
def angle_2d(x1, y1, x2, y2):
    theta1 = math.atan2(y1, x1)
    theta2 = math.atan2(y2, x2)
    dtheta = theta2 - theta1

    two_pi = math.pi + math.pi
    while dtheta > math.pi:
        dtheta -= two_pi
    while dtheta < -math.pi:
        dtheta += two_pi
    
    return dtheta

#CHECK WETHER POINT IS INSIDE POLYGON, WHERE POLYGON IS A LIST OR TUPLE OF POINTS
def is_in_polygon(polygon, point):
    
    angle = 0
    n = polygon.__len__()
    p1 = [0, 0]
    p2 = [0, 0]

    for i in range(0, n):
        p1[X] = polygon[i][X] - point[X]
        p1[Y] = polygon[i][Y] - point[Y]
        p2[X] = polygon[(i + 1) % n][X] - point[X]
        p2[Y] = polygon[(i + 1) % n][Y] - point[Y]
        
        angle += angle_2d(p1[X], p1[Y], p2[X], p2[Y])
    
    if abs(angle) < math.pi:
        return False
    else:
        return True

#MAIN FUNCTION THAT PARSES THE PEOPLE.TXT AND PRINTS THE RESULTS, TAKES FILEPATH AS ARGUMENT
def challenge(filePath):
    
    #LIST CONTAINING PARSED COORDINATES
    coords = []

    try:
        txt = open(filePath, 'r')
        lines = txt.readlines()

        #TXT PARSING
        for line in lines:
            coor = line.strip().split(',')
            
            item = []
    
            for i in range(0, coor.__len__() - 1):
                item.append(tuple(coor[i].strip().split(' ')))
            
            item.append(tuple(coor[coor.__len__() - 1].strip().split('|')[X].strip().split(' ')))
            item.append(tuple(coor[coor.__len__() - 1].strip().split('|')[Y].strip().split(' ')))
            coords.append(item)

        coords = list(map(lambda arr: list(map(lambda inner_arr: tuple(map(float, inner_arr)), arr)), coords))

    #REALEASE RESOURCES
    finally:
        if txt:
            txt.close()

    #FIND MAX VALUES AND MIN VALUES FIRST
    for inner_arr in coords:

        minX = inner_arr[0][X]
        maxX = inner_arr[0][X]
        minY = inner_arr[0][Y]
        maxY = inner_arr[0][Y]

        person = inner_arr[inner_arr.__len__() - 1]
        polygon = inner_arr[0:inner_arr.__len__() - 1]#NON INCLUSIVE AS WELL

        #START FROM 1 SINCE 0 IS BEEN TAKEN AS THE BASE ABOVE
        for i in range(1, inner_arr.__len__() - 1):#NON INCLUSIVE
            point = inner_arr[i]
            minX = min(minX, point[X])
            maxX = max(maxX, point[X])
            minY = min(minY, point[Y])
            maxY = max(maxY, point[Y])
        
        #DISCARD IF IT IS OUT OF BOUNDS
        if person[X] < minX or person[X] > maxX or person[Y] < minY or person[Y] > maxY:
            pass
            
        else:

            #ELSE CHECK WETHER IT IS IN POLYGON OR NOT
            if is_in_polygon(polygon, person):
                print(PRISONER)

            #IF THE FUNCTION RETURNS FALSE IT CAN STILL BE INSIDE BUT ON THE POLYGON EDGES,
            #SO WE MAKE SURE BY RUNNING THE point_on_border FUNCTION
            else:
                #NOW WE ARE SURE IT IS A PRISONER
                if point_on_border(person, polygon):
                    print(PRISONER)
                #NOW WE ARE SURE IT IS A CITIZEN
                else:
                    print(CITIZEN)


challenge(sys.argv[1])
