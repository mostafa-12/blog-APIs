from flask import Flask, jsonify, request
from models import User, Post, Comment
from extension import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Blog API!"})

@app.route("/users")
def get_users():
    users = User.query.all()
    return jsonify({"users": [{
        "id": user.id,
        "username": user.username,
        "email": user.email
    } for user in users]})
    
@app.route("/users", methods = ["POST"])
def create_user():
    data = request.get_json()
    user = User(
        username = data["username"],
        email = data["email"]
    )
    user.password = data["password"]
    try:
        db.session.add(user)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 201

@app.route("/users/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return "",204

@app.route("/users/<int:user_id>", methods = ["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not all(key in data for key in ["username", "email", "password"]):
        return "", 204
    user.username = data["username"]
    user.email = data["email"]
    user.password = data["password"]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

@app.route("/users/<int:user_id>", methods = ["PATCH"])
def patch_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not any(key in data for key in ["username", "email", "password"]):
        return "", 204
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200


@app.route("/posts")
def get_posts():
    from models import Post
    posts = Post.query.all()
    return jsonify({"posts": [{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "comments":[
            {
                "id": comment.id,
                "content": comment.content,
                "author_id": comment.author_id,
            }
            for comment in post.comments
        ]
    } for post in posts]})
    
    
@app.route("/posts", methods = ["POST"])
def create_post():
    data = request.get_json()
    post = Post(
        title = data["title"],
        content = data["content"],
        author_id = int(data["author_id"])
    )
    try:
        db.session.add(post)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id
    }), 201    
    
    
    
@app.route("/post/<int:post_id>", methods = ["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return "",204

@app.route("/post/<int:post_id>", methods = ["PUT"])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    if not all(key in data for key in ["title", "content", "author_id"]):
        return "", 204
    post.title = data["title"]
    post.content = data["content"]
    post.author_id = int(data["author_id"])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id
    }), 200

@app.route("/post/<int:post_id>", methods = ["PATCH"])
def patch_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    if not any(key in data for key in ["title", "content", "author_id"]):
        return "", 204
    if "title" in data:
        post.title = data["title"]
    if "content" in data:
        post.content = data["content"]
    if "author_id" in data:
        post.author_id = int(data["author_id"])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id
    }), 200



@app.route("/comments")
def get_comments():
    from models import Comment
    comments = Comment.query.all()
    return jsonify({"comments": [{
        "id": comment.id,
        "content": comment.content,
        "author_id": comment.author_id,
        "post_id": comment.post_id
    } for comment in comments]}) 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)