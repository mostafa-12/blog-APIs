from app import db, app
from models import User, Post, Comment
from faker import Faker

def seed_users(n=10):
    fake = Faker()
    for i in range(n):
        user = User(
            username = fake.name(),
            email = fake.email(),
        )
        user.password = fake.password(length=12)
        db.session.add(user)
        db.session.commit()
            
            
def seed_posts(n=20):
    fake = Faker()
    for i in range(n):
        post = Post(
            title = fake.sentence(),
            content = fake.text(),
            author_id = fake.random_int(min=1, max = User.query.count())
        )
        db.session.add(post)
        db.session.commit()
            
def seed_comments(n=50):
    fake = Faker()
    for i in range(n):
        comment = Comment(
            content = fake.text(),
            author_id = fake.random_int(min=1, max = User.query.count()),
            post_id = fake.random_int(min=1, max = Post.query.count())
        )
        db.session.add(comment)
        db.session.commit()
            
            
if __name__ == '__main__':
    with app.app_context():
        seed_users()
        seed_posts()
        seed_comments()