import json
import os
import time

from django.db import transaction
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from qcloud_cos import CosConfig, CosS3Client

from BackEnd import global_config
from four_s.models import Post, Notice, File, Block, FileConn

tencent_cos_secret_id = global_config['tencent_cos']['secret_id']
tencent_cos_secret_key = global_config['tencent_cos']['secret_key']
tencent_cos_region = global_config['tencent_cos']['region']
tencent_cos_bucket = global_config['tencent_cos']['bucket']
tencent_cos_config = CosConfig(Region=tencent_cos_region, SecretId=tencent_cos_secret_id,
                               SecretKey=tencent_cos_secret_key, Timeout=10)


chars = 'abcdefghijklmnopqrstuvwxyz0123456789'


def rand_str():
    ret = str(time.time()).replace('.', '')
    size = 25 - len(ret)
    if size > 0:
        ret = ret + get_random_string(size, chars)
    return ret


@csrf_exempt
def file_upload(request):
    if request.method != 'POST':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        file = request.FILES.get('file', None)
        file_name = request.POST.get('name')
        if file is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        if file_name is not None:
            file_name = str(file_name)
        if len(file) > 10 * 1024 * 1024:
            return JsonResponse({'status': -1, 'info': '文件过大'})
        suffix = os.path.splitext(file.name)[-1]
        file_key = rand_str() + suffix
        # file_path = 'tmp/' + file_key
        # with open(file_path, 'wb') as f:
        #     file_data = file.file.read()
        #     f.write(file_data)
        try:
            tencent_cos_client = CosS3Client(tencent_cos_config, retry=0)
            response = tencent_cos_client.upload_file_from_buffer(
                Bucket=tencent_cos_bucket, Key=file_key, Body=file.file)
            # response = tencent_cos_client.put_object_from_local_file(
            #     Bucket=tencent_cos_bucket, Key=file_key, LocalFilePath=file_path)
        except Exception as e:
            print(e)
            return JsonResponse({'status': -1, 'info': '上传超时'})
        if response is None:
            return JsonResponse({'status': -1, 'info': '上传失败'})
        file_url = 'https://{}.cos.{}.myqcloud.com/{}'.format(tencent_cos_bucket, tencent_cos_region, file_key)
        new_file = File(url=file_url, name=file_name)
        new_file.save()
        return JsonResponse({'status': 0, 'info': '上传成功',
                             'data': {'url': file_url, 'file_id': new_file.file_id}})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，上传失败'})


@csrf_exempt
def file_connect(request):
    if request.method != 'POST':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        data = json.loads(request.body)
        obj_type = data.get('type')
        obj_id = data.get('id')
        url_list = data.get('url_list', [])
        # check params
        if obj_type is None or obj_id is None or url_list is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        obj_type = int(obj_type)
        if obj_type not in [0, 1, 2, 3]:
            return JsonResponse({'status': -1, 'info': '类型错误'})
        obj_id = int(obj_id)
        url_list = list(url_list)
        urls = []
        for url in url_list:
            urls.append(str(url))
        # db
        with transaction.atomic():
            if (obj_type == 1 and not Post.objects.filter(post_id=obj_id).exists()) \
                    or (obj_type == 2 and not Notice.objects.filter(notice_id=obj_id).exists()) \
                    or (obj_type == 3 and not Block.objects.filter(block_id=obj_id).exists()):
                return JsonResponse({'status': -1, 'info': '类型错误'})
            for url in urls:
                file_query_set = File.objects.filter(url=url)
                if not file_query_set.exists():
                    new_file = File(url=url)
                    new_file.save()
                    file_id = new_file.file_id
                else:
                    file_id = file_query_set[0].file_id
                conn_query_set = FileConn.objects.filter(obj_id=obj_id)\
                    .filter(obj_type=obj_type).filter(file_id=file_id)
                if not conn_query_set.exists():
                    new_conn = FileConn(file_id=file_id, obj_id=obj_id, obj_type=obj_type)
                    new_conn.save()
            return JsonResponse({'status': 0, 'info': '已关联'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，关联失败'})


@csrf_exempt
def file_list(request):
    if request.method != 'GET':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        obj_type = request.GET.get('type')
        obj_id = request.GET.get('id')
        # check params
        if obj_type is None or obj_id is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        obj_id = int(obj_id)
        obj_type = int(obj_type)
        if obj_type not in [0, 1, 2, 3]:
            return JsonResponse({'status': -1, 'info': '类型错误'})
        # db
        with transaction.atomic():
            url_list = []
            name_list = []
            for conn in FileConn.objects.filter(obj_id=obj_id).filter(obj_type=obj_type):
                f = File.objects.get(file_id=conn.file_id)
                url_list.append(f.url)
                name_list.append(f.name)
            return JsonResponse({'status': 0, 'info': '查询成功', 'data': {'url_list': url_list, 'name_list': name_list}})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})