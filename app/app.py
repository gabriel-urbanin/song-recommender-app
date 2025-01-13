from flask import Flask, request, jsonify, render_template, send_from_directory
from model_loader import load_model, watch_model
import logging, os

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    app.model = load_model(app)

    @app.before_request
    def check_for_model_updates():
        watch_model(app)
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/api/recommend', methods=['POST'])
    def recommend():
        if app.model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        input_data = request.get_json(force=True)
        songs = input_data.get('songs', [])
        recommendations = set()

        for song in songs:
            if song not in app.model:
                recommendations.update(app.model['default_recommendation'])
            else:
                recommendations.update(app.model[song])

        return jsonify({"songs": list(recommendations)}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()