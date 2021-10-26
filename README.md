## 1. Hello

This is my awersome research on virtual environments. The article is available at doi:10.1111/1000-7 
You can easily reproduce my results by running scripts locally.
Please cite me!

## 2. Prerequirements

### 2.1. OS version

This project and instruction was tested on Ubuntu 20.04.
Step-by-step instruction listed below might not work correctly on other OS.

### 2.2. Python version

This project is using some python features that are available only in python3.9.
Compatibility with other python version was not tested.

### 2.3. System software

You should have some set of software in your system. You can setup them using these commands:

`sudo apt update`<br>
`sudo apt install git python3.9 python3.9-venv libgl-dev libglib2.0-0`

## 3. Step-by-step instruction

1. Clone the repo.<br> `git clone https://github.com/krglkvrmn/Virtual_environment_research`
1. Make virtual evironment.<br>  `python3.9 -m venv vpain`
1. Switch to virtual environment.<br> `source vpain/bin/activate`
1. Install python requirements.<br> `pip install -r Virtual_environment_research/requirements.txt`
1. And run the project's script.<br> `python Virtual_environment_research/pain.py`
1. Enjoy!
