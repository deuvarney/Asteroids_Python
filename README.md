# Asteroids Game
A Python implementation of the classic Asteroids game.

## Features
* A ship that can move around the screen
* Ability to shoot missiles
* Randomly spawned asteroids (rocks) that move at varying velocities
* Collision detection

# Controls
- Ship Movement: Use the left and right arrow keys to move the ship left and right, respectively.
- Thrust: Press the up arrow key to accelerate the ship forward. **
- Fire Missiles: Press the space bar to fire missiles at asteroids.**


# Running the Game
You have two options:

### Option 1: Run Locally To run the game locally, you'll need to set up a Python environment. Here's how:

**Install Python**: Install Python 3.9 or higher from the official website if you haven't already.

**Create Virtual Environment**: Create a new virtual environment using `python -m venv asteroid-env` (replace "asteroid-env" with your preferred name).

**Activate Virtual Environment**: Activate the virtual environment by running `source asteroid-env/bin/activate` on Linux/Mac or `astaion-env\Scripts\activate` on Windows.

**Install Dependencies**: Install the required dependencies from the `requirements.txt` file using `pip install -r requirements.txt`.

**Clone Repository**: Clone this repository and navigate to the project directory.

**Run Game**: Run the game using `python main.py`.

### Option 2: Play Online If you'd rather not set up a local environment, [play the game online](https://deuvarney.github.io/Asteroids_Python).

## Deployment
To deploy the game on MacOS for distribution, use python setup.py py2app -A for local development or python setup.py py2app for distribution. Note that this requires py2app to be installed.

Enjoy playing Asteroids!