import numpy as np


MIN_GREEN_TIME = 5
MAX_GREEN_TIME = 20
LOW_DENSITY_THRESHOLD = 10
ZERO_DENSITY_THRESHOLD = 0.1

def get_next_signal_state(densities, current_green_lane_index):

    num_lanes = len(densities)


    if not densities or num_lanes == 0:
        return 0, MIN_GREEN_TIME
    if num_lanes == 1:
        duration = MIN_GREEN_TIME + (MAX_GREEN_TIME - MIN_GREEN_TIME) * (densities[0] / 100.0)
        return 0, int(round(max(MIN_GREEN_TIME, min(duration, MAX_GREEN_TIME))))


    non_zero_density_indices = [i for i, d in enumerate(densities) if d >= ZERO_DENSITY_THRESHOLD]


    if not non_zero_density_indices:

        next_green_lane_index = (current_green_lane_index + 1) % num_lanes
        print(f"All lanes have zero density, cycling to Lane {next_green_lane_index + 1}")
        return next_green_lane_index, MIN_GREEN_TIME

    non_zero_densities = [densities[i] for i in non_zero_density_indices]
    relative_max_index = np.argmax(non_zero_densities)
    highest_density_lane_index = non_zero_density_indices[relative_max_index]
    max_density = densities[highest_density_lane_index]

    next_green_lane_index = highest_density_lane_index

    if highest_density_lane_index == current_green_lane_index and len(non_zero_density_indices) > 1:
        sorted_non_zero_indices = sorted(non_zero_density_indices, key=lambda i: densities[i], reverse=True)

        if len(sorted_non_zero_indices) > 1:
            second_highest_lane_index = sorted_non_zero_indices[1]
            print(f"Current green (Lane {current_green_lane_index + 1}) still max non-zero density, switching to second highest (Lane {second_highest_lane_index + 1})")
            next_green_lane_index = second_highest_lane_index

    winning_density = densities[next_green_lane_index]

    green_duration = MIN_GREEN_TIME + (MAX_GREEN_TIME - MIN_GREEN_TIME) * (winning_density / 100.0)

    green_duration = max(MIN_GREEN_TIME, min(green_duration, MAX_GREEN_TIME))

    print(f"Decision Logic: Densities={ [f'{d:.1f}' for d in densities] }, NonZeroIndices={non_zero_density_indices}, CurrentGreen={current_green_lane_index + 1} -> NextGreen={next_green_lane_index + 1}, Duration={int(round(green_duration))}s")

    return next_green_lane_index, int(round(green_duration))
