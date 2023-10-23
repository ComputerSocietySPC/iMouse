import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Controller as MouseController
import keyboard

pyautogui.FAILSAFE = False

prev_index_finger_y = None

prev_index_finger_x = None

vel = 0

all_vel = 0

mouse_x = 0

mouse_y = 0

is_left_click = False

is_right_click = False

mouse = MouseController()

def is_key_pressed(key):
    return keyboard.is_pressed(key)

# Function to perform left scroll
def scroll_left():
    pyautogui.scroll(-1)

# Function to perform right scroll
def scroll_right():
    pyautogui.scroll(1)

# Function to perform page up scroll
def scroll_page_up():
    pyautogui.scroll(100)

# Function to perform page down scroll
def scroll_page_down():
    pyautogui.scroll(-100)

# Function to move the mouse
def move_mouse(x, y):
    pyautogui.moveTo(x, y)

# Function to perform left-click
def left_click():
    pyautogui.leftClick()

# Function to perform right-click
def right_click():
    pyautogui.rightClick()

# Function to switch to previous tab
def previous_tab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.keyUp('alt')

# Function to switch to next tab
def next_tab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

# MediaPipe hand tracking initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# OpenCV window initialization
cv2.namedWindow("Hand Gestures")

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe hands
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as hands:
    while cap.isOpened():
        # Read the video feed
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image color to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip the image horizontally for a mirror-like effect
        image = cv2.flip(image, 1)

        # Process the image with MediaPipe
        results = hands.process(image)

        # Convert the image back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw hand landmarks on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # Get the coordinates of index finger and thumb
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
                index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

                middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
                middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
               
                ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                
                pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

                # Get the coordinates of hand center
                hand_center = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

                # Calculate the distance between index finger and thumb
                index_middle_distance = abs(index_finger.x - middle_finger.x) + abs(index_finger.y - middle_finger.y)
                middle_ring_distance = abs(ring_finger.x - middle_finger.x) + abs(ring_finger.y - middle_finger.y)
                index_finger_is_straight = bool((index_finger.y / index_finger_dip.y / (index_finger_dip.y / index_finger_mcp.y)) > 0)
                all_fingers_raised = bool(index_finger.y < index_finger_mcp.y and middle_finger.y < middle_finger_mcp.y and ring_finger.y < ring_finger_mcp.y and pinky.y < pinky_mcp.y)

                # Calculate the change in index finger y-coordinate
                if prev_index_finger_y is not None:
                    delta_y = index_finger.y - prev_index_finger_y
                else:
                    delta_y = 0

                vel = vel*0.7
                mouse.scroll(0,vel)

                # Update the previous index finger y-coordinate
                prev_index_finger_y = index_finger.y

                if prev_index_finger_x is not None:
                    delta_x = index_finger.x - prev_index_finger_x
                else:
                    delta_x = 0
                
                # Update the previous index finger y-coordinate
                prev_index_finger_x = index_finger.x

                if all_fingers_raised == True:
                    if abs(delta_x) > 0.3:
                        next_tab()

                elif index_middle_distance < 0.1 and index_finger_is_straight == True:
                    if delta_y > 0.1:
                        vel = delta_y*14
                        # scroll_page_up()
                        cv2.putText(
                            image,
                            "Scroll Page Up",
                            (int(hand_center.x * image.shape[1]), int(hand_center.y * image.shape[0])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                            cv2.LINE_AA,
                        )
                    elif delta_y < -0.1:
                        vel = delta_y*14
                        cv2.putText(
                            image,
                            "Scroll Page Down",
                            (int(hand_center.x * image.shape[1]), int(hand_center.y * image.shape[0])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                            cv2.LINE_AA,
                        )
                    else:
                        cv2.putText(
                            image,
                            "Scroll",
                            (int(hand_center.x * image.shape[1]), int(hand_center.y * image.shape[0])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                            cv2.LINE_AA,
                        )
                    
                else:
                    mouse_x = mouse_x + (index_finger_mcp.x * image.shape[1]*3.5 - 200 - mouse_x)*0.2
                    mouse_y = mouse_y + (index_finger_mcp.y * image.shape[0]*3.5 - 300 - mouse_y)*0.2
                    
                    list_1 = [str(int(mouse_x)), str(int(mouse_y))] 

                    separator = ', ' 

                    result = separator.join(list_1) 
                    
                    mouse.position = mouse_x, mouse_y

                    cv2.putText(
                        image,
                        "Move Mouse",
                        (int(hand_center.x * image.shape[1]), int(hand_center.y * image.shape[0])),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

                    if index_finger_mcp.x - thumb.x < 0.06:
                        if is_left_click == False:
                            left_click()
                            is_left_click = True
                    
                    else:
                        is_left_click = False

                    
                    if index_finger_dip.y < index_finger.y:
                        if is_right_click == False:
                            right_click()
                            is_right_click = True
                    
                    else:
                        is_right_click = False

        # Display the image
        cv2.imshow("Hand Gestures", image)

        # Exit the program if 'q' is pressed
        if is_key_pressed('esc'):
            break
        if cv2.waitKey(1) == 27:
            break

# Release the video capture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
