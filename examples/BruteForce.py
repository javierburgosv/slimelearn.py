"""
PROJECT: SLIMELEARN FRAMEWORK BRUTE FORCE EXAMPLE
AUTHOR: Javier Burgos Valdés
DESCRIPTION:
    This script contains a very basic AI that jumps in the direction of 
    the next platform and brute forces its way up by making small changes
    to this result until it make a successful jump.
"""

######## Imports ########
import numpy as np
from math import atan, degrees
from random import *
from numpy.core.numeric import Infinity

######## SDK ########
from slimelearnpy import SlimeLearn

sl = SlimeLearn()
custom_config = {
    "req": "config",
    "payload": {
        "mode": "jump",
        "speed": 2
    }
}

######## Agent ########
#The list of successful jumps in order
steps = []
step_index = 0

#Previous player_y before jumping
previous_height = None

#Last jump's angle
previous_cangle = None
remembering = False

#Agent configuration
min_offset = 5           
angle_offset = min_offset
angle_offset_increment = 3     
success_tolerance = 0

def target_brute_force(input_data):
    """
    Basic brute force algorithm example.
    REQUIREMENT: Server mode set to "jump"
    """
    global sl
    global steps
    global step_index
    global previous_height
    global previous_cangle
    global remembering 
    global angle_offset
    global success_tolerance

    #Unpack player data and invert the y axis to compensate for Godot inverted values
    player = input_data["player"]
    player["y"] = -player["y"]                  

    #Check if we should be reproducing already successful jumps or calculate a new one
    if step_index == len(steps): remembering = False

    if remembering:
        #Reproduce the successful jump that follows
        print("Using my memory...")
        last_jump = steps[step_index]
        sl.jump(last_jump)
        step_index += 1
    else:
        resolution = True
        if previous_cangle != None:
            #If we've made a new jump in the previous step we should evaluate if it was successful
            resolution = check_last_jump_success(player, previous_height, previous_cangle, success_tolerance)
        if resolution:
            print("Calculating new jump...")
            #Find next objective
            next_platform = calculate_target(player, input_data["sight"])
            if next_platform != None:
                #Calculates the angle for the jump and execute the jump
                angle = calculate_jump(player, next_platform, angle_offset)
                previous_height = player["y"]
                previous_cangle = angle
                sl.jump(angle)
                print(angle)
            else:
                print("NO MORE JUMPS AVAILABLE")
    
    print("----------")

def calculate_jump(player, next_platform, offset):
    """
    Calculate the angle to jump to the next platform
    """
    dif_y = next_platform["y"] - player["y"]
    dif_x = next_platform["x"] - player["x"]
        
    angle = degrees(atan(abs(dif_y / dif_x)))
        
    if dif_x < 0:
        angle = -90 + angle + offset
    else:
        angle = 90 - angle - offset

    return angle
    
def check_last_jump_success(player, previous_height, previous_cangle, tolerance):
    """
    Determines wheather or not the last jump was a success an should be saved
    """
    global angle_offset
    global angle_offset_increment
    global min_offset

    success = False
    print(player["y"])
    print(previous_height)
    if previous_height != None and player["y"] <= previous_height - tolerance:
        print("Failure! Starting Again...")
        angle_offset += angle_offset_increment
        reset_game()
    else:
        if previous_cangle != None:
            print("Success! Saving Jump...")
            steps.append(previous_cangle)
            previous_height = player["y"]
            angle_offset = min_offset
        success = True

    return success

def calculate_target(player_data, sight_data):
    """
    Function that locates the next platform the agent should reach
    """
    target = None
    min_height = Infinity

    for platform in sight_data:
        platform_y = -platform["y"]

        if platform_y < min_height and platform_y > player_data["y"]:
            min_height = platform_y
            target = platform
            target["y"] = platform_y

    return target

def reset_game():
    """
    Start a new game keeping the successful steps
    """
    global step_index
    global remembering
    global previous_height
    global previous_cangle

    step_index = 0
    remembering = True
    previous_height = None
    previous_cangle = None

    sl.reset()

sl.run(uri = "//localhost:8080" , config = custom_config, function = target_brute_force)

input("Press enter to exit...")
