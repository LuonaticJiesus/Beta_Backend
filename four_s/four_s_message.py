import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from four_s.models import Message, UserInfo, Block


def wrap_message(message):
    m_dict = message.to_dict()
    m_dict['receiver_name'] = UserInfo.objects.get(user_id=message.receiver_id).name
    if message.message_type in [101, 102]:
        m_dict['sender_name'] = Block.objects.get(block_id=message.sender_id).name
    elif message.message_type in [207, 304, 305]:
        m_dict['sender_name'] = UserInfo.objects.get(user_id=message.sender_id).name
    else:
        m_dict['sender_name'] = '系统消息'
    return m_dict


@csrf_exempt
def message_query_rec(request):
    if request.method != 'GET':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        with transaction.atomic():
            messages_queryset = Message.objects.filter(receiver_id=user_id)
            messages = []
            for message in messages_queryset:
                m_dict = wrap_message(message)
                messages.append(m_dict)

            def cmp(element):
                return element['time']

            messages.sort(key=cmp, reverse=True)
            return JsonResponse({'status': 0, 'info': '查询成功', 'data': messages})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，查询失败'})


@csrf_exempt
def message_confirm(request):
    if request.method != 'POST':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        data = json.loads(request.body)
        message_id = data.get('message_id')
        confirm = data.get('confirm')
        # check params
        if message_id is None or confirm is None:
            return JsonResponse({'status': -1, 'info': '缺少参数'})
        message_id = int(message_id)
        confirm = int(confirm)
        if confirm not in [0, 1]:
            return JsonResponse({'status': -1, 'info': '参数错误'})
        # db
        with transaction.atomic():
            message_query_set = Message.objects.filter(message_id=message_id).filter(receiver_id=user_id)
            if not message_query_set.exists():
                return JsonResponse({'status': -1, 'info': '消息不存在'})
            message_query_set.update(state=confirm)
            return JsonResponse({'status': 0, 'info': '消息状态已更新'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，更新失败'})


@csrf_exempt
def message_confirm_all(request):
    if request.method != 'POST':
        return JsonResponse({'status': -1, 'info': '请求方式错误'})
    try:
        user_id = int(request.META.get('HTTP_USERID'))
        with transaction.atomic():
            Message.objects.filter(receiver_id=user_id).filter(status=0).update(state=1)
            return JsonResponse({'status': 0, 'info': '所有消息状态已更新'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': -1, 'info': '操作错误，更新失败'})
