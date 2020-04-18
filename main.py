#! /usr/bin/env python
import argparse
import os
import requests

BOT_TOKEN = "MYBOTTOKEN"
CHAT_ID = "MYCHATID"


def download_latest_photo(dst_path):
    updates = post_json('getUpdates', data={"chat_id": CHAT_ID})
    for message in updates["result"][::-1]:
        if "photo" in message["message"]:
            # Select highest resolution photo
            file_id = updates["result"][-1]["message"]["photo"][-1]["file_id"]
            # Get file_path
            photo = get_json('getFile', params={"chat_id": CHAT_ID, "file_id": file_id})
            file_path = photo['result']['file_path']
            # Download photo
            file_name = os.path.basename(file_path)
            response = requests.get('https://api.telegram.org/file/bot%s/%s' % (BOT_TOKEN, file_path))
            dst_file_path = os.path.join(dst_path, file_name)
            with open(dst_file_path, 'w') as f:
                f.write(response.content)
            print(u"Downloaded file to {}".format(dst_file_path))
            break

def get_json(method_name, *args, **kwargs):
    return make_request('get', method_name, *args, **kwargs)

def post_json(method_name, *args, **kwargs):
    return make_request('post', method_name, *args, **kwargs)

def make_request(method, method_name, *args, **kwargs):
    response = getattr(requests, method)(
        'https://api.telegram.org/bot%s/%s' % (BOT_TOKEN, method_name),
        *args, **kwargs
    )
    if response.status_code > 200:
        raise DownloadError(response)
    return response.json()

class DownloadError(Exception):
    pass

def main():
    parser = argparse.ArgumentParser("Download latest photo received")
    parser.add_argument("dst", help="Destination folder")
    args = parser.parse_args()

    download_latest_photo(args.dst)

if __name__ == "__main__":
    main()
@tnvnieya
