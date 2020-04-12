from util import get_label_count, is_numeric


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
