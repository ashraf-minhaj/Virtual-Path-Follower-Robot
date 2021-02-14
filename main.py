"""
    ** Virtual Path Follower Robot **

    License: GPL3
    You should receive a copy of license with this program.

    (c) author: ashraf minhaj
        mail  : ashraf_minhaj@yahoo.com
    
    Written on 15th Feb 2021
"""

""" install - 
$ pip install pygame
"""

# import library
import pygame
import serial

# robot port and buadrate
# change these according to your need
PORT = "COM8"
BUADRATE = 9600

# initialize things
pygame.init()
robot = serial.Serial(PORT, BUADRATE)  # connect robot

# create window with size (our image size)
window = pygame.display.set_mode((700,400))  # track 1
#window = pygame.display.set_mode((1155,399))   # track 2

# load image file
bg  = pygame.image.load("track1.png")
#bg  = pygame.image.load("track2.png")
car = pygame.image.load("car.png")
car = pygame.transform.scale(car, (40, 40)) # resize car image

""" main loop varibales and things """
# set up timer clock 
clock = pygame.time.Clock()

# initial x y axis position of the car
car_x = 30   
car_y = 260  

JUMP_VALUE = 25     # turning point value
direction = 'y_up'  # cars current direction
run = 1

# start the robot
robot.write(b'f')

# main loop
while run:
    clock.tick(60)         # update the window/run loop by this speed
    #check for events
    for event in pygame.event.get():
        # quit button clicked
        if event.type == pygame.QUIT:
            run = 0

    # position images
    window.blit(bg, (0, 0))          # load the track image
    window.blit(car, (car_x, car_y)) # the car image

    # record last x, y pos of car
    last_x, last_y = car_x, car_y
    
    # find the center of the car and draw a point on that
    center_x, center_y = (int(car_x + 40 /2), int(car_y + 40 / 2))
    pygame.draw.circle(window, (0,255,255), (center_x, center_y), 5, 5)

    # check surrounding (4 direction data)
    # the calibration value is the pixel from car's sensor/mid point
    # so it checks for road info 30 pixels far from the sensor.
    # 255 means we have a clear white road
    cal_value = 30              # calibrate this to get good data
    y_up      = window.get_at((center_x, center_y - cal_value))[0]
    y_down    = window.get_at((center_x, center_y + cal_value))[0]
    x_right   = window.get_at((center_x + cal_value, center_y))[0]
    x_left    = window.get_at((center_x - cal_value, center_y))[0]
    #print("y_up   ", y_up)
    #print("y_down ", y_down)
    #print("x_right", x_right)
    #print("x_left ", x_left)
    #print("-----------")

    # determine which way to go
    # go up
    if y_up == 255 and direction == 'y_up' and x_left != 255 and x_right != 255:
        # move up
        car_y -= 2  # decrease pixel and move the car on y axis
        
    # make the turn
    if y_up == 255 and direction == 'y_up' and x_left != 255 and x_right == 255:
        # make a right turn
        direction = 'x_right'
        car_y -= JUMP_VALUE
        car_x += JUMP_VALUE
        car = pygame.transform.rotate(car, -90)
        window.blit(car, (car_x, car_y))
        print('Turn Right')
        robot.write(b'r')

    # go x right
    if y_up != 255 and direction == 'x_right' and y_down != 255 and x_right == 255:
        car_x += 2

    if y_down == 255 and direction == 'x_right' and x_left == 255 and x_right == 255:
        # make a turn from x_right
        car = pygame.transform.rotate(car, -90)
        direction = 'y_down'
        car_y += JUMP_VALUE + 5
        car_x += JUMP_VALUE
        window.blit(car, (car_x, car_y))
        print('Turn Right')
        robot.write(b'r')

    # go y down
    if y_down == 255 and direction == 'y_down' and x_left != 255 and x_right != 255:
        # move down
        car_y += 2

    # left turn
    if y_down == 255 and direction == 'y_down' and x_left != 255 and x_right == 255:
        # turn from y_down
        car = pygame.transform.rotate(car, 90)
        direction = 'x_right'
        car_y += JUMP_VALUE
        car_x += JUMP_VALUE
        print('Turn left')
        robot.write(b'l')
    
    # turn to y up
    if y_up == 255 and direction == 'x_right' and x_left == 255 and x_right == 255:
        # turn from y_down
        car = pygame.transform.rotate(car, 90)
        direction = 'y_up'
        car_y -= JUMP_VALUE + 5
        car_x += JUMP_VALUE
        print('Turn left')
        robot.write(b'l')
    
    # if car is stopped
    if car_x == last_x and car_y == last_y:
        # stop the engine sound
        print("STOPPED")
        robot.write(b's')
        
    pygame.display.update()  # update the window

pygame.quit()      #close everything
