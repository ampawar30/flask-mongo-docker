from flask import Flask,jsonify,redirect, url_for, request, render_template
from flask_pymongo import PyMongo,MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import os
app=Flask(__name__)

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.mongotask    #Select the database
tasks = db.tasks #Select the collection
#app.config['MONGO_DBNAME']='mongotask'
#app.config['MONGO_URI']='mongodb://127.0.0.1:27017/mongotask'

#create object for connection between flask and monogdb
#mongo=PyMongo(app)

#cross orgin resource sharing for all origin
CORS(app)

@app.route('/api/tasks',methods=['GET'])
def get_all_tasks():
    result=[]
    for field in tasks.find():
        result.append({'_id':str(field['_id']),'title':field['title']})

    return render_template('api.html',result=result)

@app.route('/api/task',methods=['POST'])
def add_task():
    title=request.get_json()
    title=title['title']
    task_id=tasks.insert({'title':title})
    new_task=tasks.find_one({'_id':task_id})
    result={'title':new_task['title']}
    print(result)
    return jsonify({'result':result})

@app.route('/api/task/<new>',methods=['POST'])
def update_task(new):
    new_title = {
        'title': request.form['title']
            }
    task_id=tasks.insert(new_title)
    new_task=tasks.find_one({'_id':task_id})
    print(new_task)
    return redirect(url_for('get_all_tasks'))


if __name__ == "__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    debug = False if env == 'production' else True
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port, debug=debug)
