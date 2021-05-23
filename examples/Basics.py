"""
PROJECT: SLIMELEARN FRAMEWORK BASICS EXAMPLE
AUTHOR: Javier Burgos Valdés
DESCRIPTION:
    This script's purpouse is to serve as a basic tutorial to learn how
    to structure your code, connect to the server, recive information
    and take actions.
"""

######## SDK ########
# First we import and load the SlimeLearn SDK to simplify the comunication
# with the server.
from slimelearnpy import SlimeLearn

sl = SlimeLearn()

######## Config ########
# Now we stablish the configuration we will send to the server. We can
# write a python dictionary or use the "load_config_file()" method from
# the SDK to load a .json file.
# The object should have this structure:

conf = {
    "req": "config",
    "payload": {
        "mode": "sec",
        "delay": 3,
    }
}

# The "mode" field is mandatory and must have either "sec", "jump" or "frame" 
# value. This sets when the server is going to call your agent function.
# This mode requires the "delay" field to set the time period between calls.


######## Agent ########
# It is time to write our agent. We must create a function with 1 parameter.
# The server will automaticly call this function as specified in the config.

def brain(input_data):
    """
    Shows its position and jump in the arrow's direction
    """
    x = input_data["player"]["x"]
    y = input_data["player"]["y"]

    print("I am at: ", x, "-", y)

    sl.jump()

# Note that the agent doesn't check if it is on the ground in the moment of
# executing the jump. If the agent tries to jump when he is not on the floor,
# the game will behave as if a human were playing and pressed the key in the
# wrong time. The action will be ignored. You can try this by reducing the
# delay time so the agent is called before it reaches the ground after the
# lastest jump.


######## Connection ########
# Finaly we connect, configure and run the server. Before executing this line
# the SlimeLearn server should have been launched and running.

sl.run("//localhost:8080", config=conf, function=brain)