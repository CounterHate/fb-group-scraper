from tokenize import group
from facebook_scraper import get_posts
import fbpost
import fbcomment
import fbgroup
import json
import time
import csv


def dump_group_posts(posts, group):
    with open(f"output/{group.group_name}.json", "w") as f:
        f.write(json.dumps(posts, indent=2))


def dump_comments(comments, post_id):
    with open(f"output/comments/{post_id}.json", "w") as f:
        f.write(json.dumps(comments, indent=2))


def process_post(p, group):
    post = fbpost.Post(
        post_id=int(p["post_id"]),
        content=p["text"],
        date=str(p["time"]),
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
        date=str(c["comment_time"]),
        group_id=group.group_id,
        group_name=group.group_name,
        author_id=int(c["commenter_id"]),
        author_profile_url=c["commenter_url"],
        replies=str(c["replies"]),
        reaction_count=c["comment_reaction_count"],
    )
    return comment


def process_group(group):
    time.sleep(5)
    print(f"Processing {group.group_name}")
    posts = []
    options = {"comments": True}
    credentials = ("", "")
    for p in get_posts(group=group.group_id, pages=2, options=options):
        try:
            post = process_post(p, group)
        except Exception as e:
            print(e)
            print(p)
        comments = []
        for c in p["comments_full"]:
            comment = process_comment(c, post_id=p["post_id"], group=group)
            comments.append(comment.to_dict())
        posts.append(post.to_dict())
        if len(comments) > 0:
            dump_comments(comments=comments, post_id=p["post_id"])
    dump_group_posts(posts=posts, group=group)


def get_groups():
    groups = []
    with open("groups.csv", "r") as file:
        inputreader = csv.reader(file)
        for index, row in enumerate(inputreader):
            if index == 0:
                continue
            groups.append(
                fbgroup.Group(
                    group_id=row[0],
                    group_name=row[1],
                    private=row[2],
                    email=row[3],
                    password=row[4],
                )
            )
    return groups


def main():
    groups = get_groups()
    iter = 0
    while True:
        print(f'Iter: {iter}')
        for group in groups:
            time.sleep(20)
            process_group(group)
        iter += 1
        time.sleep(600)


if __name__ == "__main__":
    main()
