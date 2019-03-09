# Traffic System
This system consists of two parts, a traffic publisher and a lights controller

The communications are all done over mqtt

I've eliminated the need for a broker entirely, start `traffic.py` first, then start `publisher.py`. 

The publisher first asks the user for a password (the password is `password`, then sends that password to the lights controller. Upon a successful password, the controller will go into authenticated mode and you can begin to give it commands.

All traffic to the lights controller is being sent over `traffic/lights`, and all publisher traffic is going over `traffic/pub`.

## Publisher commands
```
H - shows this help message
L - gets current light direction
N, S, E, W - sends car to lights
US, UK - set country
```

## Usage
Note that you should not need to use any external publisher tools to test this application, it should just take the following commands
```
$ python traffic.py
$ python publisher.py
```

## Wiring
You don't need to use a raspberry pi to test this, there is a module in the project folder that will display all the light changes.

If you do decide to wire up a breadboard and test this out, see the lights diagram picture in the project directory (written instructions coming soon).