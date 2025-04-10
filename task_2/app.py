from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0)

@app.route('/count')
def count():
    try:
        visits = r.incr('counter')
        return jsonify({
            "counter": visits,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
