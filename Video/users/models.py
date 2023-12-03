from django.db import models
from django.contrib.auth.models import AbstractUser
from Video.utils.base_models import BaseModel


# Create your models here.

class UserModel(AbstractUser, BaseModel):
    """用户模型类，继承Django自带的AbstractUser类，并继承自BaseModel类"""
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=True)
    real_name = models.CharField(max_length=20, verbose_name='真实姓名', null=True, blank=True)
    nationality = models.CharField(max_length=20, verbose_name='国籍', null=True, blank=True)
    city = models.CharField(max_length=20, verbose_name='城市', null=True, blank=True)
    user_icon = models.FileField(max_length=200, verbose_name='用户头像', null=True, blank=True,default='avatar.jpg')
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)
    sex = models.CharField(max_length=4, verbose_name='性别', null=True, blank=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username


# 用户之间的模型类
class UserFocusModel(BaseModel):
    """ 两个属性表达了：每个用户之间的关联关系"""
    cur_user = models.ForeignKey('UserModel', verbose_name='当前用户',related_name='current_user_list', on_delete=models.CASCADE)
    focus_user = models.ForeignKey('UserModel', verbose_name='关注用户',related_name='focus_user_list', on_delete=models.CASCADE)
    class Meta:
        db_table = 't_user_focus'
        verbose_name = '用户关注表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.cur_user.usernaem + self.focus_user.username