from ultralytics import YOLO
import torch
import cv2
from utils import get_vehicle_class_indices


yolo_model = None
vehicle_class_indices = []
model_names = {}

def load_yolo_model(model_path='yolov8n.pt'):

    global yolo_model, vehicle_class_indices, model_names


    if yolo_model is None:
        print(f"Loading YOLOv8 model from {model_path}...")
        try:

            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"Using device: {device}")


            yolo_model = YOLO(model_path)
            yolo_model.to(device)


            model_names = yolo_model.names
            vehicle_class_indices = get_vehicle_class_indices(model_names)

            print("YOLOv8 model loaded successfully.")
            print(f"Tracking vehicle class indices: {vehicle_class_indices}")
            print(f"All class names: {model_names}")


            print("Warming up model...")
            dummy_image = torch.zeros(1, 3, 640, 640).to(device)
            _ = yolo_model(dummy_image, verbose=False)
            print("Model warmup complete.")

        except Exception as e:
            print(f"Error loading YOLO model: {e}")

            yolo_model = None
            model_names = {}
            vehicle_class_indices = []

    return yolo_model, model_names, vehicle_class_indices

def detect_vehicles(frame, model, class_indices_to_detect, conf_threshold=0.3):
    if model is None:
        print("Error: YOLO model is not loaded.")
        return None

    try:

        results = model(frame, classes=class_indices_to_detect, conf=conf_threshold, verbose=False)


        if results and isinstance(results, list):
            processed_results = results[0]
            if processed_results.boxes is not None:

                return processed_results.boxes.data.cpu().numpy()
            else:
                return []
        else:
             print("Warning: No results returned from YOLO model or unexpected format.")
             return []

    except Exception as e:
        print(f"Error during YOLO detection: {e}")
        return None
