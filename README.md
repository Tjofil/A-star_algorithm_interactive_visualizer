# A* algorithm interactive visualization
A visual simulation of popular algorithm using custom, distance based heuristic. 

![Image](https://github.com/Tjofil/A-star_algorithm_interactive_visualizer/gif/sim.gif)

## Running
Aside from [Python](https://www.python.org), third-party modules required to run the program are `pygame` and `tkinter` which can be obtained with pip by the following command:

    pip install pygame tk
    
## Usage and features
Execution flow of the simulator itself is composed of three main parts:
- **Obstacle editor** where user is able to define custom obstacles (unpassable terrain) for grid traversal simply by using left mouse click and hold similar to painting brush.
- **Starting and ending node setup** covers simple selection of the start and goal of the algorithm.
- **Simulation and post-simulation _phase_** displays the traversal and search itself, step-by-step in a visually pleasing way.

Keyboard controls:
>Spacebar - used to progress between each phase.

>R - available only while choosing the starting and ending vertices to reset the process.

![Image](https://github.com/Tjofil/A-star_algorithm_interactive_visualizer/gif/prep.gif)

