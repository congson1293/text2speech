# -*- coding: utf-8 -*-
__author__ = 'nobita'

import os, shutil
from io import open
import random, string
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime



# return list of string
def load_data_to_dict(data_file):
    d = {}
    with open(data_file, 'r', encoding='utf-8') as f:
        for data in f:
            data = data.strip(u'\n').strip().lower()
            d.update({data:True})
    return d


def load_data_to_list(data_file):
    l = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for data in f:
            l.append(data.strip(u'\n').strip().lower())
    return l


def mkdir(dir):
    if (os.path.exists(dir) == False):
        os.mkdir(dir)


def push_data_to_stack(stack, file_path, file_name):
    sub_folder = os.listdir(file_path)
    for element in sub_folder:
        element = file_name + '/' + element
        stack.append(element)


def update_dict_from_value(d1, d2):
    for k, v in d1.items():
        for kk, vv in v.items():
            d2[k].update({vv:kk})
    return


def string2bytearray(s):
    l = [c for c in s]
    return l


def add_to_list(l1, l2):
    l = []
    for x in l1:
        for xx in l2:
            l.append(x+xx)
    return l


def get_max(l):
    maximum = max(l)
    return (l.index(maximum), maximum)


def vector_normarize(v):
    total = sum(v)
    return map(lambda x: float(x) / float(total), v)

def delete_dir(dir):
    ## Try to remove tree; if failed show an error using try...except on screen
    try:
        shutil.rmtree(dir)
    except OSError, e:
        print ("Warning: %s - %s." % (e.filename, e.strerror))


def get_similarity_score(docs1, docs2):
    set1 = set(docs1)
    set2 = set(docs2)
    if len(set1) >= len(set2):
        m = float(len(set2))
    else:
        m = float(len(set1))
    if m == 0: return 0.0
    intersection = float(len(set1.intersection(set2)))
    return intersection / m


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def connect2mongo(host, port, user, pwd, db_name):
    connection = MongoClient(host, port)
    db = connection[db_name]
    if user != '' and pwd != '':
        db.authenticate(user, pwd)
    return connection, db


def create_mongo_index(collection, field, type=u'ascending'):
    try:
        if type == u'ascending':
            collection.create_index([(field, ASCENDING)])
        else: # descending
            collection.create_index([(field, DESCENDING)])
    except Exception as e:
        print('exception raise in create_mongo_index: %s' % e.message)


def get_des_and_remove_tags(content):
    sentences = content.split(u'\n')

    if len(sentences) < 3:
        return None, None

    des = sentences[1]
    if u'[ tags ]' in sentences[len(sentences) - 1]:
        body = u'\n'.join(sentences[2:len(sentences) - 1])
    else: body = u'\n'.join(sentences[2:])
    return des, body


def is_exist(d, item):
    try:
        _ = d[item]
        return True
    except:
        return False


def get_time_at_present():
    now = datetime.now()
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f')






if __name__ == '__main__':
    ind, m = get_max([1,4,2,3,5,0])
    pass