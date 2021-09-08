import requests
import csv
import time
import tweepy as tw
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs


def scrape_T100():
    # Original source uses cloudflare and captchas to protect against bots: Use raw HTML instead
    # DATE LAST RETRIEVED:
    html = open('Top 100 Twitter users sorted by Followers - Socialblade Twitter Stats _ Twitter Statistics.html')

    with open("../Data/T100_actors.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        # Find list of rows on page
        page = bs(html.read(), 'html.parser')
        table = page.find(style='float: right; width: 900px;')  # Should be only one table
        rows = table.find_all(style='float: left; width: 200px; line-height: 25px;')  # Select all rows

        # Locate and collect users from rows
        row_index = 0
        for row in rows:
            link = row.find(name='a')
            handle = '@' + link.getText()

            # Write to CSV
            print([handle])
            writer.writerow([handle])


def scrape_congress():

    url = 'https://ucsd.libguides.com/congress_twitter/senators'
    with open("../Data/senators.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        ### SENATORS ###
        # Find list of rows on page
        page = bs(requests.get(url).content, 'html.parser')
        table = page.find_all('table')

        for tab in table:
            rows = tab.find_all('tr')

            # Locate and collect users from rows
            for row in rows[1:]:
                cols = row.find_all('td')

                # Collect info for each user
                try:
                    name = cols[0].getText()
                    identity_data = cols[0].find('a')['href']
                    handle = '@' + identity_data[identity_data.rfind('/')+1:]
                    state = cols[1].getText()
                    party = cols[2].getText()
                    entry = [name, handle, state, party]
                except TypeError as e:
                    print("Error collecting info for " + name + ": ", e)

                # Write info to CSV
                print(entry)
                writer.writerow(entry)

        url = 'https://ucsd.libguides.com/congress_twitter/reps'
        with open("../Data/house_reps.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            ### HOUSE REPS ###
            # Find list of rows on page
            page = bs(requests.get(url).content, 'html.parser')
            table = page.find_all('table')

            for tab in table:
                rows = tab.find_all('tr')

                # Locate and collect users from rows
                for row in rows[1:]:
                    cols = row.find_all('td')

                    # Collect info for each user
                    try:
                        identity_data = cols[0].find('a')['href']
                        name = cols[0].getText()
                        handle = '@' + identity_data[identity_data.rfind('/') + 1:]
                        state = cols[1].getText()
                        party = cols[2].getText()
                        entry = [name, handle, state, party]
                    except TypeError as e:
                        print("Error collecting info for " + name + ": ", e)

                    # Write info to CSV
                    print(entry)
                    writer.writerow(entry)


def check_actors_existence():
    load_dotenv()
    auth = tw.OAuthHandler(os.getenv('CONSUMER_KEY_ONE'), os.getenv('CONSUMER_SECRET_ONE'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN_ONE'),
                          os.getenv('ACCESS_TOKEN_SECRET_ONE'))
    api = tw.API(auth, wait_on_rate_limit=True)

    with open("../Data/T100_actors.csv", 'r') as T500_data, \
         open("../Data/senators.csv", 'r') as senator_data, \
         open("../Data/house_reps.csv", 'r') as rep_data:
        reader1 = csv.reader(T500_data)
        reader2 = csv.reader(senator_data)
        reader3 = csv.reader(rep_data)

        actor_handles = [entry[0] for entry in list(reader1)] + [entry[1] for entry in list(reader2)] + [entry[1] for entry in list(reader3)]
        for handle in actor_handles:
            try:
                account = api.get_user(screen_name=handle)
            except tw.error.TweepError as e:
                print("ERROR:", e, "\nACCOUNT:", handle)


def remove_redundancy():
    with open("../Data/T100_actors.csv", 'r') as T500_data, \
            open("../Data/senators.csv", 'r') as senator_data, \
            open("../Data/house_reps.csv") as rep_data:
        reader1 = csv.reader(T500_data)
        reader2 = csv.reader(senator_data)
        reader3 = csv.reader(rep_data)

        actor_handles = [entry[0] for entry in list(reader1)] + \
                        [entry[1] for entry in list(reader2)] + \
                        [entry[1] for entry in list(reader3)]
        master_set = set()
        for handle in actor_handles:
            if handle not in master_set:
                master_set.add(handle)


    with open("../Data/master_set.csv", 'w', newline='') as master_csv:
        writer = csv.writer(master_csv)
        for handle in master_set:
            writer.writerow([handle])


if __name__ == '__main__':
    ### Scrape data for T500 actors ###
    scrape_T100()

    ### Scrape data for congress
    scrape_congress()

    ### Check if users are valid ###
    check_actors_existence()

    ### Remove redundancies & create master dataset ###
    remove_redundancy()