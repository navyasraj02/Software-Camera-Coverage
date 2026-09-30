# Software Camera Coverage

Checks whether the hardware cameras together cover the full desired range of subject distances and light levels for software camera.

## Function

```python
func(desired_x_min, desired_x_max, desired_y_min, desired_y_max, hardware_cam_list)
```

- `desired_x_min`, `desired_x_max`: required subject distance range of software camera
- `desired_y_min`, `desired_y_max`: required light level range of software camera
- `hardware_cam_list`: list of hardware cameras

Each hardware camera is:

```text
[[x_min, x_max], [y_min, y_max]]
```
where
- `x_min`, `x_max`: subject distance range of the hardware camera
- `y_min`, `y_max`: light level range of the hardware camera

Ranges are inclusive.

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
