import requests
import json

ES_URL = "http://localhost:9200"
HEADERS = {"content-type": "application/json"}
POSTS_INDEX = "fb_posts"
COMMENTS_INDEX = "fb_comments"


def delete_index(index):
    r = requests.delete(f"{ES_URL}/{index}")
    print(r.json())


def create_index(index):
    with open(f"{index}_mapping.json", "r") as file:
        data_string = json.load(file)
        print(data_string)
    r = requests.put(f"{ES_URL}/{index}", headers=HEADERS, data=json.dumps(data_string))
    print(r.json())


def main():
    # delete old indexes
    delete_index(POSTS_INDEX)
    delete_index(COMMENTS_INDEX)
    # create posts index
    create_index(POSTS_INDEX)
    # create comments index
    create_index(COMMENTS_INDEX)


if __name__ == "__main__":
    main()
