from flask import Flask, request, jsonify, render_template
from model_loader import load_model, watch_model
import logging

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    app.model = load_model(app)

    @app.before_request
    def check_for_model_updates():
        watch_model(app)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/api/recommend', methods=['POST'])
    def recommend():
        if app.model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        input_data = request.get_json(force=True)
        songs = input_data.get('songs', [])
        recommendations = []

        for song in songs:
            recommendations.extend(app.model[song])

        return jsonify({"songs": recommendations}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()