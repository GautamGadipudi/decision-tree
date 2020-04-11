from util import is_numeric, get_label_count

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


class Leaf:
    __slots__ = ['rows']

    def __init__(self, rows):
        self.predictions = get_label_count(rows)


class DecisionNode:
    __slots__ = ['question', 'true_branch', 'false_branch']

    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
