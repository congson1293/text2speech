# -*- encoding: utf-8 -*

import os

# MONGO_HOST = '103.35.64.122'
# MONGO_PORT = 2200
# MONGO_USER = 'dbMongo'
# MONGO_PASS = 'SOh3TbYhx8ypJPxmt1oOfL'

MONGO_HOST = '210.245.115.39'
MONGO_PORT = 27017
MONGO_USER = ''
MONGO_PASS = ''

MONGO_DB = 'dbMongo'

MONGO_COLLECTION_SUMMRIES = 'summaries'
MONGO_COLLECTION_TTS_ARTICLES = 'tts_articles'
MONGO_COLLECTION_TTS_EVENTS = 'tts_events'
MONGO_COLLECTION_UPDATE_TIME = 'update_time'
MONGO_COLLECTION_LONG_EVENTS = 'long_events'
MONGO_COLLECTION_HOT_EVENTS_BY_EDITOR = 'hot_events_editor'

TIME_TO_SLEEP = 60 * 1

HOUR_TO_RESET = 0

TTS_INPUT_FILE = 'input_temp.txt'

TTS_DEFAULT_OUTPUT_FILE = 'output.wav'

TTS_OUTPUT_ROOT_DIR = 'tts_temp'
TTS_OUTPUT_CHILD_DIR = 'temp'
TTS_OUTPUT_CHILD_DIR_PATH = os.path.join(TTS_OUTPUT_ROOT_DIR, TTS_OUTPUT_CHILD_DIR)
TTS_OUTPUT_LAST_DIR = 'output'
TTS_OUTPUT_LAST_DIR_PATH = os.path.join(TTS_OUTPUT_CHILD_DIR_PATH, TTS_OUTPUT_LAST_DIR)

TTS_FINAL_OUTPUT_ROOT_DIR = 'tts_output'

TTS_FINAL_ARTICLE_OUTPUT_DIR = 'articles'
TTS_FINAL_ARTICLE_OUTPUT_PATH = os.path.join(TTS_FINAL_OUTPUT_ROOT_DIR, TTS_FINAL_ARTICLE_OUTPUT_DIR)

TTS_FINAL_EVENT_OUTPUT_DIR = 'events'
TTS_FINAL_EVENT_OUTPUT_PATH = os.path.join(TTS_FINAL_OUTPUT_ROOT_DIR, TTS_FINAL_EVENT_OUTPUT_DIR)