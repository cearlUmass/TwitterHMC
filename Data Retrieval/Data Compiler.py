import pickle
import csv
import json

# This function is specifically for compiling all the dumped data into a single pickled file
# Additionally, this will add denominations for political actors
if __name__ == '__main__':

    ### Follower Compilation ###
    # NUM_OF_APIS = 12
    #
    # # Calculate indexes for fully retrieved files for each API
    # with open("../KEYS.json", "rb") as secrets:
    #     keys = json.load(secrets)
    #     num_apps = len(keys['Consumer Keys'])
    #
    # with open('../Data/master_set.csv', 'r') as actors_file:
    #     reader = csv.reader(actors_file)
    #     actors = list(reader)
    #     total_actors = len(actors)
    #     actors_per_app = int(total_actors / num_apps)
    #     ranges = [[i * actors_per_app, (i + 1) * actors_per_app] for i in range(num_apps)]
    #
    #     # Dealing with remainders
    #     r = total_actors % num_apps
    #     if r != 0:
    #         ranges[-r:] = [[ranges[-r + i][0] + i, ranges[-r + i][1] + 1 + i] for i in range(r)]
    #
    #
    # master_dict = {}
    # directory = '../Data/Follower data dump'
    # file_index = -1
    # total_collected = 0
    # for api_num in range(NUM_OF_APIS):
    #
    #     # Determine which file to compile
    #     file_num = ranges[api_num][1] - ranges[api_num][0] - 1
    #     actor = actors[file_num + file_index + 1]
    #     file_index += file_num+1
    #     loc = '../Data/Follower data dump/api{0}-{1}-{2}.pkl'.format(api_num, file_num, actor[0])
    #
    #     # Merge with master set
    #     with open(loc, 'rb') as max_data_file:
    #         data = pickle.load(max_data_file)
    #         total_collected += len(data)
    #         for k, v in data.items():
    #             if k in master_dict:
    #                 master_dict[k]['follows'].extend(v['follows'])
    #             else:
    #                 master_dict[k] = v
    #
    # print("Total followers retrieved:", total_collected)
    # print("Size of Set of Followers:", len(master_dict))
    # with open('../Data/Master sets/master follower set.pkl', 'wb') as max_file:
    #     pickle.dump(master_dict, max_file, pickle.HIGHEST_PROTOCOL)


    ### Actor Compilation ###
    with open("../Data/Master sets/master actor set.pkl", 'rb') as actor_data_file, \
         open("../Data/house_reps.csv", 'r') as reps_info_file, \
         open("../Data/senators.csv", 'r') as sen_info_file:

        data = pickle.load(actor_data_file)
        info = list(csv.reader(reps_info_file)) + list(csv.reader(sen_info_file))
        for actor_info in info:
            handle = actor_info[1]
            denomination = actor_info[3]

            if denomination == 'R':
                data[handle]['denomination'] = +1
            elif denomination == 'D':
                data[handle]['denomination'] = -1
            else:
                data[handle]['denomination'] = 0

    with open("../Data/Master sets/master actor set.pkl", 'wb') as actor_data_file:
        pickle.dump(data, actor_data_file)