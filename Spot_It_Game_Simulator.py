"""
Code to implement the game of Spot it!

http://www.blueorangegames.com/spotit/
"""

import comp140_module2 as spotit

def equivalent(point1, point2, mod):
    """
    Determines if the two given points are equivalent in the projective
    geometric space in the finite field with the given modulus.

    Each input point, point1 and point2, must be valid within the
    finite field with the given modulus.

    inputs:
        - point1: a tuple of 3 integers representing the first point
        - point2: a tuple of 3 integers representing the second point
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the points are equivalent
    """
    #calculating the first point of the resulting cross product
    val1 = point1[1]*point2[2] - point1[2] * point2[1]
    
    #calculating the second point of the resulting cross product
    val2 = point1[2] * point2[0] - point1[0] * point2[2]
    
    #calculating the third point of the resulting cross product
    val3 = point1[0] * point2[1] - point1[1] * point2[0]
    
    #Checking whether the two points are equivalent; if they are, 
    #every value should equal 0, which would return true in this situation
    return val1 % mod == 0 and val2 % mod == 0 and val3 % mod == 0
    
def incident(point, line, mod):
    """
    Determines if a point lies on a line in the projective
    geometric space in the finite field with the given modulus.

    The inputs point and line must be valid within the finite field
    with the given modulus.

    inputs:
        - point: a tuple of 3 integers representing a point
        - line: a tuple of 3 integers representing a line
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the point lies on the line
    """
    #Calculates the dot product of the individual elements of the two points 
    #as indexed by the tuples
    dot_product = point[0]*line[0] + point[1]*line[1] + point[2]*line[2]
    
    #print(dot_product % mod == 0)
    return dot_product % mod == 0

def generate_all_points(mod):
    """
    Generate all unique points in the projective geometric space in
    the finite field with the given modulus.

    inputs:
        - mod: an integer representing the modulus

    Returns: a list of unique points, each is a tuple of 3 elements
    """
    
    list_of_points = []
    #Generating points so there will be a difference sequence
    #in every tuple
    for element1 in range(0, mod):
        for element2 in range(0, mod):
            for element3 in range(0, mod):
                if (element1, element2, element3) not in list_of_points:
                    list_of_points.append((element1, element2, element3))
    #Taking out the one point that is not in any plane (the center)
    list_of_points.remove((0, 0, 0))
    #allows me to check against my final, unique list of points
    #print(len(list_of_points))
    #print(list_of_points)
    #setting the starting values to allow me to check my list for any duplicate points
    #using the criteria set by the equivalent function
    anchor_value = 0
    moving_value = 1
    #setting an anchor point and iterating through every other point in the list,
    #finding all equivalent points in the list and removing them. I iterated back an index
    #every time I removed a point, as I would have missed the point immediately adjacent to 
    #the removed point otherwise.
    
    while anchor_value < len(list_of_points) - 1:
        #print(anchor_value)
        moving_value = anchor_value + 1
        while moving_value < len(list_of_points):
            if equivalent(list_of_points[anchor_value], list_of_points[moving_value], mod):
                list_of_points.pop(moving_value)
                moving_value -= 1
            moving_value += 1
        anchor_value += 1
    #printing out the list and the length, making sure that 
    #I didn't accidentally remove too many points
    #print(list_of_points, len(list_of_points))
    
    return list_of_points
#generate_all_points(2)
def create_cards(points, lines, mod):
    """
    Create a list of unique cards.

    Each point and line within the inputs, points and lines, must be
    valid within the finite field with the given modulus.

    inputs:
        - points: a list of unique points, each represented as a tuple of 3 integers
        - lines: a list of unique lines, each represented as a tuple of 3 integers
        - mod: an integer representing the modulus

    returns: a list of lists of integers, where each nested list represents a card.
    """
    deck = []
    card = []
    #checking each line with each point
    for line_index in range(0, len(lines)):
        for point_index in range(0, len(points)):
            #if point along line, store index
            if incident(points[point_index], lines[line_index], mod):
                card.append(point_index)
            #if the card is already full of points, make a new one
            if len(card) == mod + 1:
                deck.append(card)
                card = []
    #print(len(deck), deck)
    return deck

def run():
    """
    Create the deck and play the game.
    """
    # Prime modulus
    # Set to 2 or 3 during development
    # Set to 7 for the actual game
    modulus = 2

    # Generate all unique points for the given modulus
    points = generate_all_points(modulus)

    # Lines are the same as points, so make a copy
    lines = points[:]

    # Generate a deck of cards given the points and lines
    deck = create_cards(points, lines, modulus)

    # Run GUI - uncomment the line below after you have implemented
    #           everything and you can play your game.  The GUI does
    #           not work if the modulus is larger than 7.

    spotit.start(deck)

run()
