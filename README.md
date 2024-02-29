# 音乐门户网站+音乐推荐系统

* 本系统采用的推荐算法：分析音频特征，做基于内容的音乐推荐（Content-Based Filtering,CBF）
* 采用的数据集：加拿大维多利亚大学的genres数据集训练模型
* 设计思路：利用本地音乐库，将其进行分门别类，当用户给定一首歌，该歌曲将送入训练好的模型，推荐风格类似的其他曲目
* 采用模型：基础的卷积神经网络模型（一维卷积池化堆叠+全连接分类）

# 运行前命令
``` 
python manage.py makemigration

python manage.py migrate

python manage.py createsuperuser

python manage.py startapp recommend

python manage.py startapp player_rec

python manage.py startapp index

python manage.py startapp ranking

python manage.py startapp play

python manage.py startapp comment

python manage.py startapp search

python manage.py startapp user
```

# SQL文件、运行截图及必要文件
* 在release中自行下载
