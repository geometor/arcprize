import json
import os

# Load JSON data
with open('arc-agi_test_challenges.json') as f:
    data = json.load(f)

# Create a directory for the files
folder_name = 'arc-agi_test_challenges'
os.makedirs(folder_name, exist_ok=True)

# Iterate through the JSON entries
for index, (key, content) in enumerate(data.items()):
    # Create a subdirectory for each key
    subfolder_name = os.path.join(folder_name, f'{index:03d}-{key}')
    os.makedirs(subfolder_name, exist_ok=True)

    # Save the 'train' data
    if 'train' in content:
        for train_index, train_entry in enumerate(content['train']):
            filename = os.path.join(subfolder_name, f'{train_index:03d}-train.txt')
            with open(filename, 'w') as f:
                for train_key, train_value in train_entry.items():
                    f.write(f'{train_key}:\n')
                    for row in train_value:
                        f.write(' '.join(map(str, row)) + '\n')
                    f.write('\n')

    # Save the 'test' data
    if 'test' in content:
        for test_index, test_entry in enumerate(content['test']):
            filename = os.path.join(subfolder_name, f'{test_index:03d}-test.txt')
            with open(filename, 'w') as f:
                for test_key, test_value in test_entry.items():
                    f.write(f'{test_key}:\n')
                    for row in test_value:
                        f.write(' '.join(map(str, row)) + '\n')
                    f.write('\n')

