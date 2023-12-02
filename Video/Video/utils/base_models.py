from django.db import models


class BaseModel(models.Model):
    """
    项目中所有模型类的父类，里面定义了一些公共属性或者字段
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        abstract = True