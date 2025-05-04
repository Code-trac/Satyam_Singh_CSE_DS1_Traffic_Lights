import cv2
import time
import numpy as np

import detection
import density
import decision
import utils

ROIs = utils.LANE_ROIS
MIN_GREEN_TIME = decision.MIN_GREEN_TIME


model, model_names, vehicle_class_indices = detection.load_yolo_model()

if model is None:
    print("Error: Failed to load YOLO model. Exiting.")
    exit()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

current_green_lane_index = 0
signal_timer = MIN_GREEN_TIME
last_update_time = time.time()

print("Starting traffic monitoring... Press 'q' to quit.")


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame from camera.")
        break

    current_time = time.time()
    time_delta = current_time - last_update_time

    detected_objects = detection.detect_vehicles(frame, model, vehicle_class_indices, conf_threshold=0.3)

    display_frame = frame.copy()

    display_frame, detections_in_lanes = utils.draw_detections(display_frame, detected_objects, ROIs, model_names)

    display_frame = utils.draw_rois(display_frame, ROIs)

    lane_densities = density.calculate_lane_density(detections_in_lanes, ROIs)

    signal_timer -= time_delta
    last_update_time = current_time

    if signal_timer <= 0:

        next_lane, next_duration = decision.get_next_signal_state(lane_densities, current_green_lane_index)
        current_green_lane_index = next_lane
        signal_timer = next_duration # Reset timer


    for idx, roi_density in enumerate(lane_densities):
        x, y, w, h = ROIs[idx]

        color = (0, 255, 0) if roi_density > 15 else (0, 165, 255)
        cv2.putText(display_frame, f"Lane {idx+1}: {roi_density:.1f}%", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


    for i in range(len(ROIs)):
        x, y, w, h = ROIs[i]
        text_y = y + h + 20
        if i == current_green_lane_index:

            signal_text = f"GREEN: {max(0, signal_timer):.1f}s"
            signal_color = (0, 255, 0) # Green
        else:

            signal_text = "RED"
            signal_color = (0, 0, 255) # Red

        cv2.putText(display_frame, signal_text, (x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, signal_color, 2)



    cv2.imshow("Traffic Monitor (Press 'q' to quit)", display_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break


cap.release()
cv2.destroyAllWindows()
print("Resources released.")
