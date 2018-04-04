import os
#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from celery import Celery


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


# db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize db
db = SQLAlchemy(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_ACCEPT_CONTENT'] = ['json']
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_RESULT_SERIALIZER'] = 'json'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# ftp directory path
path = '/home/ftper/ftp_root/resource'

@celery.task
def async_scan():
    """Background task."""
    with app.app_context():
        traverse(path)


def look():
        print("send")
        async_scan.apply_async()


# timer configuration
app.config['SCHEDULER_API_ENABLED'] = True
#app.config['JOBS'] =  [{ 'id': 'job1', 'func': look, 'trigger': 'interval', 'seconds': 10 }]
app.config['JOBS'] =  [{ 'id': 'job1', 'func': look, 'trigger': 'cron', 'hour': 2 }]
#app.config['SCHEDULER_JOBSTORES'] =  {'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')}

scheduler = APScheduler()
scheduler.init_app(app)
    
scheduler.start()


def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if not os.path.isdir(tmp_path):
            #print('file: %s'%tmp_path)
            split_path(tmp_path)
        else:
            traverse(tmp_path)

def split_path(str):
    if str.strip():
        items = str.split(os.path.sep)
        #print(len(items))
        if len(items) == 10:            

            file = File()
            file.language = items[5]
            file.phone_num = items[6]
            file.word_type = items[7]
            file.word_num = items[8]
            file.file_name = items[9]
            
            f = File.query.filter_by(file_name = file.file_name).first()
            if not f:
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
    if language is None or phone_num is None:
        abort(400)
    
    wordlist = db.session.query(File.file_name).filter(and_(File.language == language, File.phone_num == phone_num, File.word_type == 'Word'))

    return jsonify({'words': [y for x in wordlist for y in x]})


@app.route('/api/narrations', methods=['POST'])
def get_narrations():
    language = request.form.get('language')
    phone_num = request.form.get('phone_num')
    if language is None or phone_num is None:
        abort(400)
    narrationlist = db.session.query(File.file_name).filter(and_(File.language == language, File.phone_num == phone_num, File.word_type == 'Narration'))

    return jsonify({'narrations': [y for x in narrationlist for y in x]})


if __name__ == '__main__':
    app.run()
