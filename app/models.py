from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()    

    def __repr__(self):
        return f'User {self.username}'
    
class Pitches(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pitch = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.Column(db.String, nullable=False)
    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')
    up_vote = db.relationship('Upvote', backref='pitch', lazy='dynamic')
    down_vote = db.relationship('Downvote', backref='pitch', lazy='dynamic')
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_category(cls, category):
        pitches = Pitches.query.filter_by(category=category).all()
        return pitches    
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()    

    def __repr__(self):
        return f'User {self.title}'
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment = db.Column(db.Text())
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comments: {self.comment}'
        
    
    
    
        
