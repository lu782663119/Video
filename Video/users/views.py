from io import BytesIO

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
# 检查用户名是否重复
from django.views.decorators.http import require_http_methods
from .models import UserModel


@require_http_methods(['POST'])
def check_username(request):
    """ 验证注册的用户是否唯一"""
    # {'valid':True} 返回的时True 表示验证通过
    result_data = {'valid': True}  # 默认是通过验证的
    un = request.POST.get('username')  # 接受表单的用户名
    user = UserModel.objects.filter(username=un)  # 查询数据库中是否有该用户名
    if user:
        # 已经存在用户名
        result_data['valid'] = False
    return JsonResponse(result_data)


# 生成验证码
@require_http_methods(['GET'])
def generate_code(request):
    """ 生成验证码"""
    # 生成验证码
    from PIL import Image, ImageDraw, ImageFont
    import random
    # 生成验证码
    # 定义背景颜色

    # 定义变量 用于画面的背景颜色 、宽、 高
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(100, 255))
    width = 120
    height = 38
    # 创建画面对象
    im = Image.new('RGB', (width, height), bg_color)
    # 创建画笔的颜色
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪声点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill == fill)

    # 定义验证码的备选值
    str1 = 'ABCDEFGHIJKLMNOPQRSTUVXYZ0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 绘制4个字
    # 构造字体对象 字体对象的路径：
    font = ImageFont.truetype('ebrima.ttf', 23)
    # 构造字体的颜色
    # fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, -3), rand_str[0], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    draw.text((25, -3), rand_str[1], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    draw.text((50, -3), rand_str[2], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    draw.text((75, -3), rand_str[3], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    # 释放画笔
    del draw
    request.session['verify_code'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中 文件类型：png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端 MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')