import base64


url = "http://91.192.224.142:4080/api"
user = "admin"
password = "303.lsg"
bas64encoded_creds = base64.b64encode(
    bytes(user + ":" + password, "utf-8")).decode("utf-8")
headers = {"Content-type": "application/json",
           "Authorization": "Basic " + bas64encoded_creds}
post_index = "POSTS"
comment_index = "COMMENTS"
