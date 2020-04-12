from util import build_tree, print_tree


try:
    data_set_file = open('dataset.txt', 'r')
    lines = data_set_file.readlines()
    training_data = []
    for line in lines:
        training_data.append(line.replace('\n', '').split(' '))

    node = build_tree(training_data)
    print_tree(node)
except Exception as e:
    print(e)
