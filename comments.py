import os

directory = '/Users/marckwinbristhole/pyChess-master'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
            with open(file_path, 'w') as f:
                for line in lines:
                    # remove '#' comments
                    line = line.split('#')[0].rstrip() + '\n'
                    if line.strip():  # skip writing empty lines
                        # remove multi-line comments enclosed in triple-quotes
                        f.write(line)
