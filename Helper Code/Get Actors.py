import requests
import csv
import time
import tweepy as tw
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs


def scrape_T500():
    # As of Feb 3 2020, there are 25 users per page
    pages = 20
    url = 'https://www.trackalytics.com/the-most-followed-twitter-profiles/page/'

    with open("../Data/T500_actors.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for page in range(1, pages + 1):
            # Small delay to not annoy the host!
            time.sleep(.5)

            # Find list of rows on page
            page = bs(requests.get(url + str(page)).content, 'html.parser')
            table = page.find_all(class_='table table-bordered table-striped')  # Should be only one table
            body = table[0].find_all('tbody')  # Should be only one body
            rows = body[0].find_all('tr')  # Select all rows

            # Locate and collect users from rows
            row_index = 0
            for row in rows:
                attr_with_handle = row.contents[1].find("a")['onclick']  # Handle located in link attribute
                start = attr_with_handle.find('@')
                end = attr_with_handle.find(' ', start)
                handle = attr_with_handle[start:end]

                # Write to CSV
                print([handle])
                writer.writerow([handle])


def scrape_congress():
    # As of Feb 3 2020, there are 25 users per page
    pages = 20
    url = 'https://triagecancer.org/congressional-social-media'

    with open("../Data/congress_actors.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        # Find list of rows on page
        page = bs(requests.get(url).content, 'html.parser')
        table = page.find(id='footable_16836')
        rows = table.find_all('tr')

        # Locate and collect users from rows
        for row in rows[1:]:
            cols = row.find_all('td')
            useful_cols = cols[:3] + cols[4:6]  # Only get columns w/ useful information

            # Collect info for each user
            entry = []
            for col in useful_cols:
                entry.append(col.getText())

            # Write info to CSV
            print(entry)
            writer.writerow(entry)


def check_actors_existence():
    load_dotenv()
    auth = tw.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))  # << key/secret goes here
    auth.set_access_token(os.getenv('ACCESS_TOKEN'),
                          os.getenv('ACCESS_TOKEN_SECRET'))  # << Access_token/secret goes here
    api = tw.API(auth, wait_on_rate_limit=True)

    with open("../Data/T500_actors.csv", 'r') as T500_data, open("../Data/congress_actors.csv", 'r') as congress_data:
        reader1 = csv.reader(T500_data)
        reader2 = csv.reader(congress_data)
        actor_handles = [entry[0] for entry in list(reader1)] + [entry[4] for entry in list(reader2)]
        for handle in actor_handles:
            try:
                account = api.get_user(screen_name=handle)
            except tw.error.TweepError as e:
                print("ERROR:", e, "\nACCOUNT:", handle)


def remove_redundancy():
    with open("../Data/T500_actors.csv", 'r') as T500_data, open("../Data/congress_actors.csv", 'r') as congress_data:
        reader1 = csv.reader(T500_data)
        reader2 = csv.reader(congress_data)
        actor_handles = [entry[0] for entry in list(reader1)] + [entry[4] for entry in list(reader2)]
        master_set = set()
        for handle in actor_handles:
            if handle not in master_set:
                master_set.add(handle)


    with open("../Data/master_set.csv", 'w', newline='') as master_csv:
        writer = csv.writer(master_csv)
        for handle in master_set:
            writer.writerow([handle])


if __name__ == '__main__':
    # ### Scrape data for T500 actors ###
    # scrape_T500()
    #
    # ### Scrape data for congress
    # scrape_congress()

    ### Check if users are valid ###
    check_actors_existence()

    ### Remove redundancies & create master dataset ###
    # remove_redundancy()