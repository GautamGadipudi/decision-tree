from util import is_numeric

class Question:
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