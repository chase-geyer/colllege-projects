"""
Code to calculate the circle that passes through three given points.

Fill in each function with your code (including fixing the return
statement).
"""

import math
import comp140_module1 as circles
import random
def distance(point0x, point0y, point1x, point1y):
    """
    Computes the distance between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the distance between the two points
    """
    dist = ((point1x-point0x)**2 + (point1y - point0y)**2)**0.5
    print(dist)
    return dist

def midpoint(point0x, point0y, point1x, point1y):
    """
    Computes the midpoint between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the midpoint
    """
    mid_x = point0x + (point1x - point0x)/2
    mid_y = point0y + (point1y - point0y)/2
    print(mid_x, mid_y)
    return mid_x, mid_y

def slope(point0x, point0y, point1x, point1y):
    """
    Computes the slope of the line that connects two given points.

    The x-values of the two points, point0x and poin1x, must be different.

    inputs:
        -point0x: a float representing the x-coordinate of the first point.
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point.
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the slope between the points
    """
    slope_between = (point1y - point0y)/(point1x - point0x)
    print(slope_between)
    return slope_between

def perp(lineslope):
    """
    Computes the slope of a line perpendicular to a given slope.

    input:
        -lineslope: a float representing the slope of a line.
                    Must be non-zero

    returns: a float that is the perpendicular slope
    """
    inverse_slope = -1/lineslope
    print(inverse_slope)
    return inverse_slope

def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Computes the intersection point of two lines.

    The two slopes, slope0 and slope1, must be different.

    inputs:
        -slope0: a float representing the slope of the first line.
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -slope1: a float representing the slope of the second line.
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the intersection
    point
    """
    x_val = ((point0y-point1y) - slope0*point0x + slope1 * point1x)/(slope1 - slope0)
    y_val = point1y + slope1*(x_val - point1x)
    print(x_val, y_val)
    return x_val, y_val

def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Computes the center and radius of a circle that passes through
    thre given points.

    The points must not be co-linear and no two points can have the
    same x or y values.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point
        -point2x: a float representing the x-coordinate of the third point
        -point2y: a float representing the y-coordinate of the third point

    returns: three floats that are the x- and y-coordinates of the center
    and the radius
    """
    mid0x, mid0y = midpoint(point0x, point0y, point1x, point1y)
    mid1x, mid1y = midpoint(point2x, point2y, point1x, point1y)
    slope0 = perp(slope(point0x, point0y, point1x, point1y))
    slope1 = perp(slope(point2x, point2y, point1x, point1y))
    center_x_val, center_y_val = (intersect(slope0, mid0x, mid0y, slope1, mid1x, mid1y))
    radius = distance(center_x_val, center_y_val, point0x, point0y)
    return center_x_val, center_y_val, radius

# Run GUI - uncomment the line below after you have
#           implemented make_circle
circles.start(make_circle)
