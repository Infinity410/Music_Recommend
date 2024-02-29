import difflib
import random
import os
import numpy as np
import tensorflow as tf
import pandas
import warnings
from keras.models import load_model
from keras import Model
import eyed3

warnings.filterwarnings('ignore')
DIR = 'static/music_file'


def myfile(name):
    return os.path.join(DIR, name)


MUSIC_ROOT = myfile("mp3s")
mp3s = []
for root, subdirs, files in os.walk(MUSIC_ROOT):
    for fn in files:
        if fn.endswith('.mp3'):
            mp3s.append(os.path.join(root, fn))

# 导入音乐梅尔频谱图
songs = np.load('static/input_model/songs.npy', allow_pickle=True)
inputs = np.load('static/input_model/inputs.npy')

# 导入模型
cnn_model = load_model('static/input_model/song_classify.h5')
cnn_model.summary()

# 数据处理
vectorize_model = Model(inputs=cnn_model.input,
                        outputs=cnn_model.layers[-4].output)
vectors = vectorize_model.predict(inputs)

# 推荐歌曲
from collections import Counter
from sklearn.neighbors import NearestNeighbors

nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(vectors)


def most_similar_songs(song_idx):
    distances, indices = nbrs.kneighbors(
        vectors[song_idx * 10: song_idx * 10 + 10])
    c = Counter()
    for row in indices:
        for idx in row[1:]:
            c[idx // 10] += 1
    return c.most_common()


# 调试
def song_name(song_idx):
    return os.path.basename(songs[song_idx]['path'])


def print_similar_songs(song_idx, start=1, end=6):
    print("指定歌曲:", song_name(song_idx))
    # 跳过第一相似的：本身
    for idx, score in most_similar_songs(song_idx)[start:end]:
        print(f"[相似度{score}] {song_name(idx)}")


# 全部歌曲
for s in range(len(songs)):
    print(f'{s} {song_name(s)}')

class_mapping = [
    'hippop合集', 'jazz合集', 'milet的vision', '华语怀旧', '古典', '私货', '结束乐队专辑', '英语流行'
]


# 获取音乐时长
def get_duration_mp3(file_path):
    mp3Info = eyed3.load(file_path)
    secs = mp3Info.info.time_secs
    mat_min = int(secs / 60)
    mat_secs = int(secs % 60)
    if mat_min < 10:
        mat_min = '0' + str(mat_min)
    if mat_secs < 10:
        mat_secs = '0' + str(mat_secs)
    mat_time = str(mat_min) + ':' + str(mat_secs)
    return mat_time


# 封装音乐数据
def get_music_list(initial):
    music_list = []

    for i in range(5):
        per = {}
        # 风格
        name = os.path.basename(os.path.dirname(mp3s[initial[i]]))
        # 音乐地址
        mp3 = mp3s[initial[i]]
        print(mp3)
        mp3_time = get_duration_mp3(mp3)
        print(mp3_time)
        # 音乐风格名
        per["album"] = name
        # 音乐地址
        per["audio_url"] = '/' + mp3.replace('\\', '/')
        # 音乐信息
        per["name"] = os.path.basename(mp3s[initial[i]])
        # 音乐时间
        per["time"] = mp3_time
        # 音乐id
        per["id"] = int(initial[i])
        # 随机获得背景图片
        per["cover"] = f'/static/background/background_{random.randint(0, 7)}.jpg'
        music_list.append(per)
    # print(music_list)
    return music_list


# 随机获得5首歌曲信息
def net_music_list():
    initial = random.sample(range(0, 220), 5)
    return get_music_list(initial)


# 获得同种类型的5首歌曲的信息
def net_recommend_genre(album_name):
    global class_mapping
    src_dir_path = f'static/music_file/mp3s/{album_name}'
    print(src_dir_path)
    files = [os.path.join(src_dir_path, f) for f in os.listdir(src_dir_path)]
    random_files = random.sample(files, 5)
    # print(random_files)
    initial = []

    for i in range(5):
        data = os.path.basename(random_files[i])
        for j, x in enumerate(mp3s):
            if x.find(data) != -1:
                initial.append(j)

    return get_music_list(initial)


# 对喜欢的歌曲进行推荐
def net_predict_music(music_index):
    initial = []
    print("指定歌曲:", song_name(int(music_index)))
    for idx, score in most_similar_songs(int(music_index))[1:6]:
        # print(idx,score)
        print(f"[相似度{score}] {song_name(idx)}")
        initial.append(idx)

    return get_music_list(initial)