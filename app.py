from flask import Flask, render_template, request, redirect, url_for

import json

app = Flask(__name__)

def load_posts():
    with open("blog_posts.json", "r") as file:
        return json.load(file)


@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        posts = load_posts()

        new_id = max(post["id"] for post in posts) + 1 if posts else 1

        new_post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content
        }

        posts.append(new_post)
        with open("blog_posts.json", "w") as file:
            json.dump(posts, file, indent=4)
        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

