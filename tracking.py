import cv2
import os
import glob
import json
from gaze_tracking import GazeTracking
import subprocess

gaze = GazeTracking()

sharedPath = r'C:\Users\R1nge\Documents\TELEGRAM\SHARED'
statePath = os.path.join(sharedPath, "STATE")
statePathJson = os.path.join(statePath, "STATE.json")

state = {
            "state": "detection_gaze"
        }

with open(statePathJson,'w', encoding='utf-8') as f:
    json.dump(state, f,ensure_ascii=False, indent=4)

png_files = glob.glob(os.path.join(os.path.join(sharedPath, "GAZE"), '*.jpg'))

results = []

print(len(png_files))

i = 0
for png_file in png_files:
    frame = cv2.imread(png_file)

    gaze.refresh(frame)

    if gaze.is_blinking():
        direction = "Blinking"
    elif gaze.is_right():
        direction = "Looking right"
    elif gaze.is_left():
        direction = "Looking left"
    elif gaze.is_center():
        direction = "Looking center"
    else:
        direction = "Unknown"

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if left_pupil is not None:
        left_eye_x = left_pupil[0]
        left_eye_y = left_pupil[1]
    else:
        left_eye_x = None
        left_eye_y = None

    if right_pupil is not None:
        right_eye_x = right_pupil[0]
        right_eye_y = right_pupil[1]
    else:
        right_eye_x = None
        right_eye_y = None

    if left_pupil is not None or right_pupil is not None:
        data = {
            'direction': direction,
            'left_eye_x': int(left_eye_x),
            'left_eye_y': int(left_eye_y),
            'right_eye_x': int(right_eye_x),
            'right_eye_y': int(right_eye_y)
        }
        results.append(data)
        print(data)
        i += 1
        print(i)

print(len(results))

output_file = os.path.join(sharedPath, 'gaze_results.json')
with open(output_file, 'w') as json_file:
    json.dump(results, json_file, indent=4)

print(f"Results saved to {output_file}")


state = {
            "state": "gaze_finished"
        }

with open(statePathJson,'w', encoding='utf-8') as f:
    json.dump(state, f,ensure_ascii=False, indent=4)

Face_landmarks = os.path.join(sharedPath, "Face_Landmarks.bat")
result = subprocess.run([Face_landmarks], shell=True)