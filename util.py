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


def predict(predictions: dict) -> list:
    """
    Predict the class using the key with highest value
    :param predictions: Dictionary of label and its count
    :type predictions: dict
    :return: List of possible predictions
    :rtype: list
    """
    best_count = 0
    result = []
    for label in predictions:
        if predictions[label] > best_count:
            result.clear()
            result.append(label)
            best_count = predictions[label]
        elif predictions[label] == best_count:
            result.append(label)
    return result


