import pickle
import os
import pprint as pp


def make_training_data(file):
    with open(file, 'rb') as follower_Data:
        return pickle.load(follower_Data)


if __name__ == '__main__':
    for filename in os.listdir('Data/Follower data dump'):
        data = make_training_data('Data/Follower data dump/{0}'.format(filename))
        pp.pprint(data)
        # for user in data:
        #     d = len(data[user]['follows'])
        #     if d > 1:
        #         print(user)