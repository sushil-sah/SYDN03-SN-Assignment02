import turtle

# Function that draw the edges of the desired polygon based on length and depth
def draw_edge(length, depth):
    # To draw the straight line that has depth as 0
    if depth == 0:
        # draw the line which is equal to the lenth provided by user
        turtle.forward(length)
    else:
        # Dividing the length into three sengments to scale the shape properly
        segment = length / 3
        # Calling the function and dividing the segement into 3 smaller segments recursively until the depth reaches 0 and draws a line
        draw_edge(segment, depth - 1)
        # Moving the pen right for inward indentation
        turtle.right(60)
        # Calling the function and dividing the segement into 3 smaller segments recursively until the depth reaches 0 and draws a line
        draw_edge(segment, depth - 1)
        # Move the pen in anticlock wise direction to move the pen in upward direction
        turtle.left(120)
        # Calling the function and dividing the segement into 3 smaller segments recursively until the depth reaches 0 and draws a line
        draw_edge(segment, depth - 1)
        # Moving the pen right in clockwise direction
        turtle.right(60)
        # Calling the function and dividing the segement into 3 smaller segments recursively until the depth reaches 0 and draws a line
        draw_edge(segment, depth - 1)


def draw_polygon(sides, length, depth):
    """Draws the initial polygon with fractal edges."""
    # Determing the angles the cursor should go left or right
    angle = 360 / sides
    # creating a loop so that we can draw every sides 
    for i in range(sides):
        # Calling a function to draw the edges
        draw_edge(length, depth)
        # Moving the turtle to the right by the angle determined by side provided to draw new sides
        turtle.right(angle)

def main():
    # Get the sides, length and depth values from the user
    sides = int(input("Enter the number of sides: "))
    length = int(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    # Start setting up the turtle 
    # Setting the turtle spped to 0 which is the fastest turtle speed
    turtle.speed(0)
    # Hide the turtle pen to make the drawing process more clear
    turtle.hideturtle()
    # Moving the pen up from the drawing sheets to move the pen to another location without leaving any trace of the pen 
    turtle.penup()
    # Center the drawing in the sheet to make drawing more representable
    turtle.goto(-length/2, length/2)
    # Put the pen down on the sheet to start drawing of the shape
    turtle.pendown()

    # Calling a function to start draawing the shape
    draw_polygon(sides, length, depth)
    # Preventing the output sheet from closing
    turtle.done()

if __name__ == "__main__":
    main()