import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.48.137' # '169.254.48.137' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = 0 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.17 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red metal
bin2_offset = 0.17 #green
bin2_color = [0,1,0]# green paper
bin3_offset = 0.17 #blue
bin3_color = [0,0,1]# blue plastic
bin4_offset = 0.17 #black
bin4_color = [0,0,0] # black garbage

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

import random
import math

# intializes container bin and weight lists for use in any function
container_bin=[]
container_weight=[]

# returns the bin where the container needs to go to, records container weight as well
def random_dispense():
    container=random.randint(1,6) #variable name for the 6 different containers
    container_info=table.dispense_container(container, True) #dispenses container and store information
    location, weight, bin_num = container_info #variables for values in list
    return weight, bin_num #return weight and bin number

#Load Containers
def movement_arm(container_amount):
    #movement of arm to pick up container and rotate to face qbot
    arm.home()

    # grabs container with qarm, uses sleep functions for efficiency
    time.sleep(1)
    arm.move_arm(0.65,0,0.27)
    time.sleep(1)
    arm.control_gripper(36)
    time.sleep(1)
    arm.move_arm(0.2,0,0.4)
    arm.rotate_elbow(-30)
    arm.rotate_base(-90)
    time.sleep(1)

    if container_amount == 0: #if no containers have been loaded, move to first position on hopper
        # if bot is in range of arm, place container right away
        if bot.position()[0]-2.1 >= -0.643:
            # qarm coordinates are based on position of qbot, x at +.12
            arm.move_arm(-bot.position()[1]+.12,bot.position()[0]-2.1,0.52)
            time.sleep(1)
            arm.control_gripper(-10)
            time.sleep(2)
            arm.rotate_shoulder(-20)
        else:
            # if bot is not in range of arm when at home, bot must move forward for arm to place container
            bot.forward_distance(0.05) # 5 cm is enough in all cases
            arm.move_arm(-bot.position()[1]+.12,bot.position()[0]-2.1,0.52)
            time.sleep(1)
            arm.control_gripper(-10)
            time.sleep(2)
            arm.rotate_shoulder(-20)
            # uses time.time() library for more reliable version of sleep()
            start_time = time.time()
            current_time = 0
            while(current_time < 0.5): # waits half a second
                current_time = time.time() - start_time
            # bot returns to line since it moved off of it
            bot.rotate(180)
            bot.forward_distance(0.05)
            bot.rotate(-180)

    elif container_amount == 1: #if 1 container has already been loaded, move to next position on hopper
        # -0.643 is max range for y coordinate of qarm
        if bot.position()[0]-2.1 >= -0.643:
            arm.move_arm(-bot.position()[1]+.04,bot.position()[0]-2.1,0.52)
            time.sleep(1)
            arm.control_gripper(-10)
            # use sleep() instead of time.time() for better readability and efficiency
            time.sleep(2)
            arm.rotate_shoulder(-20)
        else:
            # only runs if bot is out of range of arm
            bot.forward_distance(0.05)
            # x coordinate of qarm at +.04
            arm.move_arm(-bot.position()[1]+.04,bot.position()[0]-2.1,0.52)
            time.sleep(1)
            arm.control_gripper(-10)
            time.sleep(2)
            arm.rotate_shoulder(-20)
            # time library used for reliability
            start_time = time.time()
            current_time = 0
            while(current_time < 0.5):
                current_time = time.time() - start_time
            # bot returns to line
            bot.rotate(180)
            bot.forward_distance(0.05)
            bot.rotate(-180)
        
    elif container_amount == 2: #if 2 container has already been loaded move to this position
        if bot.position()[0]-2.11 >= -0.643:
            arm.move_arm(-bot.position()[1]-.05,bot.position()[0]-2.11,0.52)
            time.sleep(1)
            arm.control_gripper(-10)
            time.sleep(2)
            arm.rotate_shoulder(-20)
        else:
            # only runs if bot is out of range of arm
            bot.forward_distance(0.05)
            # x coordinate of qarm at -.05
            arm.move_arm(-bot.position()[1]-.05,bot.position()[0]-2.11,0.52)
            time.sleep(1)
            arm.control_gripper(-10)
            time.sleep(2)
            arm.rotate_shoulder(-20)
            # time library substitute for sleep()
            start_time = time.time()
            current_time = 0
            while(current_time < 0.5):
                current_time = time.time() - start_time
            # bot returns to line
            bot.rotate(180)
            bot.forward_distance(0.05)
            bot.rotate(-180)

    start_time = time.time() # rest so that the arm has time to let go of the container
    current_time = 0
    while(current_time < 1):
        current_time = time.time() - start_time
    arm.rotate_elbow(-20)
    arm.home()

# loading hopper with qarm
# main function initially rotates qbot, dipenses containers and stores their info
# also calls all functions and initiates while loop to run continuously
def main():
    container_amount=0 #no container in the hopper
    total_mass=0 # no mass on hopper
    old_location="" # intializes old location to store desired bin for container
    container_on_hopper = False
    bot.rotate(-95) # rotates bot for easy access to hopper

    weight, bin_num = random_dispense() #container dispenses
    container_exists = True #container exists to pick up
    
    while True:             
        new_mass= weight # stores values of newly dispensed container
        new_location= bin_num
        # if constriants don't apply, run arm movement
        # contraints: over 3 containers on hopper, hopper mass over 90,
        # new container does not match destination of previous container
        if container_amount < 3 and total_mass < 90 and (new_location == old_location or old_location == ""): 
            total_mass += new_mass
            old_location = new_location
            # calls movement arm function with parameter so it knows where to place container
            movement_arm(container_amount)
            container_amount +=1
            # container amount on hopper incr., no more container in sorting station
            container_exists = False
            
            weight, bin_num = random_dispense() #container dispenses
            container_exists = True #container exists to pick up
        #once contraints apply, move qbot
        else:
            # qbot sets out to deliver loaded containers at specified location
            move_qbot(old_location)
            deposit_container()
            return_home()
            bot.rotate(-95) # qbot is rotated for easy access to hopper
            # mass, container, location variables are reset
            container_amount=0
            total_mass= 0
            old_location = new_location
# main function loops indefinitely as system sorts randomly dispensed containers

# dispenses one red can into the sorting station,
# initiates all other functions for one full sorting cycle
# useful for troubleshooting and diagnostics
def dispense_red_can():
    x = table.dispense_container(2, True)
    print("printing x", x)
    movement_arm()
    lower_cont_1()
    move_qbot(x[2])
    deposit_container()
    return_home()
# weighs red can, loads qbot, qbot deposits can, qbot returns home

# function to move q bot while detecting for correct box attributes (attr)
def move_qbot(bin):
    # activate both sensors, record starting (home) position
    bot.rotate(95) #-90
    bot.activate_ultrasonic_sensor()
    bot.activate_color_sensor()
    home_position = bot.position()
    # starts qbot at slow speed, initializes target values for sensing bin
    bot.set_wheel_speed([0.04, 0.04])

    # depending on container attributes:
    # qbot will be looking for the corresponding bin
    if bin == "Bin01":
        # distance to detect bin 1, 2 are greater as they're more prone to error
        dist_attr = 0.08
        color_attr = [1, 0, 0]
        print("Going to Bin 01!")
    elif bin == "Bin02":
        dist_attr = 0.06
        color_attr = [0, 1, 0]
        print("Going to Bin 02!")
    elif bin == "Bin03":
        dist_attr = 0.05
        color_attr = [0, 0, 1]
        print("Going to Bin 03!")
    else:
        dist_attr = 0.05
        color_attr = [0, 0, 0]
        print("Going to Bin 04!")

    # while loop continues to run until correct bin sensed
    while True: # bot.read_color_sensor() != color_attr or bot.read_ultrasonic_sensor() > dist_attr:
        # continues to sense presence of yellow guideline
        color = bot.read_color_sensor()[0]
        distance = bot.read_ultrasonic_sensor()
        if distance <= dist_attr and color == color_attr:
            print("I see the bin!", bot.read_ultrasonic_sensor(), bot.read_color_sensor()[0])
            break
        # adjusts direction of qbot if yellow guideline not sensed
        line = bot.line_following_sensors()
        if(line[0] == 1 and line[1] == 1):
            bot.set_wheel_speed([0.04, 0.04])
        elif(line[0] > line[1]):
            bot.set_wheel_speed([0.04, 0.064])
        elif(line[0] < line[1]):
            bot.set_wheel_speed([0.064, 0.04])
        # safety break if qbot is off course
        elif(line[0] == 0 and line[1] == 0):
            bot.stop()
            break
        # continues to print values detected for style points
        print("Colour Sensor:", color)
        print("Ultrasonic Sensor:", distance)
        print("Line Sensors:", bot.line_following_sensors())
    # stops qbot and moves forward extra 5 cm to account for early detection
    print("Stopping...")
    bot.stop()
    bot.forward_distance(0.05)


# function to deposit containers from q bot at a safe position
# hopper raised incrementely to ensure no container stays on it
# also ensures no container is launched into the stratosphere
def deposit_container():
    # rotates hopper in 30, 45, 60, and 90 deg increments
    # waits between each movement to allow containers to fall
    bot.activate_stepper_motor()
    bot.rotate_hopper(30)
    start_time = time.time()
    current_time = 0
    while(current_time < 1.5):
        current_time = time.time() - start_time
    bot.rotate_hopper(45)
    start_time = time.time()
    current_time = 0
    while(current_time < 1.5):
        current_time = time.time() - start_time
    bot.rotate_hopper(60)
    start_time = time.time()
    current_time = 0
    while(current_time < 1.5):
        current_time = time.time() - start_time
    bot.rotate_hopper(90)
    start_time = time.time()
    current_time = 0
    while(current_time < 1):
        current_time = time.time() - start_time
    # hopper retreats to original position
    bot.rotate_hopper(0)
    

# function for returning q bot to home position
def return_home():
    # starts qbot at nice, slow speed
    bot.set_wheel_speed([0.04, 0.04])
    # initializes position (pos) variable
    pos = bot.position()
    # while loops continues to run until qbot reaches home
    while not(1.3 < pos[0] < 1.7 and 0 < pos[1] < 0.2):
        line = bot.line_following_sensors()
        pos = bot.position()
        print("Bot Position:", pos[0], pos[1])
        print("Line Sensors:", line)
        # adjusts course of qbot if yellow line not detected
        if(line[0] == 1 and line[1] == 1):
            bot.set_wheel_speed([0.05, 0.05])
        elif(line[0] > line[1]):
            bot.set_wheel_speed([0.02, 0.08])
        elif(line[0] < line[1]):
            bot.set_wheel_speed([0.08, 0.02])
        else:
            bot.set_wheel_speed([-0.05, -0.05])
    bot.stop()

# records and prints home position as soon as starting the program
home_position = bot.position()
print(home_position)

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
