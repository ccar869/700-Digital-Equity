from flask import Flask, jsonify, send_from_directory, request, make_response, Response
from flask_cors import CORS
import test
import os
from pymongo import MongoClient
from datetime import datetime,timezone

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

client = MongoClient('mongodb+srv://rebeccafitzpatrick:hfJ|m#gv5W55@cluster0.pvplf8n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['700_web_tool_db']
leaderboard_collection = db['leaderboard']
users_collection = db['users']

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route('/web', methods=['GET'])
def speedtest():
    (download, upload, packet_loss, avg_ping) = test.speedTest()
    return jsonify({
        'download': download,
        'upload': upload,
        'packet_loss': packet_loss,
        'avg_ping': avg_ping
    })

@app.route('/api/speedtest', methods=['POST'])
def user_speedtest():
    data = request.json
    username = data.get('username')
    packet_loss = "0"
    if not username:
        return jsonify({'success': False, 'message': 'Username required'}), 400

    # Run the speed test
    download, upload, packet_loss, avg_ping = test.speedTest()

    # Store the result in the database
    speedtest_record = {
        'name': username,
        'download': download,
        'upload': upload,
        'packet_loss': packet_loss,
        'avg_ping': avg_ping,
        'timestamp': datetime.now(timezone.utc)

    }
    leaderboard_collection.insert_one(speedtest_record)
    speedtest_record.pop('_id', None)  # Remove MongoDB's _id field for the response

    return jsonify({'success': True, 'result': speedtest_record})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    data = list(leaderboard_collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
    return jsonify(data)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify(users)

# Example: login route using users_collection
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = users_collection.find_one({"username": data.get("username"), "password": data.get("password")})
    if user:
        return jsonify({"success": True, "user": user["username"]})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/garbage.php', methods=['GET', 'HEAD'])
def download_test():
    try:
        size = int(request.args.get('ckSize', 1* 1024 *1024))  # default 10MB
    except ValueError:
        return "Invalid size", 400

    if request.method == 'HEAD':
        # Return headers only (for latency test)
        response = make_response()
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Length'] = str(size)
        return response

    # Streaming generator to avoid large memory allocation
    def generate():
        chunk_size = 8192
        bytes_sent = 0
        while bytes_sent < size:
            yield b'\0' * min(chunk_size, size - bytes_sent)
            bytes_sent += chunk_size

    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(size),
    }

    return Response(generate(), headers=headers)

@app.route('/empty.php', methods=['POST'])
def upload_test():
    # Data is received but not stored
    _ = request.get_data()
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run()
    