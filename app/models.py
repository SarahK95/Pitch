from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager
from datetime import datetime



class User(UserMixin,db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password = db.Column(db.String(255))
    pitches = db.relationship('Pitches', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic')
  
   

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()  
        
      
    def set_password(self, password):
        pass_hash = generate_password_hash(password)
        self.password = pass_hash

    def verify_password(self, password):
        return check_password_hash(self.password, password)      

    def __repr__(self):
        return f'User {self.username}'
    
    @login_manager.user_loader
    def load_user(user_id):
    
      return User.query.get(int(user_id))
    
    
    
class Pitches(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pitch = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.Column(db.String, nullable=False)
    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')
    upvote = db.relationship('Upvote', backref='pitch', lazy='dynamic')
    downvote = db.relationship('Downvote', backref='pitch', lazy='dynamic')
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    comment = db.Column(db.Text())
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comments: {self.comment}'
    
class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    upvote = db.Column(db.Integer, default=1)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def upvote(cls, id):
        upvote_pitch = Upvote(user=current_user, pitch_id=id)
        upvote_pitch.save()

    @classmethod
    def query_upvotes(cls, id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    @classmethod
    def all_upvotes(cls):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
    
class Downvote(db.Model):
    __tablename__ = 'downvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    downvote = db.Column(db.Integer, default=1)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def downvote(cls, id):
        downvote_pitch = Downvote(user=current_user, pitch_id=id)
        downvote_pitch.save()

    @classmethod
    def query_downvotes(cls, id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    def all_downvotes(cls):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'    
    
    
    
    
    
    
    
    
    

    
    
         
        
    
    
    
        
