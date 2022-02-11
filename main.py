from facebook_scraper import get_posts
import fbpost
import fbcomment
import fbgroup
import json
import time
import requests
from datetime import datetime
import openpyxl
import random

ES_URL = "http://localhost:9200"
POST_INDEX = "fb_posts"
COMMENTS_INDEX = "fb_comments"
HEADERS = {"content-type": "application/json"}
# INPUT_FILE = "Lista grup do przeglądu.xlsx"
INPUT_FILE = "test_input.xlsx"

def to_epoch(date):
    utc_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return (utc_time - datetime(1970, 1, 1)).total_seconds()


def add_to_index(index, data):
    if index == POST_INDEX:
        r = requests.put(
            f"{ES_URL}/{index}/_doc/{data['post_id']}",
            headers=HEADERS,
            data=json.dumps(data),
        )
        print(r.json())
    else:
        r = requests.put(
            f"{ES_URL}/{index}/_doc/{data['comment_id']}",
            headers=HEADERS,
            data=json.dumps(data),
        )
        print(r.json())


def process_post(p, group):
    post = fbpost.Post(
        post_id=int(p["post_id"]),
        content=p["text"],
        date=to_epoch(str(p["time"])),
        group_name=group.group_name,
        group_id=group.group_id,
        post_url=p["post_url"],
        urls=p["link"],
        author_id=p["user_id"],
        author_profile_url=p["user_url"],
        like_count=p["likes"],
        comment_count=p["comments"],
        share_count=p["shares"],
    )
    return post


def process_comment(c, post_id, group):
    comment = fbcomment.Comment(
        original_post_id=post_id,
        comment_id=int(c["comment_id"]),
        content=c["comment_text"],
        date=to_epoch(str(c["comment_time"])),
        group_id=group.group_id,
        group_name=group.group_name,
        author_id=int(c["commenter_id"]),
        author_profile_url=c["commenter_url"],
        replies=str(c["replies"]),
        reaction_count=c["comment_reaction_count"],
    )
    return comment


def process_group(group):
    print(f"Processing {group.group_name}")
    options = {"comments": True}
    credentials = ("", "")
    for p in get_posts(group=group.group_id, pages=2, options=options):
        time.sleep(random.randint(2,6))
        try:
            post = process_post(p, group)
        except Exception as e:
            print(e)
            print(p)
        for c in p["comments_full"]:
            comment = process_comment(c, post_id=p["post_id"], group=group)
            add_to_index(index=COMMENTS_INDEX, data=comment.to_dict())
        add_to_index(index=POST_INDEX, data=post.to_dict())


def get_groups():
    wb = openpyxl.load_workbook(INPUT_FILE)
    groups = []
    for ws in wb.worksheets:
        for row in range(1, ws.max_row + 1):
            if row == 1:
                continue
            # get group id from group url
            group_id = ws[row][2].value.split("/")[-2]
            group = fbgroup.Group(
                group_id=group_id,
                group_name=ws[row][1].value,
                email="",
                password="",
                private=False,
            )
            groups.append(group)
    return groups


def main():
    groups = get_groups()
    for group in groups:
        process_group(group)
        time.sleep(7200 + random.randint(1,10) * 60 - random.randint(1,10) * 60)


if __name__ == "__main__":
    main()
