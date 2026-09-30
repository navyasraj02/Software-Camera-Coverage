def func(desired_x_min, desired_x_max, desired_y_min, desired_y_max, hardware_cam_list):
    # Collect X boundaries
    x_points = [desired_x_min, desired_x_max]

    for cam in hardware_cam_list:
        if desired_x_min <= cam[0][0] <= desired_x_max:
            x_points.append(cam[0][0])

        if desired_x_min <= cam[0][1] <= desired_x_max:
            x_points.append(cam[0][1])

    x_points = sorted(set(x_points))

    # Check boundaries and midpoints
    points_to_check = []

    for i in range(len(x_points) - 1):
        points_to_check.append(x_points[i])

        midpoint = (x_points[i] + x_points[i + 1]) / 2
        points_to_check.append(midpoint)

    points_to_check.append(x_points[-1])

    for desired_x in points_to_check:

        # Find cameras active at this X
        active_cams = []

        for hardware_cam in hardware_cam_list:
            if hardware_cam[0][0] <= desired_x <= hardware_cam[0][1]:
                active_cams.append(hardware_cam[1])

        if len(active_cams) == 0:
            return False

        active_cams.sort(key=lambda x: x[0])

        # Check continuous Y coverage
        covered_y = desired_y_min

        for cam in active_cams:

            if cam[0] > covered_y:
                return False

            covered_y = max(covered_y, cam[1])

            if covered_y >= desired_y_max:
                break

        if covered_y < desired_y_max:
            return False

    return True

# Test case 1: Return True
print(func(
    0, 10,
    0, 10,
    [
        [[0, 5], [0, 10]],
        [[5, 10], [0, 10]]
    ]
))

# Test case 2: Return False
print(func(
    0, 10,
    0, 10,
    [
        [[0, 5], [0, 10]],
        [[6, 10], [0, 10]]
    ]
))