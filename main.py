import os
import requests
import random
import json

# إعدادات الصفحة
PAGE_ID = "90118319153"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"

# الرسائل الممكنة للرد بها
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

def get_last_posts(limit=3):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/posts?limit={limit}&access_token={ACCESS_TOKEN}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        print("❌ فشل في جلب المنشورات.")
        return []

def get_comments(post_id):
    # filter=toplevel لجلب تعليقات المستوى الأول فقط
    url = f"https://graph.facebook.com/v19.0/{post_id}/comments?filter=toplevel&access_token={ACCESS_TOKEN}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        print(f"❌ فشل في جلب تعليقات البوست {post_id}")
        return []

def reply_to_comment(comment_id, message):
    url = f"https://graph.facebook.com/v19.0/{comment_id}/comments"
    data = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    r = requests.post(url, data=data)
    return r.status_code == 200

# تنفيذ الردود
posts = get_last_posts()

for post in posts:
    comments = get_comments(post['id'])
    for comment in comments:
        comment_id = comment["id"]
        commenter_id = comment.get("from", {}).get("id", "")

        # تجاهل التعليق إذا تم الرد عليه مسبقًا أو كاتبه هو الصفحة
        if comment_id in replied:
            continue
        if commenter_id == PAGE_ID:
            continue

        # الرد على التعليق
        random_message = random.choice(messages)
        reply_text = f"شكراً على تعليقك ❤️ رسالة المسيح ليك هي:\n{random_message}"
        success = reply_to_comment(comment_id, reply_text)
        if success:
            print(f"✅ تم الرد على: {comment_id}")
            replied.add(comment_id)
        else:
            print(f"❌ فشل الرد على: {comment_id}")

# حفظ التعليقات التي تم الرد عليها
with open('replied.json', 'w') as f:
    json.dump(list(replied), f)
