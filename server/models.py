from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError('Author must have a name')


        existing = Author.query.filter(Author.name == name).first()
        if existing and existing.id != getattr(self, 'id', None):
            raise ValueError('Author name must be unique')

        return name

    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if phone_number is None:
            return phone_number

        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Phone number must be exactly 10 digits')

        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('title')
    def validate_title(self, key, title):
        if not title or title.strip() == '':
            raise ValueError('Post must have a title')

        clickbait_phrases = ["Won't Believe", 'Secret', 'Top', 'Guess']
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Post title must be clickbait-y')

        return title

    @validates('content')
    def validate_content(self, key, content):
        if content is None or len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary is None:
            return summary
        if len(summary) > 250:
            raise ValueError('Summary must be 250 characters or less')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid = ['Fiction', 'Non-Fiction']
        if category not in valid:
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
