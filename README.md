# Camera_Calibration

## Installation

### 1. Clone this repository

```
git clone https://github.com/RVGroup-CTUT/Camera_Calibration.git 
```
### 2. Install dependencies

``` python
pip install -r requirements.txt or pip3 install -r requirements.txt
```
### 3. Tutorials

__``The below steps is to implement Step by step the camera calibration``__ 

#### Step 1: Take chessboard image

```
python take_image.py
```
#### Step 2: Run the code for the calibration. We will get the "json" file that contains undistortion matrix

```
python Calibrate_camera.py
```
