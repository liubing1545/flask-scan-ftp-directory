import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from celery import Celery


db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@192.168.33.10:5432/ftp_files'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# ftp directory path
path = 'D:\\recording'


@celery.task
def async_scan():
    """Background task."""
#    with app.app_context():
    print("fuck")
    traverse(path)


def look():
    #with app.app_context():
        print("send")
        async_scan.apply_async()
    #print("zzz")
    # with db.app.app_context():
    #     print(User.query.all())


def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if not os.path.isdir(tmp_path):
            print('file: %s'%tmp_path)
            split_path(tmp_path)
        else:
            print('folder:%s'%tmp_path)
            traverse(tmp_path)

def split_path(str):
    if str.strip():
        items = str.split(os.path.sep)
        print(len(items))
        if len(items) == 7:
            # print(items[0])
            # print(items[1])
            # print(items[2])
            # print(items[3])
            # print(items[4])
            # print(items[5])
            # print(items[6])
            

            file = File()
            file.language = items[2]
            file.phone_num = items[3]
            file.word_type = items[4]
            file.word_num = items[5]
            file.file_name = items[6]
            
            file.insert()
    


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(10), index=True)
    phone_num = db.Column(db.String(20), index=True)
    word_type = db.Column(db.String(10))
    word_num = db.Column(db.String(10))
    file_name = db.Column(db.Text())

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error %s" % e)
            raise e
        finally:
            print("Insert"
                  "<id=%s> in database" % (self.id))

    def to_json(self):
        json_file = {
           
            'file_name': self.file_name
        }
        return json_file


@app.route('/api/words', methods=['POST'])
def get_words():
    language = request.form.get('language')
    phone_num = request.form.get('phone_num')
    print("kkk")
    if language is None or phone_num is None:
        abort(400)
    
    wordlist = db.session.query(File.file_name).filter(and_(File.language == language, File.phone_num == phone_num, File.word_type == 'word'))

    return jsonify({'words': [y for x in wordlist for y in x]})


@app.route('/api/narrations', methods=['POST'])
def get_narrations():
    language = request.json.get('language')
    phone_num = request.json.get('phone_num')
    if language is None or phone_num is None:
        abort(400)
    narrationlist = db.session.query(File.file_name).filter(and_(File.language == language, File.phone_num == phone_num, File.word_type == 'narration'))

    return jsonify({'narrations': [y for x in wordlist for y in x]})


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': look,
            'trigger': 'interval',
            'seconds': 5
        }
    ]

    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')
    # }

    SCHEDULER_API_ENABLED = True


if __name__ == '__main__':
    # app = Flask(__name__)
    app.config.from_object(Config())



    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    
    db.app = app
    db.init_app(app) 
    # db.drop_all()
    # db.create_all()
    # traverse(path)
    app.run()