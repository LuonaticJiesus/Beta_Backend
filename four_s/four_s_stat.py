import datetime
from dateutil.relativedelta import relativedelta

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from four_s.models import Stat, Post, Block, PointBlock
from utils.time_util import get_zero_time


def get_stat_dict(state: int):
    ret = {}
    zero_time = get_zero_time()
    if state == 1:
        for i in range(0, 12):
            step_time = zero_time - relativedelta(months=i)
            step_time_str = step_time.strftime('%Y-%m')
            ret[step_time_str] = 0
    else:
        for i in range(0, 7):
            step_time = zero_time - relativedelta(days=i)
            step_time_str = step_time.strftime('%Y-%m')
            ret[step_time_str] = 0
    return ret


def cmp(element):
    return element['time']


@csrf_exempt
def stat_post_time(request):
    if request.method != 'GET':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        state = request.GET.get('state')
        # check param
        if state is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        state = int(state)
        if state not in [1, 2]:
            return JsonResponse({'status': -1, 'info': '参数错误'})
        # db
        with transaction.atomic():
            post_query_set = Post.objects.filter(user_id=user_id).order_by('-time')
            blocks = Block.objects.all()
            block_id_name = {}
            for b in blocks:
                block_id_name[b.block_id] = b.name
            stat_dict = get_stat_dict(state)
            time_format = '%Y-%m' if state == 1 else '%Y-%m-%d'
            for p in post_query_set:
                p_time_str = p.time.strftime(time_format)
                if p_time_str in stat_dict.keys():
                    stat_dict[p_time_str] += 1
            ret = []
            for k in stat_dict.keys():
                ret.append({'time': k, 'post_num': stat_dict[k]})
            ret.sort(key=cmp, reverse=False)
            return JsonResponse({'status': 0, 'info': '查询成功', 'data': ret})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})


@csrf_exempt
def stat_post_block(request):
    if request.method != 'GET':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        # db
        with transaction.atomic():
            post_query_set = Post.objects.filter(user_id=user_id)
            block_ids = set()
            for p in post_query_set:
                block_ids.add(p.block_id)
            ret = []
            for block_id in block_ids:
                block_name = Block.objects.get(block_id=block_id).name
                ret.append({'name': block_name, 'value': post_query_set.filter(block_id=block_id).count()})
            return JsonResponse({'status': 0, 'info': '查询成功', 'data': ret})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})


@csrf_exempt
def stat_point_block(request):
    if request.method != 'GET':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        # db
        with transaction.atomic():
            point_query_set = PointBlock.objects.filter(user_id=user_id)
            ret = []

            for p in point_query_set:
                block_name = Block.objects.get(block_id=p.block_id).name
                ret.append({'name': block_name, 'value_plus': p.point_add, 'value_minus': p.point_sub})
            return JsonResponse({'status': 0, 'info': '查询成功', 'data': ret})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})


@csrf_exempt
def stat_point_time(request):
    if request.method != 'GET':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        state = request.GET.get('state')
        # check param
        if state is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        state = int(state)
        if state not in [1, 2]:
            return JsonResponse({'status': -1, 'info': '参数错误'})
        with transaction.atomic():
            stat_query_set = Stat.objects.filter(user_id=user_id)
            stat_dict = get_stat_dict(state)
            time_format = '%Y-%m' if state == 1 else '%Y-%m-%d'
            for s in stat_query_set:
                s_time_str = s.time.strftime(time_format)
                if s_time_str in stat_dict.keys():
                    stat_dict[s_time_str] += 1

    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})
