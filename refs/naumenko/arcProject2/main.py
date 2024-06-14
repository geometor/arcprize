# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import json
import os
import numpy as np
from matplotlib import pyplot as plt
import pickle
from PIL import Image as im


def prep_img(arr):
    item_size = 40
    fill_color = [204, 255, 255]
    colors = [[0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 128, 255], [0, 0, 255], [255, 0, 255],
              [204, 102, 0], [255, 204, 255], [192, 192, 192]]
    img_w, img_h = len(arr), len(arr[0])
    data = np.zeros((img_h*item_size, img_w*item_size, 3), dtype=np.uint8)
    for j in range(img_h*item_size):
        for i in range(img_w*item_size):
            data[j, i] = colors[arr[i//item_size][j//item_size]]
            if (j/item_size - j//item_size > 0.8 or i/item_size - i//item_size > 0.8):
                data[j, i] = fill_color
    return data


# Define function to read tasks
def load_tasks(path):
    """
    Function to load .json files of tasks
    :param path: Path to folder where tasks are stored
    :return: - training and test tasks separated into a list of dictionaries
    where each entry is of the type {'input': [.task.], 'output': [.task.]}
    - list of file names
    """
    # Load Tasks
    # Path to tasks
    tasks_path = path
    # Initialize list to s
    # tore file names of tasks
    tasks_file_names = list(np.zeros(len(os.listdir(tasks_path))))
    # Initialize lists of lists of dictionaries to store training and test tasks
    # Format of items will be [{'input': array,'output': array},...,
    # {'input': array,'output': array}]
    tasks_count = len(os.listdir(tasks_path))
    train_tasks = list(np.zeros(tasks_count))
    test_tasks = list(np.zeros(tasks_count))
    # Read in tasks and store them in lists initialized above
    cnt = 1
    for i, file in enumerate(os.listdir(tasks_path)):
        with open(tasks_path + file, 'r') as f:
            task = json.load(f)
            tasks_file_names[i] = file
            train_tasks[i] = []
            test_tasks[i] = []
            # print("task begin\n", file=open('output.txt', 'a'))
            for t in task['train']:
                train_tasks[i].append(t)
                # print(np.matrix(t['input']), file=open('output.txt', 'a'))
                # print(np.matrix(t['output']), file=open('output.txt', 'a'))
                img = prep_img(t['input'])
                img2 = im.fromarray(img, 'RGB')
                img2.save('test' + str(cnt) + '.png')
                img = prep_img(t['output'])
                img2 = im.fromarray(img, 'RGB')
                img2.save('test' + str(cnt) + 'a.png')
                cnt = cnt + 1
            # print("task end\n", file=open('output.txt', 'a'))
            for t in task['test']:
                test_tasks[i].append(t)
    return train_tasks, test_tasks, tasks_file_names


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Read in evaluation tasks
    training_tasks, testing_tasks, file_names = load_tasks('training/')
    # Get number of test tasks for outputting progress later and define counter.
    num_test_tasks = len(testing_tasks)
    # print("num_test_tasks - " + str(num_test_tasks))

    counter = 0
    # Do some stuff to generate solution
    # Allocate space for overall solution
    solution = []
    # Iterate over all tasks to generate solution
    for test_task, task_filename in zip(testing_tasks, file_names):
        # Allocate space for solutions of task examples
        test = []
        # Store filename
        task_name = task_filename.strip('.json')
        # Iterate over test examples (1 or 2)
        for id_example, example in enumerate(test_task):
            pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
