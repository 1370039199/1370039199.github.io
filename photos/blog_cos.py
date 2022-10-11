# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

import io
import os
import sys
import logging
import shutil
import urllib2
import string

# ��Ѷ��COSV5Python SDK, Ŀǰ����֧��Python2.6��Python2.7�Լ�Python3.x
# pip��װָ��:pip install -U cos-python-sdk-v5
# cos���¿��õ���,����https://www.qcloud.com/document/product/436/6224

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# �����û�����, ����secret_id, secret_key, region
# appid�����������Ƴ�,���ڲ���Bucket�д���appid��Bucket��bucketname-appid���
secret_id = 'AKIDKXpwpUO7C6mEVXKsDKBpFSP6Ys41iANM'     # �滻Ϊ�û���secret_id
secret_key = 'lQs52jNtDOOCm9HNGwOfjaDbmjSxDF3f'     # �滻Ϊ�û���secret_key
region = 'ap-chengdu'    # �滻Ϊ�û���region
token = None               # ʹ����ʱ��Կ��Ҫ����Token��Ĭ��Ϊ��,�ɲ���
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # ��ȡ���ö���
client = CosS3Client(config)
print("��������ѶCOS")


galleries = []
json_name = "galleries.yaml"    # ͼƬ�����ļ�����
bucket_name = "hyh1370039199-1313349927"      # ��ѶCOS�洢Ͱ����
photos_name = "galleries/"      # ��ѶCOSһ�����Ŀ¼

# json�ļ�����·�� ����D://blog/source/_data/galleries.json
cwd = os.getcwd().replace("photos", "_data")
json_cwd = os.path.join(cwd, json_name).replace('\\', '/').replace(':', ':/')

# �鿴 json �ļ��Ƿ��Ѵ���
def json_file_exists():
    if os.path.exists(json_cwd):
        os.remove(json_cwd)

# ��ȡ���������Ϣ
def get_galleries_data():
    global galleries_name
    galleries_name = []
    # ��ѯ���Ŀ¼����������
    response = client.list_objects(
        Bucket= bucket_name,
        Prefix= photos_name,
        Delimiter='/',
    )
    CommonPrefixes = response['CommonPrefixes']
    for Prefixes in CommonPrefixes:
        Prefix = Prefixes['Prefix']
        gallery_name = Prefix.split("/")[1]
        galleries_name.append(gallery_name)
        # ��ѯ���Ŀ¼���������ļ�������
        response = client.list_objects(
            Bucket= bucket_name,
            Prefix= photos_name + gallery_name + '/',
            Delimiter='/',
        )
        contents = response['Contents']
        # ���ļ���������Ƭ��ӵ� photos_list �б�
        photos_list = []
        for i in range(len(contents)):
            content = contents[i]['Key'].split("/")[2]
            photos_list.append(content)
        del photos_list[0]
        # �����ӵ� gallery_dict �ֵ���
        gallery_dict = dict(name=1, cover=1, description=1, photos=1)
        gallery_dict.update(name = gallery_name)
        gallery_dict.update(cover = photos_list[0])
        gallery_dict.update(photos = photos_list[0:])
        photos_list = []
        # ���������ӵ� galleries �б���
        galleries.append(gallery_dict)
    print("��������������")

# ����д��
def galleries_data_write():
    with io.open(json_cwd.decode('UTF-8'), 'w', encoding='UTF-8') as file:
        # �������ݸ�ʽ
        data0 = str(galleries).replace("}, {" , "},\n {")
        data1 = data0.replace("[{", "[\n {")
        data = data1.replace("}]", "}\n]")
        file.write(data.decode('UTF-8'))
        print("����д�����")

# �����ļ���
def mkdir_galleries(file):
    if os.path.exists(file):
        shutil.rmtree(file)
    os.mkdir(file)

# # �����������Ŀ¼�Ͷ�Ӧ��index.md�ļ�
def galleries_index():
    for name in galleries_name:
        gallery_index_dict= dict(title = name, layout = 'photo', comments = "false")
        mkdir_galleries(name)
        gallery_index_cwd = os.path.join(os.getcwd(), name , "index.md").replace('\\', '/').replace(':', ':/')
        with io.open(gallery_index_cwd.decode('UTF-8'), 'w', encoding='UTF-8') as file:
            data0 = str(gallery_index_dict)
            data1 = data0.replace("{", "---\n").replace(",","\n").replace("}", "\n---")
            data = data1.replace("'", "").replace("photo",'''"photo"''').replace(" layout","layout").replace(" comments","comments")
            file.write(data.decode('UTF-8'))
    print("index����д�����")

if __name__ == "__main__":
    json_file_exists()      # �鿴 json �ļ��Ƿ��Ѵ���
    get_galleries_data()    # ��ȡ���������Ϣ
    galleries_data_write()    # ͼ������д��
    galleries_index()         # �����������Ŀ¼�Ͷ�Ӧ��index.md�ļ�