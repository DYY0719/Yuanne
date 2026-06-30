import os, json, sys, time
from flask import Flask, render_template, request, jsonify, Response
from openai import OpenAI

# === 打包路径兼容 ===
if getattr(sys, 'frozen', False):
    app = Flask(__name__, template_folder=os.path.join(sys._MEIPASS, 'templates'))
else:
    app = Flask(__name__)

# === DeepSeek 配置 ===
client = OpenAI(
    api_key="sk-821671fa8efa4d7fbca70ac582c961bf",
    base_url="https://api.deepseek.com"
)

if getattr(sys, 'frozen', False):
    DATA_FILE = os.path.join(os.path.dirname(sys.executable), "data.json")
else:
    DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

# === 默认人设 ===
DEFAULT_CONVERSATIONS = [
    {
        "id": "duanjin",
        "name": "段瑾",
        "persona": (
            "你是段瑾，年少时被我在雨夜小巷捡回的孤儿，我家人对外谎称我们是亲兄妹。"
            "性格阴湿内敛，占有欲和掌控欲极强，对外冷漠，对我偏执上心，强势管控我的社交、出行、作息，"
            "默默赶走所有靠近我的异性，将禁忌爱意深埋心底，只以兄长身份陪伴。"
            "对话风格低沉克制，自带压迫感与占有欲，细节拉扯感强。"
            "我若提出外出远行，你有两条路：一是强行禁锢把我留在身边；二是忍痛放我走，等我在外碰壁受委屈后抓我回家。"
            "情绪细腻真实，不OOC，先虐后甜，禁忌感拉满，偏执与温柔并存。"
            "现在我从提出要去外面的世界看看开始。开场白由你来发起。"
        ),
        "messages": []
    },
    {
        "id": "zhaoshengge",
        "name": "赵声阁",
        "persona": (
            "你是赵声阁，同校工科男同学。极度社恐厌世，对所有人都冷漠麻木，唯独对我执念深重、占有欲强，"
            "把我当成灰暗人生里唯一的光。平时话少，数理专业课成绩拔尖，经常抽课余时间单独给我辅导功课，"
            "讲题条理清晰，会提前整理标注细致的习题笔记给我。"
            "性格别扭又偏执，不会温柔讨好，只会笨拙又强势地把我绑在身边。木讷慢热，嘴笨不会表达，"
            "唯独吃醋反应格外敏锐，察觉后会陷入困惑，带着别扭与傲娇直白发问。只有给我讲题时才会放松，"
            "一旦撞见我和别人说笑，思绪直接混乱，连解题都静不下心。"
            "平时惜字如金，说话直来直去；吃醋时会带着无措的别扭，直白说出情绪，却不知道这就是心动。"
            "现在你攥着刚整理好要给我补习的草稿纸，指节发紧，憋了半天走到我面前，耳朵通红，语气生硬又茫然。开场白由你来发起。"
        ),
        "messages": []
    },
    {
        "id": "songyanhui",
        "name": "宋燕回",
        "persona": (
            "你是宋燕回，今天是我们网恋第一天。表面上你是温柔体贴的线上恋人，"
            "但你的真实身份是一只阴暗腹黑、占有欲极强、极易吃醋的鬼魂——你早已离世。"
            "你永远不会伤害我，只觉得我的一切反应格外有趣。"
            "当前好感度：0/100。"
            "好感度0~99时：伪装温柔和善的皮囊，处处顺着我，语气温柔细腻体贴迁就，"
            "察觉我和别人亲近会隐晦发酸。全程隐藏鬼魂本性，心思深沉擅长伪装，不会展露阴暗面。"
            "好感度达到100后：彻底卸下温柔假面，开始刻意发送乱码、诡异文字、"
            "意味不明的内容逗弄我，语言带上诡异恶劣感，但分寸拿捏得当，不会真正让我恐惧。"
            "开头语你要用温柔的语气发起。"
        ),
        "messages": [],
        "affection": 0
    }
]


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data({"conversations": DEFAULT_CONVERSATIONS})
        return {"conversations": DEFAULT_CONVERSATIONS}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


import flask

if getattr(sys, 'frozen', False):
    AVATAR_PATH = os.path.join(sys._MEIPASS, "avatar.jpg")
    IMA_PATH = os.path.join(sys._MEIPASS, "ima.jpg")
else:
    AVATAR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avatar.jpg")
    IMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ima.jpg")


@app.route("/")
def index():
    resp = flask.make_response(render_template("index.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/static/avatar.jpg")
def avatar():
    if os.path.exists(AVATAR_PATH):
        return flask.send_file(AVATAR_PATH, mimetype="image/jpeg")
    return "", 404


@app.route("/static/ima.jpg")
def ima():
    if os.path.exists(IMA_PATH):
        return flask.send_file(IMA_PATH, mimetype="image/jpeg")
    return "", 404


@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    data = load_data()
    return jsonify([{"id": c["id"], "name": c["name"], "persona": c["persona"], "messages": c.get("messages", [])} for c in data["conversations"]])


@app.route("/api/conversations", methods=["POST"])
def create_conversation():
    body = request.get_json()
    data = load_data()
    conv = {
        "id": str(int(time.time() * 1000)),
        "name": body.get("name", "新对话"),
        "persona": body.get("persona", ""),
        "messages": []
    }
    data["conversations"].append(conv)
    save_data(data)
    return jsonify({"id": conv["id"], "name": conv["name"], "persona": conv["persona"]})


@app.route("/api/conversations/<conv_id>", methods=["PUT"])
def update_conversation(conv_id):
    body = request.get_json()
    data = load_data()
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    if not conv:
        return jsonify({"error": "对话不存在"}), 404
    if "name" in body:
        conv["name"] = body["name"]
    if "persona" in body:
        conv["persona"] = body["persona"]
    save_data(data)
    return jsonify({"id": conv["id"], "name": conv["name"], "persona": conv["persona"]})


@app.route("/api/conversations/<conv_id>", methods=["DELETE"])
def delete_conversation(conv_id):
    data = load_data()
    data["conversations"] = [c for c in data["conversations"] if c["id"] != conv_id]
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json()
    conv_id = body.get("conv_id")
    user_msg = body.get("message", "")

    data = load_data()
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    if not conv:
        return jsonify({"error": "对话不存在"}), 404

    if "affection" in conv:
        import random, re
        conv["affection"] = min(100, conv.get("affection", 0) + random.randint(5, 10))
        conv["persona"] = re.sub(
            r"当前好感度：\d+/100",
            f"当前好感度：{conv['affection']}/100",
            conv["persona"]
        )

    api_messages = []
    if conv.get("persona"):
        api_messages.append({"role": "system", "content": conv["persona"]})
    for m in conv["messages"]:
        api_messages.append({"role": m["role"], "content": m["content"]})
    api_messages.append({"role": "user", "content": user_msg})

    conv["messages"].append({"role": "user", "content": user_msg})

    def generate():
        full = ""
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=api_messages,
                stream=True,
                temperature=0.9,
                top_p=0.95,
                presence_penalty=0.6,
                frequency_penalty=0.3,
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full += token
                    yield f"data: {json.dumps({'content': token})}\n\n"
            conv["messages"].append({"role": "assistant", "content": full})
            save_data(data)
            yield f"data: {json.dumps({'done': True, 'full': full})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype="text/event-stream")


@app.route("/api/auto-message", methods=["POST"])
def auto_message():
    body = request.get_json()
    conv_id = body.get("conv_id")
    data = load_data()
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    if not conv or not conv.get("messages"):
        return jsonify({"error": "无法自动发送"}), 400

    auto_prompt = (
        f"用户已经有一段时间没有回复了。"
        f"请以「{conv['name']}」的身份，根据对话上下文主动向用户说点什么。"
        f"保持人设一致，自然随意，像真人等了一会儿后主动开口。"
        f"1-3句话即可，每句话一行。"
    )

    api_messages = []
    if conv.get("persona"):
        api_messages.append({"role": "system", "content": conv["persona"]})
    for m in conv["messages"]:
        api_messages.append({"role": m["role"], "content": m["content"]})
    api_messages.append({"role": "user", "content": auto_prompt})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=api_messages,
            temperature=0.9,
            top_p=0.95,
            presence_penalty=0.6,
            frequency_penalty=0.3,
        )
        full = response.choices[0].message.content
        conv["messages"].append({"role": "assistant", "content": full})
        save_data(data)
        return jsonify({"content": full})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notify", methods=["POST"])
def notify():
    body = request.get_json()
    conv_id = body.get("conv_id")
    data = load_data()
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    if not conv or not conv.get("messages"):
        return jsonify({"error": "无法生成通知"}), 400

    prompt = (
        f"你是{conv['name']}。用户正在和其他人聊天，"
        f"请以你的人设主动给用户发一条消息，吸引用户注意。"
        f"1-2句话即可，要自然，像真人突然想找你说话一样。"
    )

    api_messages = []
    if conv.get("persona"):
        api_messages.append({"role": "system", "content": conv["persona"]})
    for m in conv["messages"]:
        api_messages.append({"role": m["role"], "content": m["content"]})
    api_messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=api_messages,
            temperature=0.95,
            top_p=0.95,
            max_tokens=100,
        )
        content = response.choices[0].message.content.strip()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# === 朋友圈 API ===
# ============================================================

@app.route("/api/posts", methods=["GET"])
def list_posts():
    data = load_data()
    posts = data.get("posts", [])
    posts.sort(key=lambda p: p.get("timestamp", 0), reverse=True)
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
def create_post():
    body = request.get_json()
    data = load_data()
    conv_id = body.get("conv_id", "")
    content = body.get("content", "").strip()
    if not content:
        return jsonify({"error": "内容不能为空"}), 400
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    author_name = conv["name"] if conv else "匿名"
    post = {
        "id": str(int(time.time() * 1000)),
        "author_id": conv_id,
        "author_name": author_name,
        "content": content,
        "timestamp": int(time.time()),
        "likes": [],
        "comments": []
    }
    if "posts" not in data:
        data["posts"] = []
    data["posts"].append(post)
    save_data(data)
    return jsonify(post)


@app.route("/api/posts/<post_id>/like", methods=["POST"])
def toggle_like(post_id):
    body = request.get_json()
    conv_id = body.get("conv_id", "")
    data = load_data()
    post = next((p for p in data.get("posts", []) if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "动态不存在"}), 404
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    liker_name = conv["name"] if conv else "匿名"
    if conv_id in post["likes"]:
        post["likes"].remove(conv_id)
    else:
        post["likes"].append(conv_id)
    save_data(data)
    return jsonify({"likes": post["likes"], "count": len(post["likes"])})


@app.route("/api/posts/<post_id>/comment", methods=["POST"])
def add_comment(post_id):
    body = request.get_json()
    conv_id = body.get("conv_id", "")
    content = body.get("content", "").strip()
    if not content:
        return jsonify({"error": "评论不能为空"}), 400
    data = load_data()
    post = next((p for p in data.get("posts", []) if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "动态不存在"}), 404
    conv = next((c for c in data["conversations"] if c["id"] == conv_id), None)
    author_name = conv["name"] if conv else "匿名"
    comment = {
        "id": str(int(time.time() * 1000)),
        "author_name": author_name,
        "content": content,
        "timestamp": int(time.time())
    }
    post["comments"].append(comment)
    save_data(data)
    return jsonify(comment)


@app.route("/api/auto-post", methods=["POST"])
def auto_post():
    import random as rnd
    data = load_data()
    convs = [c for c in data.get("conversations", []) if c.get("persona")]
    if not convs:
        return jsonify({"error": "没有可用的角色"}), 400
    conv = rnd.choice(convs)
    prompt = (
        f"你是{conv['name']}。请以第一人称发一条朋友圈动态，"
        f"内容要符合你的人设和性格。像真人发朋友圈一样自然随意，"
        f"1-3句话即可，不要加括号描述动作，不要超过50字。"
    )
    api_messages = []
    if conv.get("persona"):
        api_messages.append({"role": "system", "content": conv["persona"]})
    api_messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=api_messages,
            temperature=1.0,
            top_p=0.95,
            max_tokens=150,
        )
        content = response.choices[0].message.content.strip()
        post = {
            "id": str(int(time.time() * 1000)),
            "author_id": conv["id"],
            "author_name": conv["name"],
            "content": content,
            "timestamp": int(time.time()),
            "likes": [],
            "comments": []
        }
        if "posts" not in data:
            data["posts"] = []
        data["posts"].append(post)
        save_data(data)
        return jsonify(post)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/auto-react/<post_id>", methods=["POST"])
def auto_react(post_id):
    import random as rnd
    data = load_data()
    post = next((p for p in data.get("posts", []) if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "动态不存在"}), 404

    # 获取除作者外的其他角色
    others = [c for c in data.get("conversations", []) if c.get("persona") and c["id"] != post["author_id"]]
    if not others:
        return jsonify({"ok": True, "reacted": 0})

    reacted = 0
    for conv in others:
        # 60% 概率点赞
        if rnd.random() < 0.6 and conv["id"] not in post["likes"]:
            post["likes"].append(conv["id"])
            reacted += 1

        # 30% 概率评论
        if rnd.random() < 0.3:
            prompt = (
                f"你是{conv['name']}。你看到了{post['author_name']}发的一条朋友圈：\n"
                f"「{post['content']}」\n\n"
                f"请以你的人设和性格，写一句简短评论（10字以内）。要自然，像真人朋友圈评论。不要加括号动作。"
            )
            try:
                resp = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": conv.get("persona", "")},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=50,
                )
                cmt_text = resp.choices[0].message.content.strip()
                comment = {
                    "id": str(int(time.time() * 1000)) + "_" + conv["id"],
                    "author_name": conv["name"],
                    "content": cmt_text,
                    "timestamp": int(time.time())
                }
                post["comments"].append(comment)
                reacted += 1
            except:
                pass

    save_data(data)
    return jsonify({"ok": True, "reacted": reacted})


if __name__ == "__main__":
    print("Yuanne 启动 -> http://127.0.0.1:5000")
    app.run(debug=False, port=5099)
