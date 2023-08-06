# -*- coding: utf-8 -*-

import hashlib
import os
import typing
import uuid
from datetime import timedelta

from flask import current_app, request
from minio.error import MinioException
from werkzeug.datastructures import FileStorage

from .error import MinioError

"""
minio 文件上传
https://codecalamity.com/uploading-large-files-by-chunking-featuring-python-flask-and-dropzone-js/
"""


class MinioFile(object):
    """
    对minio中存储的文件的描述
    :param bucket_name: 存储的桶
    :param object_name: 存储在minio中对象名称
    :param object_size: 存储在minio中对象的大小
    """

    def __init__(self, bucket_name: str, object_name: str, object_size: int):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.object_size = object_size


def get_file_md5(file_name: str) -> str:
    """
    计算文件的md5
    :param file_name: 文件的路径
    :return: 文件的md5字符串
    """
    m = hashlib.md5()
    with open(file_name, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


def put_file(bucket_name: str,
             file_name: str,
             file_path: str,
             content_type='application/octet-stream') -> str:
    """
    将文件上传到minio
    :param bucket_name: 桶名称
    :param file_name: 对象名称
    :param file_path: 本地文件路径
    :param content_type: 内容类型
    :return: 保存到minio中的文件名称
    """
    try:
        minio_client = current_app.minio_manager.connection
        is_exists = minio_client.bucket_exists(bucket_name)
        if not is_exists:
            minio_client.make_bucket(bucket_name)

        md5 = get_file_md5(file_path)
        _name, file_type = os.path.splitext(file_name)
        object_name = md5 + file_type
        try:
            minio_client.stat_object(bucket_name, object_name)
        except MinioException:
            minio_client.fput_object(bucket_name, object_name, file_path, content_type)
        return object_name
    except Exception as ex:
        raise MinioError(f"将文件上传到minio,error{ex}")


def put_object(bucket_name: str,
               object_name: str,
               file_stream: typing.Union[bytes, bytearray],
               content_type='application/octet-stream') -> MinioFile:
    """
    将文件流上传到minio
    :param bucket_name: 桶名称
    :param object_name: 对象名称
    :param file_stream: 文件流
    :param content_type: 内容类型
    :return:
    """
    try:
        temp_space = current_app.config['MINIO_TEMP_SPACE']
        if not os.path.exists(temp_space):
            os.makedirs(temp_space)

        save_path = os.path.join(temp_space, object_name)
        with open(save_path, 'ab') as f:
            f.write(file_stream)

        save_name = put_file(bucket_name, object_name, save_path, content_type)
        file_size = os.path.getsize(save_path)
        os.remove(save_path)
        return MinioFile(bucket_name, save_name, file_size)
    except Exception as ex:
        raise MinioError(f"将文件流上传到minio,error{ex}")


def put_chunk_object(bucket_name: str,
                     object_name: str,
                     file_stream: typing.Union[bytes, bytearray],
                     chunk_index: int,
                     chunk_byte_offset: int,
                     total_chunk_count: int,
                     content_type='application/octet-stream') -> typing.Union[None, MinioFile]:
    """
    文件分块上传
    :param bucket_name: 桶名称
    :param object_name: 对象名称
    :param file_stream: 文件流
    :param chunk_index: 分块索引
    :param chunk_byte_offset: 分块偏移
    :param total_chunk_count: 分块总数
    :param content_type: 文件内容类型
    :return: 文件分块上传完成后返回MinioFile,否则返回none表示没有上传完成
    """
    try:
        temp_space = current_app.config['MINIO_TEMP_SPACE']
        if not os.path.exists(temp_space):
            os.makedirs(temp_space)

        save_path = os.path.join(temp_space, object_name)
        with open(save_path, 'ab') as f:
            f.seek(int(chunk_byte_offset))
            f.write(file_stream)

        if chunk_index + 1 == total_chunk_count:
            save_name = put_file(bucket_name, object_name, save_path, content_type)
            file_size = os.path.getsize(save_path)
            os.remove(save_path)
            return MinioFile(bucket_name, save_name, file_size)
        return None
    except Exception as ex:
        raise MinioError(f"文件分块上传,error{ex}")


def put_dropzone_object(bucket_name: str, f: FileStorage) -> typing.Union[None, MinioFile]:
    """
    dropzone插件上传文件,其中默认处理了分块上传和非分块分块上传，
    需要用到request.form对象：
    request.form['dzuuid'] 当前上传的ID，一般未uuid对象，
    request.form['dzchunkindex'] 分块索引，为空表示不分块上传
    request.form['dzchunkbyteoffset'] 分块的偏移量，
    request.form['dztotalchunkcount'] 分块的总量

    :param bucket_name: 桶名称
    :param f: flask upload file
    :return: 文件分块上传完成后返回MinioFile,否则返回none表示没有上传完成
    """
    try:
        _name, file_type = os.path.splitext(f.filename)
        # 对保存到临时空间的文件重命名
        dzuuid = request.form.get('dzuuid', None)
        if dzuuid:
            temp_file_name = dzuuid + file_type
        else:
            temp_file_name = str(uuid.uuid4()) + file_type

        # 是不分块上传的情况，直接上传文件
        chunk_index = request.form.get('dzchunkindex', None)
        if not chunk_index:
            return put_object(bucket_name, temp_file_name, f.stream.read())

        # 分块上传，需要分块上传后，判断分块完成后写入数据库数据。
        chunk_index = int(chunk_index)
        chunk_byte_offset = int(request.form['dzchunkbyteoffset'])
        total_chunk_count = int(request.form['dztotalchunkcount'])
        return put_chunk_object(bucket_name, temp_file_name, f.stream.read(),
                                chunk_index, chunk_byte_offset, total_chunk_count, f.content_type)
    except Exception as ex:
        raise MinioError(f"dropzone插件上传文件,error{ex}")


def get_presigned_object(bucket_name: str, object_name: str, expires=timedelta(days=7)):
    """
    获取预签名对象，用于分享功能，返回url
    :param bucket_name: 桶名称
    :param object_name: 对象名称
    :param expires: 过期时间
    :return: 返回分享的url
    """
    return current_app.minio_manager.connection.presigned_get_object(bucket_name, object_name, expires)


def fget_object(bucket_name: str, object_name: str) -> str:
    """
    从minio中获取对象转存到本地文件
    :param bucket_name: 桶名称
    :param object_name: 对象名称
    :return: 本地文件路径
    """
    try:
        temp_space = current_app.config['MINIO_TEMP_SPACE']
        if not os.path.exists(temp_space):
            os.makedirs(temp_space)

        save_path = os.path.join(temp_space, "download", object_name)
        if not os.path.exists(save_path):
            current_app.minio_manager.connection.fget_object(bucket_name, object_name, save_path)
        return save_path
    except Exception as ex:
        raise MinioError(f"从minio中获取对象转存到本地文件,error{ex}")
