# from util import get_label_count


def is_numeric(value) -> bool:
    """
    Check if a value is of type int or float.
    :param value: Value whose datatype is to be checked.
    :return: True if value is of type int or float. False otherwise.
    :rtype: bool
    """
    return isinstance(value, int) or isinstance(value, float)

def get_label_count(rows: list) -> dict:
    """
    Get the count of occurrence of every label in the list of rows
    The actual label/class must be the last attribute in each item of list
    :param rows: List of examples from training data
    :type rows: list
    :return: Dictionary of label and it's count
    :rtype: dict
    """
    count = {}
    for row in rows:
        label = row[-1]
        if label not in count:
            count[label] = 1
        else:
            count[label] += 1
    return count

class Question:
    __slots__ = ['column', 'value']

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        """
        Match/check example with the question.
        :param example: A row/example to check against this question.
        :type example: list of values for all attributes.
        :return: True of match. False otherwise.
        :rtype: bool
        """
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __str__(self):
        comparator = '=='
        if is_numeric(self.value):
            comparator = '>='
        return f'{self.column} {comparator} {self.value}?'




class Leaf:
    __slots__ = ['predictions']

    def __init__(self, rows):
        self.predictions = get_label_count(rows)

    def __str__(self):
        return str(self.predictions)


class DecisionNode:
    __slots__ = ['question', 'predictions', 'true_branch', 'false_branch']

    def __init__(self, question, rows, true_branch, false_branch):
        self.question = question
        self.predictions = get_label_count(rows)
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __str__(self):
        return f'{str(self.question)} {str(self.predictions)}'
