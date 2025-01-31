from flask import Flask, render_template, request, redirect, url_for

import json

app = Flask(__name__)

def load_posts():
    """ load blog posts from JSON, ensuring 'likes' field exists """
    try:
        with open("blog_posts.json", "r") as file:
            posts = json.load(file)

            for post in posts:
                post.setdefault("likes", 0)

            return posts
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@app.route("/")
def index():
    """ Display all blog posts from the JSON file """
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Handles adding a new blog post.
    - GET: Displays the form for adding a post
    - POST: Saves the new post and redirects to the homepage
    """
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


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()

    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["title"] = request.form["title"]
        post["author"] = request.form["author"]
        post["content"] = request.form["content"]

        with open("blog_posts.json", "w") as file:
            json.dump(posts, file, indent=4)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """ remove a blog post by ID and update the JSON file """
    posts = load_posts()

    posts = [post for post in posts if post["id"] != post_id]

    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)

    return redirect(url_for("index"))


@app.route("/like/<int:post_id>")
def like(post_id):
    """ increase the like count of a blog post """
    posts = load_posts()

    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    post["likes"] = post.get("likes", 0) + 1

    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)

    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

