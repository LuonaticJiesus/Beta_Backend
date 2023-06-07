import json
import os
import time

from django.db import transaction
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from qcloud_cos import CosConfig, CosS3Client

from BackEnd import global_config
from four_s.models import Post, Notice, File, Block

tencent_cos_secret_id = global_config['tencent_cos']['secret_id']
tencent_cos_secret_key = global_config['tencent_cos']['secret_key']
tencent_cos_region = global_config['tencent_cos']['region']
tencent_cos_bucket = global_config['tencent_cos']['bucket']
tencent_cos_config = CosConfig(Region=tencent_cos_region, SecretId=tencent_cos_secret_id,
                               SecretKey=tencent_cos_secret_key, Timeout=5)
tencent_cos_client = CosS3Client(tencent_cos_config, retry=0)

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
        if file is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        suffix = os.path.splitext(file.name)[-1]
        file_key = rand_str() + suffix
        response = tencent_cos_client.upload_file_from_buffer(
            Bucket=tencent_cos_bucket, Key=file_key, Body=file)
        if response is None:
            return JsonResponse({'status': -1, 'info': '上传失败'})
        file_url = 'https://{}.cos.{}.myqcloud.com/{}'.format(tencent_cos_bucket, tencent_cos_region, file_key)
        return JsonResponse({'status': 0, 'info': '上传成功',
                             'data': {'url': file_url}})
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
        # db
        with transaction.atomic():
            if (obj_id == 1 and not Post.objects.filter(post_id=obj_id).exists()) \
                    or (obj_id == 2 and not Notice.objects.filter(notice_id=obj_id).exists()) \
                    or (obj_id == 3 and not Block.objects.filter(block_id=obj_id).exists()):
                return JsonResponse({'status': -1, 'info': '类型错误'})
            file_query_set = File.objects.filter(obj_type=obj_type).filter(obj_id=obj_id)
            url_set = set()
            for f in file_query_set:
                url_set.add(f.obj_url)
            for url in url_list:
                url = str(url)
                if url in url_set:
                    continue
                new_file = File(obj_type=obj_type, obj_id=obj_id, obj_url=url)
                new_file.save()
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
            for f in File.objects.filter(obj_id=obj_id).filter(obj_type=obj_type):
                url_list.append(f.obj_url)
            return JsonResponse({'status': 0, 'info': '查询成功', 'data': {'url_list': url_list}})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})