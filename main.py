import os
import requests
import random
import json
from datetime import datetime

# إعداد المتغيرات من GitHub Secrets
PAGE_ID = "90118319153"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"


# قائمة الرسائل (ممكن تضيف أكتر هنا)
messages = [
    "أنا هو الطريق والحق والحياة، ثق إني ماشٍ معاك خطوة بخطوة.",
    "لا تخف، لأني معك. لا تتلفت، لأني إلهك.",
    "في العالم سيكون لكم ضيق، ولكن ثقوا: أنا قد غلبت العالم.",
    "أنا الراعي الصالح، والراعي الصالح يبذل نفسه عن الخراف.",
    "ثق أنني أراك في وحدتك، وأسمعك في صمتك، وأحبك رغم كل شيء.",
    "سلامي أترك لكم، سلامي أعطيكم. ليس كما يعطي العالم أعطيكم.",
    "أنا هو نور العالم، من يتبعني فلا يمشي في الظلمة.",
    "ارفع عينيك نحوي، فأنا معينك في وقت الضعف.",
    "لا تهتموا لحياتكم، ولا لما تلبسون، أليس الرب يهتم بكم أكثر؟",
    "كل الأشياء تعمل معًا للخير للذين يحبون الله.",
    "أنا هو الألف والياء، البداية والنهاية.",
    "دعني أحمل عنك ما يُتعبك، فقط سلّمني قلبك.",
    "حينما تبكي، أنا بجانبك أمسح دموعك.",
    "إن سرتُ في وادي ظل الموت، لا أخاف شرًا لأنك معي.",
    "أحببتك منذ الأزل، لذلك أدمت لك الرحمة.",
    "أنا معك، لا أهملك ولا أتركك.",
    "دع السلام يملك في قلبك، فأنا إله السلام.",
    "حينما تنهار، أكون قوتك.",
    "كل من يأتي إليّ لا أخرجه خارجًا.",
    "أحبك محبة أبدية، ولن أتخلى عنك."
]

# تحميل التعليقات التي تم الرد عليها سابقًا
try:
    with open('replied.json', 'r') as f:
        replied = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    replied = set()

def get_comments():
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed?fields=id,message,comments{{id,message,from}}&access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()
    return data.get("data", [])

def reply_to_comment(comment_id, message):
    url = f"https://graph.facebook.com/v19.0/{comment_id}/comments"
    data = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    r = requests.post(url, data=data)
    return r.status_code == 200

posts = get_comments()

for post in posts:
    comments = post.get("comments", {}).get("data", [])
    for comment in comments:
        comment_id = comment["id"]
        if comment_id not in replied:
            random_message = random.choice(messages)
            full_reply = f"شكراً على تعليقك ❤️ رسالة المسيح ليك هي:\n{random_message}"
            success = reply_to_comment(comment_id, full_reply)
            if success:
                print(f"✅ تم الرد على: {comment_id}")
                replied.add(comment_id)
            else:
                print(f"❌ فشل الرد على: {comment_id}")

# حفظ التعليقات التي تم الرد عليها
with open('replied.json', 'w') as f:
    json.dump(list(replied), f)
