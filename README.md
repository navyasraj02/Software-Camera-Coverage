# Software Camera Coverage

Checks whether the hardware cameras together cover the full desired range of subject distances and light levels for software camera.

## Function

```python
def can_cover_desired_ranges(
    desired_distance_min,
    desired_distance_max,
    desired_light_min,
    desired_light_max,
    hardware_cameras,
):
```

- `desired_distance_min`, `desired_distance_max`: subject distance range of software camera
- `desired_light_min`, `desired_light_max`: light level range of software camera
- `hardware_cameras`: list of hardware cameras

Each hardware camera is:

```text
[[distance_min, distance_max], [light_min, light_max]]
```
where
- `distance_min`, `distance_max`: subject distance range of the hardware camera
- `light_min`, `light_max`: light level range of the hardware camera

Ranges are inclusive.

## Algorithm
The aim of this algorithm is to check for every desired distance and light level, do we have atleast one hardware camera that can satisfy the criteria. Let's assume an X-Y coordinate system with X-axis covering subject distance and Y-axis covering light level. Each camera (software or hardware) has the range of subject distance and light level it supports. Therefore, we can map the camera onto this 2D plane with 4 points (2 points for distance and 2 points for light levels). Now, we can visualize every camera as a rectangle in this 2D plane. The question now becomes: does the given list of hardware cameras (visualized as rectangles) cover the entire software camera rectangle.

At high level, the solution first selects some important distances (checkpoints) in the X-axis. Then, at each such distance, it checks whether the available cameras cover the entire required light range in the Y-axis.

### Detailed Description
1. Initialize a list of important distances `distance_boundaries` and add `desired_distance_min`, `desired_distance_max` to that list.
2. For each hardware camera, check if its `distance_min` and `distance_max` fall within the desired range. If yes, then add them to `distance_boundaries`. The reason behind collecting these points is that these are the points where a camera can start or stop being available. 
3. In order to remove duplicates and traverse them in an increasing order, we convert this list into a set and sort them.
4. Now, create a new list `distances_to_check` from `distance_boundaries`, which will contain the distances that will be actually checked.
5. Traverse through `distance_boundaries` in pair-wise manner. Add the current boundary and midpoint between current and next boundary to `distances_to_check`. The reason behind adding the midpoint is to check the light coverage for that gap. We can safely say that no camera would start or stop inside that gap. Only the same cameras will be available throughout that gap. Hence, this addition covers that edge case.
6. Sort the cameras by minimum light level they support to form `cameras_sorted_by_light_min`.
7. Traverse through `distances_to_check`. For each distance, create a list of active light ranges of cameras, `active_light_ranges` that work at that particular subject distance.
8. Check whether the camera's distance is within the desired range. If yes, then append its light range to `active_light_ranges`. If no camera works at this distance, then return False.
9. Next step is to check for light coverage for the current subject distance. Start by initializing `covered_light_max` to `desired_light_min`. This variable keeps track of how far we have reached along Y-axis without a gap.
10. For each light range, if the `light_min` of current camera is greater than `covered_light_max`, then it indicates a gap in the coverage. Since all the ranges are sorted, no other camera can fill this gap. Therefore, return False.
11. `covered_light_max` is set to the maximum value between `covered_light_max` or `light_max` of current hardware camera.
12. If `covered_light_max` equals or exceeds `desired_light_max`, break out of the light-range loop.
13. Check that if `covered_light_max` is less than `desired_light_max`. If yes, it means there's some gap left in the desired light level range that no cameras could satisfy, Hence, return False.
14. If all the checks are passed, return True.
    
## Test Cases

```python
# Test case 1
# Expected: True
print(func(
    0, 10,
    0, 10,
    [
        [[0, 5], [0, 10]],
        [[5, 10], [0, 10]]
    ]
))

# Test case 2
# Expected: False
print(func(
    0, 10,
    0, 10,
    [
        [[0, 5], [0, 10]],
        [[6, 10], [0, 10]]
    ]
))
```
