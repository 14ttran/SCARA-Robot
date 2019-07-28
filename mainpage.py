## @file mainpage.py
#  @author - Ahmed Shorab, Kevin Tran, Tomy Tran
#  @mainpage
#  @section Purpose 
#   This script controls the robot Bot Ross to paint a given profile with
#   a specified paint color. This script implements multiple tasks that
#   repeatedly run asynchronously, but they are run so quickly that the
#   mechanical system operates as if the tasks were being operated
#   simultaneously.
#  @section Usage
#   How to use: The script is already complete with all tasks set up. To use
#       it, upload the code to the STM32 microcontroller and plug in the motor
#       pins to the appropriate locations. Then run the code and follow the
#       instructions.
#  @section Testing
#   This script was tested by providing a variety of profiles to draw and
#   running the script to see the result.
#  @section Limitations
#   If different hardware is used, or if the user desires to use different
#   pins on the microcontroller, the script will have to be modified to
#   accomodate the change.
#  @section Location
#   http://wind.calpoly.edu/hg/mecha13 under Project