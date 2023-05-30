# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
import json

from django.db import models


class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    card_id = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    avatar = models.CharField(max_length=200, null=True)
    point = models.IntegerField()

    def to_dict(self):
        ret = {
            'user_id': self.user_id,
            'name': self.name,
            'point': self.point
        }
        if self.avatar is not None:
            ret['avatar'] = self.avatar
        if self.card_id is not None:
            ret['card_id'] = self.card_id
        if self.phone is not None:
            ret['phone'] = self.phone
        if self.email is not None:
            ret['email'] = self.email
        return ret


class UserLogin(models.Model):
    user_id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    user_id = models.IntegerField()
    txt = models.TextField()
    block_id = models.IntegerField()
    time = models.DateTimeField()

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'title': self.title,
            'user_id': self.user_id,
            'txt': self.txt,
            'block_id': self.block_id,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class PostLike(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField()


class PostFavor(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField()


class PostChosen(models.Model):
    post_id = models.IntegerField()
    block_id = models.IntegerField()


class Block(models.Model):
    block_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    time = models.DateTimeField()
    avatar = models.CharField(max_length=200)
    info = models.CharField(max_length=200)
    # <0: 无需认证，0:需要路人认证，1:成员认证，2:助理认证，3:管理认证，>=4：超管认证
    approve_permission = models.IntegerField()

    def to_dict(self):
        ret = {
            'block_id': self.block_id,
            'name': self.name,
            'avatar': self.avatar,
            'info': self.info,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'approve_permission': self.approve_permission
        }
        return ret


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    parent_id = models.IntegerField(null=True)  # null: to post, else to comment
    reply_user_id = models.IntegerField(null=True)  # null: to post, else to comment
    root_comment_id = models.IntegerField(null=True)  # null: to post, else: the first comment
    txt = models.TextField()
    time = models.DateTimeField()

    def to_dict(self):
        ret = {
            'comment_id': self.comment_id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'txt': self.txt,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S')
        }
        if self.parent_id is not None:
            ret['parent_id'] = self.parent_id
        if self.root_comment_id is not None:
            ret['root_comment_id'] = self.root_comment_id
        if self.reply_user_id is not None:
            ret['reply_user_id'] = self.reply_user_id
        return ret


class CommentLike(models.Model):
    user_id = models.IntegerField()
    comment_id = models.IntegerField()


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    txt = models.TextField()
    user_id = models.IntegerField()
    block_id = models.IntegerField()
    time = models.DateTimeField()
    ddl = models.DateTimeField()

    def to_dict(self):
        return {
            'notice_id': self.notice_id,
            'title': self.title,
            'txt': self.txt,
            'user_id': self.user_id,
            'block_id': self.block_id,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'ddl': self.ddl.strftime('%Y-%m-%d %H:%M:%S')
        }


class NoticeConfirm(models.Model):
    user_id = models.IntegerField()
    notice_id = models.IntegerField()


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    receiver_id = models.IntegerField()
    message_type = models.IntegerField()
    time = models.DateTimeField()
    state = models.IntegerField()  # (0:未查看, 1:已查看)
    sender_id = models.IntegerField(null=True)
    source_id = models.IntegerField()
    source_content = models.CharField(max_length=200, null=True)
    related_id = models.IntegerField()
    related_content = models.CharField(max_length=200, null=True)
    point = models.IntegerField(null=True)

    def to_dict(self):
        ret = {
            'message_id': self.message_id,
            'receiver_id': self.receiver_id,
            'message_type': self.message_type,
            'state': self.state,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'source_id': self.source_id,
            'related_id': self.related_id,
        }
        if self.source_content is not None:
            ret['source_content'] = self.source_content
        if self.related_content is not None:
            ret['related_content'] = self.related_content
        if self.sender_id is not None:
            ret['sender_id'] = self.sender_id
        if self.point is not None:
            ret['point'] = self.point
        return ret


class Permission(models.Model):
    user_id = models.IntegerField()
    block_id = models.IntegerField()
    permission = models.IntegerField()


class Contribution(models.Model):
    user_id = models.IntegerField()
    block_id = models.IntegerField()
    contribution = models.IntegerField()


class EmailPro(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=50,
                                 choices=(('regster', '邮箱注册'), ('forget', '忘记密码')),
                                 verbose_name='发送类型')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    card_id = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    avatar = models.CharField(max_length=200, null=True)
