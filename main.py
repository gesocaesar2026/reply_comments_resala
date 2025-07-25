import requests
import os
import json

PAGE_ID = "90118319153"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
REPLIED_FILE = "replied_comments.txt"

def get_last_post_id():
    url = f"https://graph.facebook.com/{PAGE_ID}/posts?limit=1&access_token={ACCESS_TOKEN}"
    res = requests.get(url).json()
    return res["data"][0]["id"] if "data" in res and res["data"] else None

def get_comments(post_id):
    url = f"https://graph.facebook.com/{post_id}/comments?filter=stream&access_token={ACCESS_TOKEN}"
    res = requests.get(url).json()
    return res.get("data", [])

def load_replied():
    if not os.path.exists(REPLIED_FILE):
        return set()
    with open(REPLIED_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_replied(comment_id):
    with open(REPLIED_FILE, "a") as f:
        f.write(comment_id + "\n")

def reply_to_comment(comment_id, message):
    url = f"https://graph.facebook.com/{comment_id}/comments"
    payload = {"message": message, "access_token": ACCESS_TOKEN}
    res = requests.post(url, data=payload)
    return res.ok

def main():
    print("🔁 بدء تشغيل الرد التلقائي...")
    last_post_id = get_last_post_id()
    if not last_post_id:
        print("❌ لا يوجد منشور")
        return

    comments = get_comments(last_post_id)
    replied_ids = load_replied()

    for comment in comments:
        if comment["id"] in replied_ids:
            continue
        if comment.get("parent") is not None:
            continue  # رد على تعليق = تجاهله

        msg = "ربنا يباركك ويكون معاك دايمًا ✝️❤️"
        if reply_to_comment(comment["id"], msg):
            print(f"✅ تم الرد على: {comment['id']}")
            save_replied(comment["id"])
        else:
            print(f"⚠️ فشل الرد على: {comment['id']}")

if __name__ == "__main__":
    main()
