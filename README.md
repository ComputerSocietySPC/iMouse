# iMouse

![image](https://github.com/ComputerSocietySPC/iMouse/assets/148703297/3b4f12ac-1664-472a-a5fe-e0608626bfd1)

iMouse is a Python script that utilizes hand gestures for controlling the mouse cursor and performing various actions. It uses the MediaPipe library for hand tracking and OpenCV for capturing and processing video from the webcam.

## Features

- Control the mouse cursor by raising the index finger and the thumb.
- Perform left-click by closing the thumb.
- Perform right-click by bending the index finger.
- Scroll the page up or down by raising both the index finger and the middle finger and moving it vertically.
- Switch between tabs in the browser by raising all fingers and moving the index finger horizontally.

## Our model series
- `iMouse_Opt.py` is a version that provides maximum performance and processing speed. It only shows the camera view in the cv2 window.
- `iMouse_Pro.py` is a version that provides a powerful display, providing real time data of the motion of the hand in the cv2 window.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI
- pynput
- keyboard
- Pillow
- numpy

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install the required Python packages by running the following command:
~~~
pip install opencv-python mediapipe pyautogui pynput keyboard Pillow numpy
~~~

## Usage

1. Connect a webcam to your computer.
2. Run the `iMouse_Opt.py` or `iMouse_Pro.py` script using the following command:
~~~
python iMouse_Opt.py
~~~
~~~
python iMouse_Pro.py
~~~
3. The webcam feed will open in a new window titled "Hand Gestures".
4. Perform the hand gestures described above to control the mouse cursor and perform actions.

## Notes
- Press the 'Esc' key to exit the program.
- Adjust the sensitivity of the hand gestures by modifying the thresholds and parameters in the script.

## Credit
- iMouse is a script completely created by **Christopher Wong**, a student from St. Paul's College.

## Disclaimer
The iMouse script is provided as-is without any warranties. The author is not responsible for any damages or issues caused by the usage of this script. Use it at your own risk.

## License
The iMouse script is released under the MIT License.
