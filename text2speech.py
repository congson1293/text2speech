# -*- encoding: utf-8 -*-

import subprocess, os
import utils, config
from sklearn.externals import joblib
import time
from io import open
import shutil
from datetime import datetime
from dateutil.parser import parse
# from multiprocessing import Process




class text2speech:
    def __init__(self, firs_run=False):
        self.root_path = os.getcwd()
        self.summary_level = u'medium'
        self.first_run = firs_run
        self.event_ids = {}
        self.date = datetime.now()


    def check_date(self, date_obj):
        datetime_obj = date_obj.date()
        now = datetime.now()
        diff = now.date() - datetime_obj
        if diff.days != 0:
            return True
        return False


    def tts_articles(self, db, db_product):
        try:
            contentId = joblib.load('contentId.pkl')
        except:
            contentId = 0

        try:
            collection_tts = db_product.get_collection(config.MONGO_COLLECTION_TTS_ARTICLES)
        except:
            collection_tts = db_product.create_collection(config.MONGO_COLLECTION_TTS_ARTICLES)

        try:
            collection_summary = db.get_collection(config.MONGO_COLLECTION_SUMMRIES)
            documents = collection_summary.find({u'contentId': {u'$gt': contentId}})

            for doc in documents:
                try:
                    try:
                        date_obj = parse(doc[u'date'])
                    except:
                        date_obj = doc[u'date']
                    if self.check_date(date_obj):
                        continue
                    content = u'\n'.join([doc[u'summaries'][self.summary_level].replace(u'_', u' '),
                                          u'Theo ' + doc[u'publisher']])
                    contentId = doc[u'contentId']
                    output_file_path = self.create_audio_file(contentId, content,
                                                              config.TTS_FINAL_ARTICLE_OUTPUT_PATH)
                    now = datetime.utcnow()
                    collection_tts.insert_one({u'contentId': contentId,
                                               u'title' : doc[u'title'],
                                               u'content' : content,
                                               u'relative_path': output_file_path,
                                               u'root_path': self.root_path,
                                               u'updated_at': now})
                except Exception as e:
                    print(e.message)
                    continue
                time.sleep(5)

            joblib.dump(contentId, 'contentId.pkl')
        except Exception as e:
            print('exception raise in tts_articles: %s' % (e.message))


    # tts both hot event and long event
    def tts_events(self, db, db_product):
        if self.first_run:
            self.first_run = True
            self.tts_long_event(db, db_product)
        self.tts_hot_event(db, db_product)


    def tts_hot_event(self, db, db_product):
        try:
            collection_tts = db_product.get_collection(config.MONGO_COLLECTION_TTS_EVENTS)
        except:
            collection_tts = db_product.create_collection(config.MONGO_COLLECTION_TTS_EVENTS)

        try:
            collection_hot_events = db.get_collection(config.MONGO_COLLECTION_HOT_EVENTS_BY_EDITOR)
            documents = collection_hot_events.find()
            for hot in documents:
                try:
                    event_id = hot[u'event_id']
                    if not utils.is_exist(self.event_ids, event_id):
                        self.event_ids.update({event_id : True})
                        self.save_event_to_mongo(collection_tts, event_id, hot[u'event_name'])
                except:
                    continue
                time.sleep(5)
        except:
            pass



    def tts_long_event(self, db, db_product):
        event_ids = {}

        try:
            collection_tts = db_product.get_collection(config.MONGO_COLLECTION_TTS_EVENTS)
        except:
            collection_tts = db_product.create_collection(config.MONGO_COLLECTION_TTS_EVENTS)

        try:
            collection_long_events = db.get_collection(config.MONGO_COLLECTION_LONG_EVENTS)
            documents = collection_long_events.find()
            for long in documents:
                try:
                    long_event_id = long[u'event_id']
                    if not utils.is_exist(event_ids, long_event_id):
                        event_ids.update({long_event_id : True})
                        self.save_event_to_mongo(collection_tts, long_event_id, long[u'event_name'])
                    for child in long[u'child_events']:
                        child_event_id = child[u'event_id']
                        if not utils.is_exist(event_ids, child_event_id):
                            event_ids.update({child_event_id : True})
                            self.save_event_to_mongo(collection_tts, child_event_id, child[u'event_name'])
                except:
                    continue
        except:
            pass


    def save_event_to_mongo(self, collection, event_id, event_name):
        output_file_path = self.create_audio_file(event_id, event_name,
                                                  config.TTS_FINAL_EVENT_OUTPUT_PATH)
        now = datetime.utcnow()
        collection.insert_one({u'event_id': event_id,
                               u'event_name': event_name,
                               u'relative_path': output_file_path,
                               u'root_path': self.root_path,
                               u'updated_at': now})


    def create_audio_file(self, output_filename, content, output_path):
        utils.mkdir(config.TTS_OUTPUT_ROOT_DIR)
        with open(config.TTS_INPUT_FILE, 'w', encoding='utf-8') as fp:
            fp.write(unicode(content))

        text_norm_cmd = ['java', '-jar',
                         'TextNorm.jar',
                         config.TTS_INPUT_FILE,
                         'Female']
        subprocess.call(text_norm_cmd)

        files = os.listdir(config.TTS_OUTPUT_ROOT_DIR)

        synthesis_cmd = ['java', '-jar',
                         'Syn.jar',
                         os.path.join(config.TTS_OUTPUT_ROOT_DIR, files[0]),
                         config.TTS_OUTPUT_LAST_DIR,
                         'NOR', 'Female']
        subprocess.call(synthesis_cmd)

        output_file_path = os.path.join(output_path,
                                        str(output_filename) + '.wav')
        shutil.move(os.path.join(config.TTS_OUTPUT_LAST_DIR_PATH,
                                 config.TTS_DEFAULT_OUTPUT_FILE),
                    output_file_path)

        shutil.rmtree(config.TTS_OUTPUT_ROOT_DIR)

        return output_file_path


    def run_tts_articles(self):
        while True:
            print('run_tts_articles is running...')
            try:
                print('connect to mongodb ...')
                connection, db = utils.connect2mongo(config.MONGO_HOST, config.MONGO_PORT,
                                                     config.MONGO_USER, config.MONGO_PASS,
                                                     config.MONGO_DB)

                self.tts_articles(db)
            except:
                try:
                    connection.close()
                except:
                    pass


    def run_tts_events(self):
        while True:
            try:
                print('run_tts_events is running...')
                if self.check_date(self.date):
                    self.date = datetime.now()
                    self.event_ids.clear()

                print('connect to mongodb ...')
                connection, db = utils.connect2mongo(config.MONGO_HOST, config.MONGO_PORT,
                                                     config.MONGO_USER, config.MONGO_PASS,
                                                     config.MONGO_DB)

                self.tts_events(db)
            except:
                try:
                    connection.close()
                except:
                    pass


    # def run(self):
    #     utils.mkdir(config.TTS_FINAL_OUTPUT_ROOT_DIR)
    #     utils.mkdir(config.TTS_FINAL_ARTICLE_OUTPUT_PATH)
    #     utils.mkdir(config.TTS_FINAL_EVENT_OUTPUT_PATH)
    #
    #     handle_articles = Process(target=self.run_tts_articles)
    #     handle_articles.start()
    #
    #     handle_events = Process(target=self.run_tts_events)
    #     handle_events.start()
    #
    #     while True:
    #         time.sleep(60 * 60)


    def run(self):
        utils.mkdir(config.TTS_FINAL_OUTPUT_ROOT_DIR)
        utils.mkdir(config.TTS_FINAL_ARTICLE_OUTPUT_PATH)
        utils.mkdir(config.TTS_FINAL_EVENT_OUTPUT_PATH)

        try:
            shutil.rmtree(config.TTS_OUTPUT_ROOT_DIR)
        except: pass

        while True:
            try:
                print('connect to mongodb ...')
                connection, db = utils.connect2mongo(config.MONGO_HOST, config.MONGO_PORT,
                                                     config.MONGO_USER, config.MONGO_PASS,
                                                     config.MONGO_DB)

                connection_product, db_product = utils.connect2mongo(config.MONGO_HOST_PRODUCT,
                                                                     config.MONGO_PORT_PRODUCT,
                                                                     config.MONGO_USER_PRODUCT,
                                                                     config.MONGO_PASS_PRODUCT,
                                                                     config.MONGO_DB_PRODUCT)

                print('tts_events is running...')
                if self.check_date(self.date):
                    self.date = datetime.now()
                    self.event_ids.clear()
                self.tts_events(db, db_product)

                print('tts_articles is running...')
                self.tts_articles(db, db_product)

                connection.close()
                connection_product.close()

                print('sleep in %d seconds' % (config.TIME_TO_SLEEP))
                time.sleep(config.TIME_TO_SLEEP)
            except:
                try:
                    connection.close()
                    connection_product.close()
                except:
                    pass
                print('sleep in %d seconds' % (config.TIME_TO_SLEEP))
                time.sleep(config.TIME_TO_SLEEP)





if __name__ == '__main__':
    tts = text2speech()
    tts.run()