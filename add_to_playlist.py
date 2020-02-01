# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    with open('to_add.txt') as f:
        raw = f.read().split()
    raw = set(raw)
    TO_ADD = set()
    for r in raw:
        x = r[len('https://www.youtube.com/watch?v='):]
        if x:
            TO_ADD.add(x)
    print(TO_ADD)

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    

    for v in TO_ADD:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": "PL7xx8Kc-zlMwD8uioIL5oPU8-TsW9PW1m",
                "position": 0,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": v
                }
              }
            }
        )
        response = request.execute()

if __name__ == "__main__":
    main()