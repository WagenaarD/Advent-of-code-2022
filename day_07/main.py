"""
Advent of code challenge 2022

Not really competetive with time today, spread coding over multiple sessions
Start  - 18:09 
Part 1 - 19:58
Part 2 - 
"""


class FileFolder:
    def __init__(self, isdir: bool, name: str, size: int = None) -> None:
        self.name, self.isdir, self.file_size = name, isdir, size
        if isdir:
            self.content = []
    
    def add_to_folder(self, other) -> None:
        self.content.append(other)
    
    @property
    def size(self) -> int:
        if self.isdir:
            return sum([item.size for item in self.content])
        else:
            return int(self.file_size)

    def __str__(self) -> str:
        if not self.isdir:
            return '- {} (file, size = {})'.format(self.name, self.size)
        else:
            # return '- {} (dir)\n  '.format(self.name) + \
            return '- {} (dir, size = {})\n  '.format(self.name, self.size) + \
                '\n  '.join('\n'.join([str(item) for item in self.content]).split('\n'))
    
    def __repr__(self) -> str:
        return '<FileFolder, "{}" {}>'.format(self.name, '(dir)' if self.isdir else '(file)')
    
    def get_dirs(self) -> list:
        return [self] + sum([item.get_dirs() for item in self.content if item.isdir], [])


def process_input(input_lines):
    base_folder = FileFolder(True, '/')
    print(base_folder)
    stack = [base_folder]
    idx = 0
    while idx < len(input_lines):
        print('Command: ' + input_lines[idx])
        if input_lines[idx] == '$ cd /':
            stack = [base_folder]
        elif input_lines[idx] == '$ ls':
            while idx < len(input_lines) - 1:
                if input_lines[idx+1][0] == '$':
                    break
                elif input_lines[idx+1][:4] == 'dir ':
                    print('Ignoring: ' + input_lines[idx+1])
                    idx += 1
                else:
                    print('Adding: ' + input_lines[idx+1])
                    stack[-1].add_to_folder(FileFolder(False, *input_lines[idx + 1].split()[::-1]))
                    idx += 1
        elif input_lines[idx] == '$ cd ..':
            stack.pop()
        elif input_lines[idx].startswith('$ cd '):
            new_folder = FileFolder(True, input_lines[idx][5:])
            stack[-1].add_to_folder(new_folder)
            stack.append(new_folder)
        print('Stack: ' + repr(stack))
        idx += 1
    return base_folder


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    base_folder = process_input(open('input.txt').read().split('\n'))
    # base_folder = process_input(open('test_input.txt').read().split('\n'))
    print(base_folder)
    print(base_folder.get_dirs())

    # Part 1: Find all of the directories with a total size of at most 100000. What is the sum of 
    # the total sizes of those directories?
    print('\n'.join([repr(dir) for dir in base_folder.get_dirs() if dir.size <= 100000]))
    print('Part 1 result: {}'.format(sum([dir.size for dir in base_folder.get_dirs() if dir.size <= 100000])))