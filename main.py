from reader import get_training_data
from class_util import build_tree, print_tree, classify

if __name__ == '__main__':
    training_data = get_training_data('dataset.txt', ' ')
    node = build_tree(training_data)
    print_tree(node)
    example = ["False", "False", "True", "False", "False", "False", "False", "True"]
    x = classify(example, node)
    print(f'{str(example)} is one of types {x}')
