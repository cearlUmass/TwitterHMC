import csv
import tweepy as tw
import pickle
import threading
import json
from typing import Optional


def filter_user_data(unfiltered_data, actor_name) -> dict:
    user_fields = [
        'screen_name',
        'id',
        'followers_count',
        'friends_count',
        'created_at',
        'time_zone',
        'statuses_count',
        'protected',
        'verified',
        'default_profile',
        'default_profile_image',
        'withheld_in_countries',
    ]

    # Add desired fields
    filtered_data = {}
    for field in user_fields:
        try:
            filtered_data[field] = unfiltered_data._json[field]
        except KeyError as e:
            print("COULD NOT GET KEY:", field, "FOR USER", filtered_data['screen_name'])
    filtered_data["follows"] = [actor_name]

    return filtered_data


def collect_follower_data(
    file_name: str,
    api: tw.API,
    api_name: Optional[str],
    num_items: int,
    start: Optional[int] = 0,
    end: Optional[int] = -1
) -> None:

    # Retrieve list of political actors
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        actors = list(reader)

    # Iterate through all followers of a given political actor
    # followers = { follower_name : { Data : ..., follows : [list of actors user is following] }
    followers = {}

    for i, actor in enumerate(actors[start:end]):
        actor_name = actor[0]

        try:

            # TODO: Try dynamic sampling (dynamically change num_iters according to actor)
            # Iterate through followers of actor
            for follower in tw.Cursor(api.followers, actor_name).items(num_items):
                follower_name = follower.screen_name

                # If follower is already in dict, append the actor
                if follower_name in followers:
                    followers[follower_name]['follows'].append(actor_name)

                # Otherwise add follower data to dict
                else:
                    followers[follower_name] = filter_user_data(follower, actor_name)

            with open('../Data/Follower data dump/{0}-{1}-{2}.pkl'.format(api_name, i, actor_name), 'wb') as write_file:
                pickle.dump(followers, write_file, pickle.HIGHEST_PROTOCOL)

        except tw.error.TweepError as e:
            print("ERROR RETRIEVING ACTOR:", e, "\nACCOUNT:", actor_name, "API:", api_name)


def collect_actor_data(
    file_name: str,
    api: tw.API,
) -> None:

    # Retrieve list of political actors
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        actors = list(reader)

    actor_data = {}
    for actor in actors:
        actor_name = actor[0]

        try:
            user = api.get_user(actor_name)
            actor_data[actor_name] = {
                'followers': user.followers_count,
                'friends': user.friends_count,
            }
        except tw.error.TweepError as e:
            print("ERROR RETRIEVING ACTOR:", e, "\nACCOUNT:", actor_name)

    with open('../Data/Master sets/master actor set.pkl', 'wb') as write_file:
        pickle.dump(actor_data, write_file, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    # Load API's & threads
    with open("../KEYS.json", "rb") as secrets:

        # Load secrets
        keys = json.load(secrets)
        num_apps = len(keys['Consumer Keys'])
        CK = keys['Consumer Keys']
        CS = keys['Consumer Secrets']
        AT = keys['Access Tokens']
        AS = keys['Access Secrets']

        # Assertions
        assert all([(len(keys[k]) == num_apps) for k in keys]), "Un-equal number of tokens"
        assert all((len(i) == 25) for i in CK), "A Consumer Key is wrong"
        assert all((len(i) == 50) for i in CS), "A Consumer Secret is wrong"
        assert all((len(i) == 50) for i in AT), "An Access Token is wrong"
        assert all((len(i) == 45) for i in AS), "An Access Secret is wrong"

    # ### Get Followers Data ###
    # # Calculate even division of work
    # with open('../Data/master_set.csv', 'r') as actors_file:
    #     reader = csv.reader(actors_file)
    #     actors = list(reader)
    #     total_actors = len(actors)
    #     actors_per_app = int(total_actors / num_apps)
    #     ranges = [[i * actors_per_app, (i+1) * actors_per_app] for i in range(num_apps)]
    #
    #     # Dealing with remainders
    #     r = total_actors % num_apps
    #     if r != 0:
    #         ranges[-r:] = [[ranges[-r+i][0]+i, ranges[-r+i][1]+1+i] for i in range(r)]
    #
    #
    # # Create API's & threads
    # threads = []
    # for i in range(num_apps):
    #
    #     # Authorize
    #     auth = tw.OAuthHandler(CK[i], CS[i])
    #     auth.set_access_token(AT[i], AS[i])
    #     api = tw.API(auth, wait_on_rate_limit=True)
    #
    #     # Thread
    #     thread = threading.Thread(
    #         target=collect_follower_data,
    #         args=(
    #               '../Data/master_set.csv',     # Actors file name
    #               api,                          # API
    #               "api{0}".format(i),           # API name
    #               9500,                         # Number of retrievals
    #               ranges[i][0],                 # Starting index
    #               ranges[i][1]                  # Ending index
    #             )
    #     )
    #     threads.append(thread)
    #
    # # Start threads
    # # Note: output format is: (api_name)-(api_index)-(actor_name).pkl
    # for thread in threads:
    #     thread.start()


    ### Get Actor Data ###
    # Authorize
    auth = tw.OAuthHandler(CK[0], CS[0])
    auth.set_access_token(AT[0], AS[0])
    api = tw.API(auth, wait_on_rate_limit=True)

    # Collect
    collect_actor_data(
        '../Data/master_set.csv',
        api
    )