import requests
import json
import es_conf as es

HEADERS = {"content-type": "application/json"}


def delete_index(index):
    r = requests.delete(f"{es.ES_URL}/{index}")
    print(r.json())


def create_index(index):
    with open(f"{index}_mapping.json", "r") as file:
        data_string = json.load(file)
        print(data_string)
    r = requests.put(f"{es.ES_URL}/{index}", headers=HEADERS, data=json.dumps(data_string))
    print(r.json())


def main():
    # delete old indexes
    # delete_index(es.POSTS_INDEX)
    # delete_index(es.es.COMMENTS_INDEX)
    # create posts index
    create_index(es.POSTS_INDEX)
    # create comments index
    create_index(es.COMMENTS_INDEX)


if __name__ == "__main__":
    main()
