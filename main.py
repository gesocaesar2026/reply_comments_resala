
import os
import requests
import json
import random

PAGE_ID = "90118319153"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
GRAPH_API_URL = f"https://graph.facebook.com/{PAGE_ID}/posts"

HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# تحميل قائمة الرسائل
MESSAGES = [
    "يا ابني، لا تخف، أنا معك وأحمل عنك كل هم.",
    "ثق أنني أراك وأعرف احتياجك، وسأملأ كل فراغ في قلبك.",
    "لا تيأس، فأنا أعمل في الخفاء من أجلك.",
    "أحبك محبة أبدية، ولن أتركك وحدك.",
    "أنا هو السلام، تعال إليّ وأعطيك راحة.",
    "كل دمعه من عينيك لها وزن عندي.",
    "أنا معك حينما تتعثر، وأحملك على كتفي.",
    "اطمئن، فأنا ضابط الكل، وكل شيء تحت سلطاني.",
    "أنا أبوك السماوي، ولن أتركك في العاصفة.",
    "حينما تصمت، أسمع صراخ قلبك.",
    "أنا أفتح لك أبوابًا لم تكن تتخيلها.",
    "أنا طبيبك، أشفي قلبك قبل جسدك.",
    "ثق أنني أُحوّل كل ألم إلى بركة.",
    "أنا الصخرة التي لا تتزعزع، احتمِ بي.",
    "دعني أُرشدك، فأنا الطريق والحق والحياة.",
    "حينما يتركك الكل، أنا أبقى.",
    "سلامي أترك لك، لا كما يعطي العالم أعطيك.",
    "أنا إله المستحيلات، لا تتقيد بحدودك.",
    "أحنّ عليك أكثر من الأم على رضيعها.",
    "أنا العامل في كل تفاصيل حياتك."
]

# تحميل أو إنشاء ملف التعليقات التي تم الرد عليها
REPLIED_FILE = "replied.json"
if os.path.exists(REPLIED_FILE):
    with open(REPLIED_FILE, "r") as f:
        replied = set(json.load(f))
else:
    replied = set()

def get_posts():
    res = requests.get(GRAPH_API_URL, headers=HEADERS)
    return res.json().get("data", [])

def get_comments(post_id):
    url = f"https://graph.facebook.com/{post_id}/comments"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("data", [])

def reply_to_comment(comment_id, message):
    url = f"https://graph.facebook.com/{comment_id}/comments"
    data = {"message": message}
    res = requests.post(url, headers=HEADERS, data=data)
    return res.status_code == 200

def main():
    posts = get_posts()
    for post in posts:
        post_id = post["id"]
        comments = get_comments(post_id)
        for comment in comments:
            comment_id = comment["id"]
            if comment_id in replied:
                continue
            message = f"شكراً على تعليقك ❤️ رسالة المسيح ليك:

{random.choice(MESSAGES)}"
            if reply_to_comment(comment_id, message):
                replied.add(comment_id)

    # حفظ الردود
    with open(REPLIED_FILE, "w") as f:
        json.dump(list(replied), f)

if __name__ == "__main__":
    main()
