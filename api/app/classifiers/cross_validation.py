import random


def allowed_extensions():
    '''Returns a list of allowed extensions'''
    return ['csv', 'tsv']


def train_test_split(data_folder, filename, split_pct=0.9):
    '''Returns True if successfully split file into train and test files'''
    # Check file extension
    file_ext = filename.split('.')[-1]
    if file_ext not in allowed_extensions():
        return False, file_ext + ' not supported'

    # Build filenames for train and test with their folder location
    ext_len = len(file_ext) + 1
    base_name = filename[:-ext_len]
    if data_folder[-1] != '/':
        data_folder += '/'
    source_file = base_name + '.' + file_ext
    train_file = 'train/' + base_name + '-train.' + file_ext
    test_file = 'test/' + base_name + '-test.' + file_ext

    # Read the file and split the file into train and test
    with open(data_folder + source_file, "rb") as f:
        data = f.readlines()
    random.seed(10)
    random.shuffle(data)

    split_idx = int(len(data) * split_pct)
    train_data = data[:split_idx]
    test_data = data[split_idx:]

    # Save the Train and Test files
    with open(data_folder + train_file, "w") as f:
        f.writelines(train_data)

    with open(data_folder + test_file, "w") as f:
        f.writelines(test_data)
    # Success
    return train_file, test_file
