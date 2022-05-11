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
    
    
    
        
