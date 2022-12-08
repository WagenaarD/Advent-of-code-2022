"""
Advent of code challenge 2022
Start  - forgot
Part 1 - forgot - 1700
Part 2 - 20:30  - 470596
"""

input_lines = open('input.txt').read().split('\n')


def get_tree_lines(row, col, height):
    return (
        height[row][:col][::-1],
        height[row][col+1:],
        [x[col] for x in height[:row]][::-1],
        [x[col] for x in height[row+1:]]
    )


def get_visibility(row, col, height):
    for tree_line in get_tree_lines(row, col, height):
        if not any([tree >= height[row][col] for tree in tree_line]):
            return True
    return False


def get_scenic_score(row, col, height):
    score = 1
    for trees in (
        height[row][:col][::-1],
        height[row][col+1:],
        [x[col] for x in height[:row]][::-1],
        [x[col] for x in height[row+1:]],
    ):
        for idx in range(len(trees)):
            if trees[idx] >= height[row][col]:
                score *= (idx + 1)
                break
        else:
            score *= len(trees)
    return score



tree_height = [[int(char) for char in line] for line in input_lines]
# visible_trees = [[False for _ in range(len(input_lines))] for __ in range(len(input_lines[0]))]

# for row in range(len(tree_height)):
#     min_height = -1
#     for col in range(len(tree_height[row])):
#         if tree_height[row][col] > min_height:
#             visible_trees[row][col] = True
#             min_height = tree_height[row][col]
#     min_height = -1
#     for col in range(len(tree_height[row]))[::-1]:
#         if tree_height[row][col] > min_height:
#             visible_trees[row][col] = True
#             min_height = tree_height[row][col]
# for col in range(len(tree_height[0])):
#     min_height = -1
#     for row in range(len(tree_height)):
#         if tree_height[row][col] > min_height:
#             visible_trees[row][col] = True
#             min_height = tree_height[row][col]
#     min_height = -1
#     for row in range(len(tree_height))[::-1]:
#         if tree_height[row][col] > min_height:
#             visible_trees[row][col] = True
#             min_height = tree_height[row][col]

visible_trees = [get_visibility(row, col, tree_height) for row in range(len(tree_height)) for col in range(len(tree_height[0]))]


max_scenic_score = 0
for row in range(len(tree_height)):
    for col in range(len(tree_height[row])):
        max_scenic_score = max(max_scenic_score, get_scenic_score(row, col, tree_height))

# Visualize our result
# print('\n'.join([''.join(['■' if vis else '.' for vis in line]) for line in visible_trees]))

# print('Part 1:', sum([row.count(True) for row in visible_trees]))
print('Part 1:', sum(visible_trees))
print('Part 2:', max_scenic_score)
