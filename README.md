# Camera_Calibration

## Git tutorial

### 1. First, we need to "pull" the code before "pushing"

```python
git init
git pull
```

### 2. Second, we add all changed code.

```python
git add .
```

### 3. Then, you upload the code to the git's repository.

```python
git commit -m "name: depending on you"
```

### 4. Final, you use the code to push all of them to your repository.

```python
git push -f  origin main
```

or

```python 
git push -f  origin master
```

-> choosing "main" or "master" based on the type of branch . 


## Installation

### 1. Clone this repository

```
git clone https://github.com/RVGroup-CTUT/Camera_Calibration.git 
```
### 2. Install dependencies

``` python
pip install -r requirements.txt
```

or 

```python
pip3 install -r requirements.txt
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
