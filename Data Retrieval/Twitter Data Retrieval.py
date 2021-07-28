import csv
import tweepy as tw
import os
import pickle
from dotenv import load_dotenv


def filterUserData(unfiltered_data, actor_name):
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


def CollectData(file_name, api, api_name, num_items, start, end):
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

            # Iterate through followers of actor
            print("ACTOR: ", actor)
            for follower in tw.Cursor(api.followers, actor_name).items(num_items):
                follower_name = follower.screen_name

                # If follower is already in dict, append the actor
                print("\tFOLLOWER:", follower_name)
                if follower_name in followers:
                    followers[follower_name]['follows'].append(actor_name)

                # Otherwise add follower data to dict
                else:
                    followers[follower_name] = filterUserData(follower, actor_name)

            print("\tDUMPING...")
            with open('../Data/Follower data dump/{0}-{1}-{2}.pkl'.format(i, api_name, actor_name), 'wb') as write_file:
                pickle.dump(followers, write_file, pickle.HIGHEST_PROTOCOL)

        except tw.error.TweepError as e:
            print("ERROR RETRIEVING ACTOR:", e, "\nACCOUNT:", actor_name)


if __name__ == '__main__':
    # CONSTANTS
    load_dotenv()
    auth1 = tw.OAuthHandler(os.getenv('CONSUMER_KEY_ONE'), os.getenv('CONSUMER_SECRET_ONE'))
    auth1.set_access_token(os.getenv('ACCESS_TOKEN_ONE'), os.getenv('ACCESS_TOKEN_SECRET_ONE'))
    api1 = tw.API(auth1, wait_on_rate_limit=True)

    auth2 = tw.OAuthHandler(os.getenv('CONSUMER_KEY_TWO'), os.getenv('CONSUMER_SECRET_TWO'))
    auth2.set_access_token(os.getenv('ACCESS_TOKEN_TWO'), os.getenv('ACCESS_TOKEN_SECRET_TWO'))
    api2 = tw.API(auth2, wait_on_rate_limit=True)

    auth3 = tw.OAuthHandler(os.getenv('CONSUMER_KEY_THREE'), os.getenv('CONSUMER_SECRET_THREE'))
    auth3.set_access_token(os.getenv('ACCESS_TOKEN_THREE'), os.getenv('ACCESS_TOKEN_SECRET_THREE'))
    api3 = tw.API(auth3, wait_on_rate_limit=True)

    APIS = [api1, api2, api3]
    FOLLOWERS_PER_ACTOR = 900
    USER_LIMIT = 900
    APP_LIMIT = 300

    CollectData('../Data/master_set.csv', api1, 1, 5, 0, 2)