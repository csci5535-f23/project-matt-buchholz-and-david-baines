from data_loader import load_dataset



def generate_statistics():

    train, test = load_dataset()
    split = 0
    data_sets = [train, test]
    for data in data_sets:
        for _, row in data.iterrows():
            split += len(row['contents'].split('\n'))

    print(f'Files: {len(train) + len(test)}')
    print(f'LOC: {split}')
    return


if __name__ == '__main__':
    #generate_statistics()