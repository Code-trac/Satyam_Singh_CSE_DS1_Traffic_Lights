from flask import Flask, jsonify, render_template
import time
import threading
import cv2
import utils
import detection
import density
import decision

app = Flask(__name__, template_folder='templates', static_folder='static')


latest_data = {
    "lane_densities": [0.0] * len(utils.LANE_ROIS),
    "current_green_lane": 0,
    "signal_timer": decision.MIN_GREEN_TIME,
    "timestamp": time.time(),
    "error": None
}
data_lock = threading.Lock()
stop_processing_flag = threading.Event()


def traffic_processing_loop():
    global latest_data
    print("Attempting to load YOLO model...")
    try:
        model, model_names, vehicle_class_indices = detection.load_yolo_model()
        if model is None:
            raise RuntimeError("Failed to load YOLO model.")
        print("YOLO model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        with data_lock:
            latest_data["error"] = f"Model Load Error: {e}"
        return # Stop thread if model fails

    print("Attempting to open webcam...")
    cap = cv2.VideoCapture(0) # Use camera index 0
    if not cap.isOpened():
        print("Error: Could not open camera.")
        with data_lock:
            latest_data["error"] = "Could not open camera."
        return # Stop thread if camera fails
    print("Webcam opened successfully.")

    current_green_lane = 0
    signal_timer = decision.MIN_GREEN_TIME
    last_update = time.time()

    while not stop_processing_flag.is_set():
        try:
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read frame from camera. Retrying...")
                time.sleep(0.5)

                continue

            current_time = time.time()
            time_delta = current_time - last_update


            detected_objects = detection.detect_vehicles(frame, model, vehicle_class_indices, conf_threshold=0.3)

            _, detections_in_lanes = utils.draw_detections(frame, detected_objects, utils.LANE_ROIS, model_names)


            lane_densities = density.calculate_lane_density(detections_in_lanes, utils.LANE_ROIS)


            signal_timer -= time_delta
            if signal_timer <= 0:

                next_lane, next_duration = decision.get_next_signal_state(lane_densities, current_green_lane)
                current_green_lane = next_lane
                signal_timer = next_duration

            last_update = current_time

            with data_lock:
                latest_data["lane_densities"] = [round(d, 1) for d in lane_densities]
                latest_data["current_green_lane"] = current_green_lane
                latest_data["signal_timer"] = round(max(0, signal_timer), 1)
                latest_data["timestamp"] = current_time
                latest_data["error"] = None



        except Exception as e:
            print(f"Error during processing loop: {e}")
            with data_lock:
                latest_data["error"] = f"Processing Error: {e}"
            time.sleep(2)


    print("Processing thread stopping...")
    cap.release()
    print("Webcam released.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/traffic_data')
def get_traffic_data():
    with data_lock:
        data_to_send = latest_data.copy()
    return jsonify(data_to_send)

if __name__ == '__main__':
    print("Starting background traffic processing thread...")
    processing_thread = threading.Thread(target=traffic_processing_loop, daemon=True)
    processing_thread.start()

    print("Starting Flask server on http://127.0.0.1:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        print("Flask server shutting down, signaling processing thread to stop...")
        stop_processing_flag.set()
        processing_thread.join(timeout=5)
        print("Shutdown complete.")

