def can_cover_desired_ranges(
    desired_distance_min,
    desired_distance_max,
    desired_light_min,
    desired_light_max,
    hardware_cameras,
):
    # Collect distances where camera availability can change.
    distance_boundaries = [desired_distance_min, desired_distance_max]

    for camera in hardware_cameras:
        camera_distance_min, camera_distance_max = camera[0]
        if desired_distance_min <= camera_distance_min <= desired_distance_max:
            distance_boundaries.append(camera_distance_min)

        if desired_distance_min <= camera_distance_max <= desired_distance_max:
            distance_boundaries.append(camera_distance_max)

    distance_boundaries = sorted(set(distance_boundaries))

    # Check each distance boundary and a midpoint between adjacent boundaries.
    distances_to_check = []

    for boundary_index in range(len(distance_boundaries) - 1):
        distances_to_check.append(distance_boundaries[boundary_index])

        distance_midpoint = (distance_boundaries[boundary_index]+ distance_boundaries[boundary_index + 1]) / 2
        distances_to_check.append(distance_midpoint)

    distances_to_check.append(distance_boundaries[-1])

    cameras_sorted_by_light_min = sorted(hardware_cameras, key=lambda camera: camera[1][0])

    for distance_to_check in distances_to_check:
        # Collect light ranges from cameras that support this distance.
        active_light_ranges = []

        for camera in cameras_sorted_by_light_min:
            camera_distance_min, camera_distance_max = camera[0]
            camera_light_range = camera[1]
            if camera_distance_min <= distance_to_check <= camera_distance_max:
                active_light_ranges.append(camera_light_range)

        if len(active_light_ranges) == 0:
            return False

        # Merge light ranges in order, checking for gaps in the desired range.
        covered_light_max = desired_light_min

        for light_min, light_max in active_light_ranges:
            if light_min > covered_light_max:
                return False

            covered_light_max = max(covered_light_max, light_max)

            if covered_light_max >= desired_light_max:
                break

        if covered_light_max < desired_light_max:
            return False

    return True


# Test case 1
# Expected: True
print(can_cover_desired_ranges(
    0, 10,
    0, 10,
    [
        [[0, 5], [0, 10]],
        [[5, 10], [0, 10]]
    ]
))

# Test case 2
# Expected: False
print(can_cover_desired_ranges(
    0, 10,
    0, 10,
    [
        [[0, 5], [0, 10]],
        [[6, 10], [0, 10]]
    ]
))
