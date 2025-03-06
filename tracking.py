import cv2
import os
import glob
import json
import numpy as np  # Add numpy import
from gaze_tracking import GazeTracking
import time

# Initialize GazeTracking
gaze = GazeTracking()

# Path to the folder containing .png files
sharedPath = r'C:\Users\R1nge\Documents\TELEGRAM\SHARED'
statePath = os.path.join(sharedPath, "STATE")
statePathJson = os.path.join(statePath, "STATE.json")

state = {
            "state": "detection_gaze"
        }

with open(statePathJson,'w', encoding='utf-8') as f:
    json.dump(state, f,ensure_ascii=False, indent=4)

# Find all .png files in the folder
png_files = glob.glob(os.path.join(sharedPath, '*.png'))

# Dictionary to store results
results = [None] * len(png_files)

print(len(png_files))

i = 0
# Analyze each .png file
for png_file in png_files:
    # Read the image
    frame = cv2.imread(png_file)

    # Send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    # Get gaze direction
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

    # Get pupil coordinates
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    # Store the result in the dictionary
    results[i] = {
        'direction': direction
    }
    i += 1
    print(i)

print(len(results))

# Save results to a JSON file
output_file = os.path.join(sharedPath, 'gaze_results.json')
with open(output_file, 'w') as json_file:
    json.dump(results, json_file, indent=4)

print(f"Results saved to {output_file}")


state = {
            "state": "gaze_finished"
        }

with open(statePathJson,'w', encoding='utf-8') as f:
    json.dump(state, f,ensure_ascii=False, indent=4)