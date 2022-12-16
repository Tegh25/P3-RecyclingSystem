# P3-RecyclingSystem
Two robot recycling system algorithm for our third engineering design project, coded in python on a raspberry pi 4 and simulated using Quanser Interactive Labs. More info about this project can be found <a href="https://atelieyt.notion.site/Revenge-of-the-Recycling-System-ba956616b3864fad92bbb51508aa9e8f" target="_blank">here</a>.

In this repo you can find the code itself, our design project report, and a research summary on inductive proximity sensors.

## How it Works

The general workflow of our programming started with dispensing a random container at the sorting station. The robotic arm would pick it up, determine its weight, and place up to three matching containers onto the hopper of the transfer robot. The transfer bot used the weight of the containers to determine which sorting bin it needed it to go to. Containers made of paper, plastic, and metal would be sorted in separate bins, and plastic and paper containers which exceeded the weight threshold were determined to be too dirty for recycling and sent to the garbage bin.

The transfer robot used a line following algorithm to follow a pre-determined path until it reached the right bin. We utilized a color sensor and an ultrasonic sensor to determine the correct bin for the robot to stop at. Once the containers were unloaded, the robot followed the line until it reached the home position. The cycle continues indefinitely until the program is terminated.
