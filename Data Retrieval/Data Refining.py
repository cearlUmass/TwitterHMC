import pickle
import csv
import numpy as np

# List of political actors twitter handles
pol_actors = np.array(list(csv.reader(open('../Data/congress_actors.csv'))))[:, 4]


# Conditions for follower to be considered in the model
def is_viable(follower) -> bool:
    # 100+ Tweets
    if follower['statuses_count'] < 100:
        return False

    # Tweeted in past 6 months
    # NA (Need premium API)

    # 25+ followers
    if follower['followers_count'] < 25:
        return False

    # Located in US
    # NA (Need premium API)

    # 3+ political accounts followed
    if len(follower['follows']) < 3:
        return False
    else:
        pol_followed = 0
        for a in follower['follows']:
            if a in pol_actors:
                pol_followed += 1
        if pol_followed < 3:
            return False

    return True


if __name__ == '__main__':

    ### Load Data ###
    follower_data_raw = pickle.load(open('../Data/Master sets/master follower set.pkl', 'rb'))
    actor_data = pickle.load(open('../Data/Master sets/master actor set.pkl', 'rb'))

    ### Filter data ###
    follower_data = {}
    for follower_name, data in follower_data_raw.items():
        if is_viable(data):
            follower_data[follower_name] = data

    print("Refined set of followers:", len(follower_data))

    with open('../Data/Refined sets/refined master follower set.pkl', 'wb') as refined_file:
        pickle.dump(follower_data, refined_file, pickle.HIGHEST_PROTOCOL)
