📝 Description

This project implements a prototype for an intelligent traffic light control system designed to optimize traffic flow at intersections. It utilizes real-time computer vision with the YOLOv8 object detection model to monitor vehicle density in different lanes. Based on this density analysis, the system dynamically adjusts traffic signal timings, prioritizing busier lanes and skipping empty ones, aiming to reduce unnecessary waiting times compared to traditional fixed-timer systems. A web-based dashboard provides a real-time view of lane densities and current signal status.

✨ Features

* **🚗 Real-time Vehicle Detection:** Uses YOLOv8 (specifically `yolov8n.pt`) via the Ultralytics library to detect vehicles (cars, trucks, buses, motorcycles) from a webcam feed.
* **📊 Lane Density Calculation:** Calculates traffic density for up to 4 predefined lanes based on the area occupied by detected vehicles within specific Regions of Interest (ROIs).
* **⏱️ Adaptive Signal Timing:** Implements dynamic green light allocation logic that:
    * Prioritizes lanes with higher density.
    * Skips lanes with zero detected density.
    * Adjusts green light duration proportionally to density (within configurable min/max limits).
    * Includes logic to prevent stagnation on a single high-density lane.
* **💻 Web Dashboard:** Provides a user-friendly web interface (built with Flask, HTML, CSS, JS) showing:
    * Live density percentage for each lane.
    * Current signal status (🟢 GREEN / 🔴 RED) for each lane.
    * Countdown timer for the active green light.

## 🛠️ Technology Stack

* **Programming Language:** Python 3.8+
* **Computer Vision:** OpenCV (`opencv-python`)
* **Object Detection:** Ultralytics YOLOv8
* **Web Backend:** Flask
* **Web Frontend:** HTML, CSS, JavaScript
* **Core Libraries:** NumPy
* **Environment:** Virtual Environment (`venv`)


## 🔧 Configuration

1.  Open the `utils.py` file.
2.  Locate the `LANE_ROIS` list.
3.  Modify the `(x, y, w, h)` tuples for each lane to accurately define the rectangular areas you want to monitor on your webcam feed. `(x, y)` is the top-left corner coordinate, `w` is the width, and `h` is the height.
    ```python
    # Example in utils.py
    LANE_ROIS = [
        (50, 250, 120, 200),   # ADJUST FOR YOUR LANE 1
        (200, 250, 120, 200),  # ADJUST FOR YOUR LANE 2
        (350, 250, 120, 200),  # ADJUST FOR YOUR LANE 3
        (500, 250, 120, 200),  # ADJUST FOR YOUR LANE 4
    ]
    ```
4.  You can use image editing tools or a simple OpenCV script (using `cv2.selectROI` on a frame from your camera) to help determine the correct coordinates.

5.  You can run 'opencv_app' file to run the traffic detection model from your setup of cameras or your Laptop/Desktop webcam.

## ▶️ Running the Application (To see the online Dashboard)

1.  Ensure your virtual environment is activated.
2.  Make sure your webcam is connected and accessible.
3.  Run the Flask backend:
    ```bash
    python backend.py
    ```
4.  The terminal will show output indicating the Flask server is running, typically on `http://127.0.0.1:5000/` or `http://localhost:5000/`. The background processing thread (camera capture, detection, etc.) will also start.
5.  Access the Dashboard: Open your web browser and navigate to the address provided by Flask (e.g., `http://127.0.0.1:5000`).

You should see the dashboard load, and the density/signal data will start updating automatically.

## 🚀 Future Work

* Implement live video streaming to the web dashboard.
* Improve density calculation (e.g., vehicle counting, tracking).
* Enhance the decision-making algorithm (consider wait times, prediction).
* Experiment with more accurate YOLOv8 models or fine-tuning.
* Add robustness for camera errors or processing failures.
* Explore automatic ROI calibration methods.
* Package for easier deployment (e.g., Docker).

## 🧑‍💻 Team Members
1. Satyam Singh
2. Komal Dahiya
3. Sakshi Singh
