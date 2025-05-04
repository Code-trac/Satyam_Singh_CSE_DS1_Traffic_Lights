import numpy as np

def calculate_lane_density(detections_in_lanes, rois):

    densities = []

    for i, lane_detections in enumerate(detections_in_lanes):

        roi_x, roi_y, roi_w, roi_h = rois[i]

        roi_area = roi_w * roi_h
        if roi_area == 0:
            densities.append(0.0)
            continue


        total_vehicle_area = 0
        for det in lane_detections:
            x1, y1, x2, y2 = det['bbox']

            bbox_area = (x2 - x1) * (y2 - y1)
            total_vehicle_area += bbox_area

        density = min((total_vehicle_area / roi_area) * 100, 100.0)
        densities.append(density)

    return densities
