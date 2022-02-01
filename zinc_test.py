import fbpost
import fbcomment
import zinc_consts as zc
import requests


def update_in_index(index, data):
    pass


def check_if_in_index(index, data):
    pass


def add_to_index(index, data):
    pass


def prepare_data():
    return fbpost.Post(
        post_id=123,
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
    data = prepare_data()
    index = zc.post_index
    if check_if_in_index(index=index, data=data):
        update_in_index(index=index, data=data)
    else:
        add_to_index(index=index, data=data)


if __name__ == '__main__':
    main()
