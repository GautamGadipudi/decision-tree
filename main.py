from util import get_gini_impurity

def convert_to_bool(string):
    return string == 'True'

try:
    data_set_file = open('dataset.txt', 'r')
    lines = data_set_file.readlines()
    training_data = []
    for line in lines:
        training_data.append(line.replace('\n', '').split(' '))

    gini_impurity = get_gini_impurity(training_data)
    print(gini_impurity)
except Exception as e:
    print(e)

