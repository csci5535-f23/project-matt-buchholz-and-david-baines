import pandas as pd
import os
from sklearn.model_selection import train_test_split

PICKLE_DIR = 'pickled_data/'
PICKLE_NAME = 'codenet.pkl'
PYTHON_CODENET_DIR = 'python_codenet/'


def build_dataset_from_files() -> pd.DataFrame:
    files = os.listdir(PYTHON_CODENET_DIR)

    file_contents = []
    for file in files:
        with open(PYTHON_CODENET_DIR + file, 'r', encoding='utf-8') as infile:
            file_contents.append("\n".join(infile.readlines()))

    files_and_contents = zip(files, file_contents)
    dataset = pd.DataFrame(files_and_contents, columns=['file', 'contents'])
    return dataset


def load_dataset(use_pickle=True, random_state=5535, drive_prefix=''):
    file_path = drive_prefix + PICKLE_DIR + PICKLE_NAME
    if os.path.exists(file_path) and use_pickle:
        dataset = pd.read_pickle(file_path)
    else:
        dataset = build_dataset_from_files()

    dataset.to_pickle(path=file_path)

    train, test = train_test_split(dataset, test_size=0.2, random_state=random_state)
    return train, test
