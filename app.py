from flask import Flask, request
import requests
import os

SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_VERIFY_TOKEN = os.environ["SLACK_VERIFY_TOKEN"]

app = Flask(__name__)

@app.route("/from-slack", methods=["POST"])
def hook():
    if request.json["token"] != SLACK_VERIFY_TOKEN:
        print("failed to verity token")
        return "hum"
    request_type = request.json.get("type")
    if request_type == "url_verification":
        print("challenged")
        return request.json["challenge"]
    elif request_type == "event_callback" and request.json["event"]["type"] == "link_shared":
        # link shared
        print("unfurling...")
        unfurls = {}
        for link in request.json["event"]["links"]:
            url = link["url"]
            print(url)
            unfurls[url] = {
                "blocks": [{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "test"
                    }
                }]
            }
            requests.post("https://slack.com/api/chat.unfurl", json={
                "channel": request.json["event"]["channel"],
                "ts": request.json["event"]["message_ts"],
                "unfurls": unfurls,
            }, headers={
                "Authorization": "Bearer {}".format(SLACK_API_TOKEN),
            }).raise_for_status()
        return "hummm"
    else:
        print("unknown type", request_type)
        return "humm"
