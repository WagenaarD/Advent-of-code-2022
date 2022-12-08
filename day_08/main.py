"""
Advent of code challenge 2022
Start  - forgot
Part 1 - forgot - 1700
Part 2 - 20:30  - 470596
"""

input_lines = open('input.txt').read().split('\n')

tree_height = [[int(char) for char in line] for line in input_lines]

no_visible_trees, max_scenic_score = 0, 0
for row in range(len(tree_height)):
    for col in range(len(tree_height[0])):
        score, visible = 1, False
        for tree_line in (
            tree_height[row][:col][::-1],
            tree_height[row][col+1:],
            [x[col] for x in tree_height[:row]][::-1],
            [x[col] for x in tree_height[row+1:]]
        ):
            if not any([tree >= tree_height[row][col] for tree in tree_line]):
                visible = True
            for idx in range(len(tree_line)):
                if tree_line[idx] >= tree_height[row][col]:
                    score *= (idx + 1)
                    break
            else:
                score *= len(tree_line)
        no_visible_trees += visible
        max_scenic_score = max(max_scenic_score, score)

print('Part 1:', no_visible_trees)
print('Part 2:', max_scenic_score)