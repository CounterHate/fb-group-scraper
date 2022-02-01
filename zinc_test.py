import fbpost
import fbcomment
import zinc_consts as zc
import requests
import json


def update_in_index(index, data, document_id):
    r = requests.put(
        f"{zc.url}/{index}/document", headers=zc.headers, data=json.dumps(data)
    )
    print(r.text)


def check_if_in_index(index, data):
    params = {
        "search_type": "querystring",
        "query": {
            "term": f"+post_id: {data['post_id']}",
            "start_time": "2022-01-01T15:08:48.777Z",
            "end_time": "2022-02-01T16:08:48.777Z",
        },
        "from": 40,
        "max_results": 20,
        "fields": ["_all"],
    }
    r = requests.post(
        f"{zc.url}/{index}/_search", headers=zc.headers, data=json.dumps(params)
    )
    print(r.json()["hits"]["hits"])
    if r.json()["hits"]["total"]["value"] > 0:
        return True
    else:
        return False


def add_to_index(index, data):
    r = requests.put(
        f"{zc.url}/{index}/document", headers=zc.headers, data=json.dumps(data)
    )
    print(r.text)


def create_index(index):
    print(f"{zc.url}/{index}")
    r = requests.put(f"{zc.url}/{index}", headers=zc.headers)
    print(r.text)


def prepare_data(post_id):
    return fbpost.Post(
        post_id=post_id,
        content="content",
        date="01.01.2022",
        group_name="group1",
        group_id=123,
        post_url="https://url.com",
        author_id=111,
        author_profile_url="https://profile.com",
        urls=[],
    )


def main():
    # post1 = prepare_data(123)
    # post2 = prepare_data(345)
    post3 = prepare_data(456)
    index = zc.post_index
    # existing post with post_id = 123
    if check_if_in_index(index=index, data=post3.to_dict()):
        pass
        # update_in_index(index=index, data=post3)
    else:
        add_to_index(index=index, data=post3.to_dict())


if __name__ == "__main__":
    main()
