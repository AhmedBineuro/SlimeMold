# What is this?
This project basically tries to emulate the simulation implemented by Sebastian Lague. Also there might be a different implementation based on the link below.
			- https://www.youtube.com/watch?v=fOIL7Gmgbr0
# How will it work?
So the Sebastian Lague implementation divides the screen into a grid composed of cells similar to cellular automata simulations. in this grid there will be particles or agents that will be moving leaving behind a trail. This trail difuses and evaporates overtime. Each particle has 3 circular sensors arranged in an arc infront of it. Lastly each particle has a some randomness in turning.

The other implementation on the otherhand, grows in a direction in which the slime has not grown yet. Then when the slime makes contact with food then it will perform A* pathfinding algorithm to find the most optimal route.