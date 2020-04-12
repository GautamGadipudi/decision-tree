from classes import Question, DecisionNode, Leaf
from util import get_gini_impurity, get_info_gain, predict


def partition(rows: list, question: Question) -> (list, list):
    """
    Partition given rows into two(true_rows and false_rows) based on the question.
    :param rows: Rows to be partitioned.
    :type rows: list
    :param question: Question to be used for partitioning.
    :type question: Question
    :return: 2 item tuple of list if true rows and false rows.
    :rtype true_rows: list
    :rtype false_rows: list
    """
    true_rows = []
    false_rows = []
    for row in rows:
        if question.match(row):  # True
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def get_best_split(rows: list) -> (float, Question):
    """
    Get the best possible question and best possible info gain for a particular set of rows.
    :param rows: Rows on which to ask a question.
    :type rows: list
    :returns best_question: Best question that maximizes info gained
    :returns best_info_gain: Info gained on asking the best question
    :rtype best_info_gain: float
    :rtype best_question: Question
    """
    best_info_gain = 0
    best_question = None
    current_uncertainty = get_gini_impurity(rows)

    # minus 1 because we're ignoring the last column which is the label.
    n_attributes = len(rows[0]) - 1

    for col in range(n_attributes):

        # get all unique values for an attribute/column
        unique_values = set([row[col] for row in rows])

        for value in unique_values:
            question = Question(col, value)

            # Split rows depending on the question
            true_rows, false_rows = partition(rows, question)

            # We don't want to partition such rows
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Get info gain from this split
            info_gain = get_info_gain(false_rows, true_rows, current_uncertainty)

            if info_gain > best_info_gain:
                best_info_gain, best_question = info_gain, question

    return best_info_gain, best_question


def build_tree(rows: list) -> DecisionNode or Leaf:
    """
    Build the decision tree recursively.
    :param rows: Training data
    :type rows: list
    :return: Node
    :rtype: DecisionNode or Leaf
    """
    info_gain, question = get_best_split(rows)

    # If no info is gained just return a leaf node with remaining rows
    if info_gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, question)
    false_branch = build_tree(false_rows)
    true_branch = build_tree(true_rows)
    return DecisionNode(question, rows, true_branch, false_branch)


def get_tabs(n) -> str:
    """
    Get stringified tabs for alignment of trees.
    :param n: Number of tabs
    :type n: int
    :return: Stringified tabs
    :rtype: str
    """
    res = ''
    for i in range(n):
        res += '\t'
    return res


def print_tree(node, val='', tabs=0):
    """
    Print the decision tree
    :param node: Root node
    :type node: DecisionNode or Leaf
    :param val: True if right tree, False otherwise
    :type val: bool
    :param tabs: Stringified tabs for alignment of trees.
    :type tabs: int
    """
    align = get_tabs(tabs)
    if isinstance(node, Leaf):
        print(align + str(val))
        print(get_tabs(tabs), str(node))
        return
    print(align + str(val))
    print(align + str(node))
    print_tree(node.true_branch, True, tabs + 1)
    print_tree(node.false_branch, False, tabs + 1)


def classify(row, node) -> list:
    """
    Classify an example into a class/classes.
    :param row: Example/testing data
    :type row: list
    :param node: Node which has question/prediction
    :type node: DecisionNode or Leaf
    :return: List of possible classes
    :rtype: list
    """
    if isinstance(node, Leaf):
        return predict(node.predictions)

    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)
