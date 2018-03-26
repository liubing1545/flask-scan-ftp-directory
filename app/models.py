import hashlib
from flask import current_app,url_for
from . import db

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(20), unique=True, index=True)
    language = db.Column(db.String(10), unique=True, index=True)
    file_paths = db.Column(db.Text())

    # def __init__(self, **kwargs):
    #     super(File, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['FLASKY_ADMIN']:
    #             self.role = Role.query.filter_by(permissions=0xff).first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()
    #     if self.email is not None and self.avatar_hash is None:
    #         self.avatar_hash = hashlib.md5(
    #             self.email.encode('utf-8')).hexdigest()

    def to_json(self):
        json_file = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'phone_num': self.phone_num,
            'language': self.language,
            'file_paths': self.file_paths
            # 'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            # 'followed_posts': url_for('api.get_user_followed_posts',
            #                           id=self.id, _external=True),
        }
        return json_file

    def __repr__(self):
        return '<File %r>' % self.phone_num
