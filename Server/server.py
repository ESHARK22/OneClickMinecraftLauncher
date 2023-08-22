import json
import flask
import uuid
app = flask.Flask(__name__)


@app.route('/McUser', methods=['GET'])
def McUser():
    username = flask.request.args.get('username')
    with open("accounts.json", "r") as f:
        database = json.load(f)
    if username in database:
        return flask.jsonify(database[username])
    else:
        return flask.abort(404)
    
@app.route('/McUser', methods=['POST'])
def McUserPost():
    username = flask.request.args.get('username')
    uuid = uuid.uuid4()
    client_token = uuid.uuid4()
    can_play_mc = flask.request.args.get('CanPlayMC')
    try:
        mc_username = flask.request.args.get('MinecraftUsername')
    except:
        mc_username = username.split("\\")[1]

    with open("accounts.json", "r") as f:
        database = json.load(f)
    database[username] = {
        "MinecraftUsername": mc_username,
        "MinecraftUUID": uuid,
        "MinecraftClientToken": client_token,
        "CanPlayMC": can_play_mc
        }

app.run(host="0.0.0.0", port=4755)