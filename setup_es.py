import requests
import json
import es_conf as es
import sys


HEADERS = {"content-type": "application/json"}


def create_iter_count_doc():
    print("Creating iter_count doc 1")
    data = {"iter_count": 1}
    r = requests.put(f"{es.ES_URL}/{es.ITER_INDEX}/_doc/1", data=json.dumps(data), headers=HEADERS)
    print(f"{r.json()}\n")


def delete_index(index):
    print(f"Deleting index {index}")
    r = requests.delete(f"{es.ES_URL}/{index}")
    print(f"{r.json()}\n")


def create_index(index):
    print(f"Reading mapping for {index}")
    with open(f"mappings/{index}_mapping.json", "r") as file:
        data_string = json.load(file)
    print(f"Creating index {index} with mapping")
    r = requests.put(
        f"{es.ES_URL}/{index}", headers=HEADERS, data=json.dumps(data_string)
    )
    print(f"{r.json()}\n")


def main():
    try:
        param = sys.argv[1]
        if param == "fresh":
            # delete old indices
            delete_index(es.POST_INDEX)
            delete_index(es.COMMENTS_INDEX)
            delete_index(es.ITER_INDEX)
    except IndexError:
        pass
    # create indices
    create_index(es.POST_INDEX)
    create_index(es.COMMENTS_INDEX)
    create_index(es.ITER_INDEX)
    # populate index iter_count
    create_iter_count_doc()


if __name__ == "__main__":
    main()
