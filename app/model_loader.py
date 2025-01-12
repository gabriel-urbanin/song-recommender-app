import os
import pickle
from time import sleep

VOLUME_PATH = '/app/model/song_recommendations.pkl'

def load_model(app):
    try:
        app.logger.info(f'Loading model file: {VOLUME_PATH}')
        app.last_modified_time = os.path.getmtime(VOLUME_PATH)
        return pickle.load(open(VOLUME_PATH, 'rb'))
    except Exception as e:
        app.logger.error(f'Error loading model: {e}')
        return None

def watch_model(app):
    try:
        current_modification_time = os.path.getmtime(VOLUME_PATH)
        if current_modification_time != app.last_modified_time:
            app.logger.info('New model was found! Updating application model...')
            app.model = load_model(app)
            app.last_modified_time = current_modification_time
        else:
            app.logger.info('No changes in current model. Proceding with recommendations')
    except Exception as e:
        app.logger.error(f'Could not check for updates on the model: {e}')
