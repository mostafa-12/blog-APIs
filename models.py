from extension import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic", cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy="dynamic", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<User {self.username}, {self.email}"
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")
    @password.setter
    def password(self, password):
        from werkzeug.security import generate_password_hash
        self.hashed_password = generate_password_hash(password)
    def verify_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.hashed_password, password)
    
    
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", backref="post", lazy="dynamic", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Post {self.title}>"
    
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    
    def __repr__(self):
        return f"<Comment {self.content[:20]}...>"