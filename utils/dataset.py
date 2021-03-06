import csv
import numpy as np
import os


def convert_to_one_hot(raw_target):
    n_uniques = len(np.unique(raw_target))
    one_hot_target = np.zeros((raw_target.shape[0], n_uniques))
    one_hot_target[np.arange(raw_target.shape[0]), raw_target.astype(np.int)] = 1
    return one_hot_target.astype(np.int32)

def load_fer(dataset = 0, one_hot = True, flat = True, expand = False, augment = False, subtract_mean = True):
    '''
    Loads the FER Dataset from memory and returns the dataset.
    The fer2013.csv file needs to be extracted and placed under data/fer2013.csv. The labels can be converted
    to one-hot encoding.

    :param dataset: selects which dataset to load - 0 = Train, 1 = Validation, 2 = Test
    :param one_hot: True returns the labels as one hot encoding
    :param flat: gives flattend version of the array
    :param expand: expands the grayscale image to three channels - just copy the one
    :return: A dict with `data` and `target` keys.
    '''


    dest_file = 'utils/data/fer2013.csv'
    delimiter = ','
    firstline = True
    i = 0
    training_labels = []
    training_images = []
    validation_labels = []
    validation_images = []
    test_labels = []
    test_images = []
    mean_image = np.load('utils/mean.npz')
    mean_image = mean_image['mean']
    with open(dest_file, 'r') as dest_f:
        data_iter = csv.reader(dest_f,
                            delimiter = delimiter,
                            quotechar = '"')
        for data in data_iter:
            i += 1
            if firstline:
                firstline = False
                continue
            elif i < 28710:
                training_labels.append(float(data[0]))
                if flat:
                    training_images.append(np.fromstring(data[1], dtype=int, sep=' '))
                else:
                    training_images.append(np.reshape(np.fromstring(data[1], dtype=int, sep=' '),[48,48]))
            elif i < 32299:
                validation_labels.append(float(data[0]))
                if flat:
                    validation_images.append(np.fromstring(data[1], dtype=int, sep=' '))
                else:
                    validation_images.append(np.reshape(np.fromstring(data[1], dtype=int, sep=' '), [48, 48]))
            else:
                test_labels.append(float(data[0]))
                if flat:
                    test_images.append(np.fromstring(data[1], dtype=int, sep=' '))
                else:
                    test_images.append(np.reshape(np.fromstring(data[1], dtype=int, sep=' '), [48, 48]))


    if dataset == 0:
        training_images = np.asarray(training_images)
        training_images = np.reshape(training_images, (-1, 1, 48, 48))
        if subtract_mean:
            training_images = training_images - mean_image
        training_labels = np.asarray(training_labels, dtype=np.int32)
        if augment:
            flipped_images = np.flip(training_images, 3)
            training_images = np.append(training_images, flipped_images, axis=0)
            training_labels = np.append(training_labels, training_labels, axis=0)
        if one_hot:
            training_labels = convert_to_one_hot(training_labels)
        fer = {'data': training_images, 'target': training_labels}
    elif dataset == 1:
        validation_images = np.asarray(validation_images)
        validation_images = np.reshape(validation_images, (-1, 1, 48, 48))
        if subtract_mean:
            validation_images = validation_images - mean_image
        validation_labels = np.asarray(validation_labels, dtype=np.int32)
        if one_hot:
            validation_labels = convert_to_one_hot(validation_labels)
        fer = {'data': validation_images, 'target': validation_labels}
    else:
        test_images = np.asarray(test_images)
        test_images = np.reshape(test_images, (-1, 1, 48, 48))
        if subtract_mean:
            test_images = test_images - mean_image
        test_labels = np.asarray(test_labels, dtype=np.int32)
        if one_hot:
            test_labels = convert_to_one_hot(test_labels)
        fer = {'data': test_images, 'target': test_labels}

    if expand:
        fer['data'] = np.tile(fer['data'], (1, 3, 1, 1))

    return fer