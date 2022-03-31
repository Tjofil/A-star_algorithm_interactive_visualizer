# A star algorithm interactive visualization
A visual simulation of a standard analog tektronix oscilloscope. Project created to help students get familiar with working in a lab during the pandemic. ⚡

![Image](https://github.com/stevomitric/Analog-Oscilloscope/blob/main/src/analogni-osciloskop-gif.gif)

## Running
Aside from [Python](https://www.python.org) itself, other third-party modules required to run the simulator are `numpy` and `PIL` which can be obtained with pip by the following command:

    pip install pillow numpy
    
## Features
Window is composed of three main parts: Screen, Controls and Input.

The Screen, shown as a blue canvas on the right side, is used to draw the input signals. It is divided into 5x4 divs, values of which can be configured in the Controls panel.

The Input panel includes two connectors which are used to describe the input signal. Left-clicking on BNC icons you are prompted to give some kind of a signal. The three most common options are shown in the app: sin, squared and custom. Custom option allows giving any signal that can be described with python lambda functions.

The Controls section is replicated from the Tektronix model and is used to display the input signals. Features (from left to right, top to bottom) include:
- Positioning each signal on a Y-axis
- Defining trigger level for synchronization
- Selecting display mode (CH1, CH2, DUAL, ADD)
- Multiplying first signal by x5
- Inverting second signal
- Configuring voltage for each DIV
- Changing time scale (for both signals), drawing Lissajous Figures
- Display mode for each signal (AC, GND, DC)


## Examples
The following is an example of a Lissajou figure:
![Image2](https://github.com/stevomitric/Analog-Oscilloscope/blob/main/src/heart.png?raw=true)

## Development
Although I'm not planning on pushing further upgrades for this project in the foreseeable future, suggestions and ideas are more than welcome!