def get_training_data(file_path, separator=',') -> list:
    """
    Get training data list from file
    :param file_path: Path of the file containing the dataset
    :param separator: Separator between values in the file
    :return: List of training data
    :rtype: list
    """
    try:
        training_data = []
        file = open(file_path, 'r')
        lines = file.readlines()
        for line in lines:
            training_data.append(line.replace('\n', '').split(separator))
    except IOError as e:
        print(e)
    finally:
        file.close()
        return training_data
