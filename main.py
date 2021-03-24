from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import datetime as dt

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'datab.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    uploadTime = db.Column(db.DateTime,default=dt.datetime.utcnow)

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration


class SongSchema(ma.Schema):
    class Meta:
        fileds = ('id', 'name', 'duration', 'uploadTime')


song_schema = SongSchema()
songs_schema = SongSchema(many=True)

@app.route("/song", methods=['POST'])
def addSong():
    name = request.json['name']
    duration = request.json['duration']

    newSong = Song(name, duration)

    db.session.add(newSong)
    db.session.commit()

    return song_schema.jsonify(newSong)


@app.route('/songs', methods=['GET'])
def getSongs():
    allSongs = Song.query.all()
    result = songs_schema.dump(allSongs)
    print(result)
    return jsonify(result)


@app.route('/songs/<id>', methods=['GET'])
def getSong(id):
    song = Song.query.get(id)
    data = song_schema.jsonify(song)
    print(data)
    print(song)
    return data


if __name__ == '__main__':
    app.run(debug=True)