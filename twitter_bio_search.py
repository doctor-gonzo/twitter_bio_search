get_ipython().system('pip install tweepy') # For running in a jupyter notebook

import csv
import time
import numpy as np
import tweepy as tw

# Fill this up with the Twitter Apps Credentials (get them @ apps.twitter.com)

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)

# Get the User object for the profile you are interested in...
user = api.get_user('USER') # Where USER is the account whose followers you are interested in

# Define terms you want to search for in bios of followers of above user

keywords = ["example", "reads Hunter S Thompson"] # Follower bio terms you are interested in
hits = [] ## Array of twitter profiles/users that contain one of the keywords above in their bio

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tw.RateLimitError:
            time.sleep(15 * 60)
            continue

for follower in limit_handled(tw.Cursor(api.followers, id = 'glenweyl').items()):
    for word in keywords:
        if word in str(follower.description.encode('utf-8')) and not (follower in hits):
            hits.append(follower)
            
            
for follower in hits:
    print((follower.screen_name)) ## Access follower name: (follower.screen_name)
    
hits = np.array(hits)
            
# Write CSV File

with open('search_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in range(0,hits.shape[0]):
        myList = []
        myList.append(hits[row])
        writer.writerow(myList)
