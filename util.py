from classes import Question, Leaf, DecisionNode


def get_gini_impurity(rows: list) -> float:
    """
    Get gini impurity for a list of rows
    The actual label/class must be the last attribute in each item of list
    :param rows: List of examples from training data
    :type rows: list
    :returns: Gini impurity(between 0 and 1) for the provided list. Lesser the better.
    :rtype: float
    """
    impurity = 1
    total_rows = len(rows)
    label_count = get_label_count(rows)
    for label in label_count:
        probability = label_count[label] / total_rows
        impurity -= probability**2
    return impurity


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


def get_info_gain(false_rows: list, true_rows: list, current_uncertainity: float) -> float:
    """
    Get a measure of info gained when split as given true rows and false rows.
    :param false_rows: Rows that are false for a particular question.
    :type false_rows: list
    :param true_rows: Rows that are true for a particular question.
    :type true_rows: list
    :param current_uncertainity: Gini impurity of current node
    :type current_uncertainity: float
    :return: Info gained. The greater the better.
    :rtype: float
    """
    # Probability of False
    p = len(false_rows) / (len(false_rows) + len(true_rows))
    info_gain = current_uncertainity - (p * get_gini_impurity(false_rows) + (1 - p) * get_gini_impurity(true_rows))
    return info_gain


def is_numeric(value) -> bool:
    """
    Check if a value is of type int or float.
    :param value: Value whose datatype is to be checked.
    :return: True if value is of type int or float. False otherwise.
    :rtype: bool
    """
    return isinstance(value, int) or isinstance(value, float)


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
    return DecisionNode(question, true_branch, false_branch)