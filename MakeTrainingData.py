import pickle
import pprint as pp


def make_training_data(file):
    with open(file, 'rb') as follower_Data:
        return pickle.load(follower_Data)


if __name__ == '__main__':
    data = make_training_data('Data/Follower Data.pkl')
    pp.pprint(data)
    for user in data:
        d = len(data[user]['follows'])
        if d > 1:
            print(user)
