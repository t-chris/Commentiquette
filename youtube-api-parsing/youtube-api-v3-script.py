# -*- coding: utf-8 -*-

import os
import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

#I probably don't intend on letting this script be runnable through Flask.
def main():
    def get_first_page_comments(youtube, video_id):

        request = youtube.commentThreads().list(
        part="snippet",
        order="relevance",
        maxResults=300,
        textFormat="plainText",
        videoId=video_id
        )

        return request.execute()
    
    #turns out, we need a pageToken parameter to move onto subsequent pages.
    def get_subsequent_page_comments(youtube, video_id, nextPageToken):

        request = youtube.commentThreads().list(
        part="snippet",
        order="relevance",
        pageToken=next_page_token,
        maxResults=300,
        textFormat="plainText",
        videoId=video_id
        )

        return request.execute()

    def write_files_and_print(file, response, write_or_append):
        f = open(file, write_or_append, encoding='utf-8')
        for comments in response["items"]:
            #pprint.pprint(comments["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            #pprint.pprint(comments["snippet"]["topLevelComment"]["snippet"]["likeCount"])
            f.write(comments["snippet"]["topLevelComment"]["snippet"]["textDisplay"] + "\n")
        f.close()

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    #It asks to use the api_key but doesn't seem to have one, choosing instead to use Auth 2.0. Here's me manually putting it in.
    api_key = "your api key lol not mine lol damnit"
    # Get credentials and create an API client
    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #    client_secrets_file, scopes)
    #credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = api_key)
    

    #Below, just writing something to get past the linter. Other than that, I'm getting the first comments call and writing files.
    #pylint: disable=maybe-no-member

    videoId = "Wmjpp0_6kb0"
    first_response = get_first_page_comments(youtube, videoId)
    write_files_and_print("./txt-data/" + videoId + ".txt", first_response, "w+")
    next_page_token = first_response["nextPageToken"]

    try:
        while next_page_token:
            next_response = get_subsequent_page_comments(youtube, videoId, next_page_token)
            next_page_token = next_response["nextPageToken"]
            write_files_and_print("./txt-data/" + videoId + ".txt", next_response, "a")

    except KeyError: #Final search will throw back error for 'nextPageToken'
        print("Final search reached!")

if __name__ == "__main__":
    main()
