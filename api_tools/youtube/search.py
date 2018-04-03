# -*- coding: utf-8 -*-
'''
search.py

CLI for accessing Youtube search API with the option to save results to json
format.

Sample usage:
    python search.py --q=surfing > outfile.json

NOTE:
    To use this program, you must provide a developer key obtained in the
    Google APIs Console. Add your on key to a '.env_key' file or Search for
    "REPLACE_ME" in this code to find the correct place to provide that key.

REFERENCE:
    https://github.com/youtube/api-samples/blob/master/python/search.py
    https://developers.google.com/youtube/v3/docs/search/list
'''
import argparse
import json

from datetime import timedelta, datetime

from apiclient.discovery import build
from apiclient.errors import HttpError

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
with open(".env_key") as env:
    DEVELOPER_KEY = env.read().strip() # REPLACE_ME

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    '''For a given a set of command-line options, query Youtube Search API and
    return the raw result in json form.'''
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        type=options.type,
        maxResults=options.max_results,
        relevanceLanguage=options.lang
    ).execute()
    return search_response.get("items", [])

def period_search():
    pass # TODO

def result_to_file(options):
    pass # TODO

# NOTE:
#   Not currently used but saved for possible future.
def youtube_topic_id(topic):
    "read relevant topic id from csv file."
    with open("youtube_topic_ids.csv") as yt_id:
        for line in yt_id:
            if topic.capitalize() not in line:
                continue
            return line.split(",")[0]
    return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--q", help="Search term", type=str, required=True)
    argparser.add_argument("--max_results", help="Max results", type=int, default=50)
    argparser.add_argument("--lang", help="most relevant language", type=str, default="en")
    argparser.add_argument("--type", help="type of content to search", type=str, default="video")
    argparser.add_argument("--period", help="Number of days to span search accross.", type=int)
    argparser.add_argument("--start_date", help="date to start period", type=str)
    args = argparser.parse_args()

    try:
        # just print stuff out for now.
        print(json.dumps(youtube_search(args), indent=2))
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))