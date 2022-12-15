"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 4737443 (ex 26)
Part 2  - 11482462818989 (ex 56000011) (18s)
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import re
from pprint import pprint


def can_be_beacon(x: int, y: int, sensors: list) -> bool:
    for (sx, sy, sd) in sensors:
        coord_distance = abs(sx - x) + abs(sy - y)
        if coord_distance <= sd:
            return False
    return True


@print_function(run_time = True)
def solve_part_1(int_line: list) -> int:
    y_target = 10 if len(int_lines) <= 14 else 2000000
    blocked = set()
    beacons = set()
    for xs, ys, xb, yb in int_lines:
        d_beacon = abs(xb - xs) + abs(yb - ys)
        d_row = abs(y_target - ys)
        for x in range(xs - (d_beacon - d_row), xs + (d_beacon - d_row) + 1):
            blocked.add(x)
        if yb == y_target:
            beacons.add(xb)
    return len(blocked - beacons)


@print_function(run_time = True)
def solve_part_2(int_lines: list, print_progress: bool = True) -> int:
    """
    # The following is already too slow, we need to find a quicker way for part 2!:
    for x in range(xy_max + 1):
        for y in range(xy_max + 1):
            x + y
    
    Instead we scan only the edges of the sensor ranges. We start at sensors with a shorter range
    """
    
    xy_max = 20 if len(int_lines) == 14 else 4000000
    sensors = [(s[0], s[1], abs(s[0] - s[2]) + abs(s[1] - s[3])) for s in int_lines]
    sensors.sort(key = lambda x: x[2])
    for idx, (sx, sy, sd) in enumerate(sensors):
        print('Progress = {:%}'.format(idx / len(sensors)))
        for x in range(sx - (sd + 1), sx + (sd + 1) + 1):
            if not 0 <= x <= xy_max:
                continue
            dy = (sd + 1) - abs(x - sx)
            for y in {sy - dy, sy + dy}:
                if 0 <= y <= xy_max:
                    if can_be_beacon(x, y, sensors):
                        return x * 4000000 + y

@print_function(run_time = True)
def solve_part_v2(int_lines: list) -> int:
    xy_max = 20 if len(int_lines) <= 14 else 4000000
    sensors_xy = [(s[0], s[1], abs(s[0] - s[2]) + abs(s[1] - s[3])) for s in int_lines]
    sensors_uv = [(sx - d + sy, sx - d - sy, d * 2) for sx, sy, d in sensors_xy]
    
    # sensor_lambdas = []
    # for us, vs, ds, in sensors_uv:
    #     # Trick: We need to assign default categories to avoid them being overwritten later. The default
    #     # parameters are stored in the lambda object, global variables at the time of creation are not.
    #     sensor_lambdas.append(lambda u, v, u_0 = us, v_0 = vs, d = ds: (0 <= u - u_0 <= d) and (0 <= v - v_0 <= d))

    # # Part 1:
    # y_target = 10 if len(int_lines) <= 14 else 2000000
    # beacons = {(line[2], line[3]) for line in int_lines}
    # min_x = min([xs - db for xs, ys, db, in sensors_xy])
    # max_x = max([xs + db for xs, ys, db, in sensors_xy])
    # # pprint(sensors)
    # # print('min_x', min_x)
    # # print('max_x', max_x)
    # blocked = 0
    # impossible_x = []
    # for x in range(min_x, max_x + 1):
    #     if (x, y_target) in beacons:
    #         continue
    #     if not can_be_beacon_uv(x + y_target, x - y_target, sensor_lambdas):
    #         impossible_x.append(x)
    #         blocked += 1
    # print('Part 1:', blocked)
    # # print(impossible_x)
    
    # # Works but not faster :-(
    # for idx, (su, sv, d) in enumerate(sensors_uv):
    #     print('Progress = {:%}'.format(idx / len(sensors_uv)))
    #     potential_beacons = \
    #         [(u,      sv - 1)     for u in range(su - 1, su + d + 3, 2)] + \
    #         [(u,      sv + d + 1) for u in range(su - 1, su + d + 3, 2)] + \
    #         [(su - 1, v)          for v in range(sv + 1, sv + d + 1, 2)] + \
    #         [(su + d + 1, v)  for v in range(sv + 1, sv + d + 1, 2)]
    #     print(sensors_xy[idx], len(potential_beacons))
    #     for u, v in potential_beacons:            
    #         if not (0 <= (u + v) // 2 <= xy_max and 0 <= (u - v) // 2 <= xy_max):
    #             continue
    #         if can_be_beacon_uv(u, v, sensor_lambdas):
    #             x, y = (u + v) // 2, (u - v) // 2
    #             print('Part 2:', x * 4000000 + y)
    #             return
    # print('Part 2:', 'No result found')

    # This could be quicker? But not really
    for u in range(0, xy_max):  # Needs to be updated, only works up to half
        if u % 100000 == 0:
            print('Progress = {:%}'.format(u / xy_max / 2))
        v_bounds = get_v_bounds_for_u(u, sensors_uv)
        # vmin = - u # Needs to be updated, only works up to half
        # vmax = vmin
        total_upper = -u  # Needs to be updated, only works up to half
        for lower, upper in v_bounds:
            if not lower <= total_upper:
                v = total_upper
                x, y = (u + v) // 2, (u - v) // 2
                print('Part 2:', x * 4000000 + y)
                print(u, v, x, y)
                return
            total_upper = max(total_upper, upper)
        if total_upper < u:  # Needs to be updated, only works up to half
            v = total_upper
            
            x, y = (u + v) // 2, (u - v) // 2
            print('Part 2:', x * 4000000 + y)
            print(u, v, x, y)
            return



        # x = (u + v) // 2
        # y = (u - v) // 2
         
        # min_x = 0
        # min_x = (u + min_v) // 2
        # min_v = min_x * 2 - u = -u
        
        




def get_v_bounds_for_u(u, sensors_uv):
    # output = []
    # for us, vs, d, in sensors_uv:
    #     if us <= u <= us + d:
    #         output.append((vs, vs + d))
    # return output
    output = [(vs, vs + d) for us, vs, d, in sensors_uv if us <= u <= us + d]
    return sorted(output, key = lambda x: x[0])


def can_be_beacon_uv(u, v, sensor_lambdas):
    for sensor in sensor_lambdas:
        if sensor(u, v):
            return False
    else:
        return True



lines = sys.stdin.read().strip().split('\n')
int_lines = [list(map(int, re.findall('-?[0-9]+', line))) for line in lines]
solve_part_v2(int_lines)

# # int_lines = int_lines[6:7]
# # print('Part 1:', solve_part_1(int_lines))
# # print('Part 1:', solve_part_2(int_lines))
# beacons = {(line[2], line[3]) for line in int_lines}

# # sensors = [(s[0], s[1], abs(s[0] - s[2]) + abs(s[1] - s[3])) for s in int_lines]
# sensors = [(s[0], s[1], abs(s[0] - s[2]) + abs(s[1] - s[3])) for s in int_lines]
# sensor_lambdas = []
# for xs, ys, db, in sensors:
#     u_0 = xs - db + ys
#     v_0 = xs - db - ys
#     # Trick: We need to assign default categories to avoid them being overwritten later. The default
#     # parameters are stored in the lambda object, global variables at the time of creation are not.
#     sensor_lambdas.append(lambda u, v, u_0 = u_0, v_0 = v_0: (0 <= u - u_0 <= 0 + 2 * db) and (0 <= v - v_0 <= 2 * db))

# # @print_function()
# # def can_be_beacon(x, y):
# #     u, v = x + y, x - y
# #     # for sensor in sensor_lambdas:
# #     for idx, sensor in enumerate(sensor_lambdas):
# #         # print(x, y, u, v, idx, sensor(u, v))
# #         if sensor(u, v):
# #             return False
# #     else:
# #         return True

# # [(2, 18, 7),
# #  (9, 16, 1),
# #  (13, 2, 3),
# #  (12, 14, 4),
# #  (10, 20, 4),
# #  (14, 17, 5),
# #  (8, 7, 9), <------
# #  (2, 0, 10),
# #  (0, 11, 3),
# #  (20, 14, 8),
# #  (17, 20, 6),
# #  (16, 7, 5),
# #  (14, 3, 1),
# #  (20, 1, 7)]


# # Part 1:
# y_target = 10 if len(int_lines) <= 14 else 2000000
# min_x = min([xs - db for xs, ys, db, in sensors])
# max_x = max([xs + db for xs, ys, db, in sensors])
# # pprint(sensors)
# # print('min_x', min_x)
# # print('max_x', max_x)
# blocked = 0
# for x in range(min_x, max_x + 1):
#     if (x, y_target) in beacons:
#         continue
#     if not can_be_beacon(x, y_target):
#         blocked += 1
# print('Part 1:', blocked)


# # # Part 2:
# xy_max = 20 if len(int_lines) <= 14 else 4000000
# for idx, (sx, sy, sd) in enumerate(sensors):
#     # print('Progress = {:%}'.format(idx / len(sensors)))
#     u_0 = xs - db + ys
#     v_0 = xs - db - ys
#     to_check = set()
#     for u in range(u_0 - 1, u_0 + 2 * db + 2):

    
#     for x in range(sx - (sd + 1), sx + (sd + 1) + 1):
#         if not 0 <= x <= xy_max:
#             continue
#         dy = (sd + 1) - abs(x - sx)
#         for y in {sy - dy, sy + dy}:
#             if 0 <= y <= xy_max:
#                 if can_be_beacon(x, y, sensors):
#                     return x * 4000000 + y
# # for idx, (sx, sy, sd) in enumerate(sensors):




