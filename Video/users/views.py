from io import BytesIO

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# 检查用户名是否重复
from django.views import View
from django.views.decorators.http import require_http_methods
from .models import UserModel, UserFocusModel



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


@require_http_methods(['POST'])
def verify_code(request):
    """ 验证验证码是否正确的用户是否唯一"""
    # {'valid':True} 返回的时True 表示验证通过
    result_data = {'valid': True}  # 默认是通过验证的
    code = request.POST.get('captcha')  # 接受表单的验证码
    code_session = request.session.get('verify_code')  # 获取session中的验证码

    if not code == code_session:
        # 两个不相等 则返回不通过
        result_data['valid'] = False
    return JsonResponse(result_data)


# 用户注册
@require_http_methods(['POST'])
def submit_register(request):
    """ 用户注册"""
    # 接收表单数据
    user = UserModel.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
        phone=request.POST['phone'],

    )
    user.phone = request.POST['phone']
    user.sex = request.POST['sex']
    user.save()
    result_data = {'code': 200, 'msg': '注册成功'}
    return JsonResponse(result_data)


class UserInfoView(LoginRequiredMixin, View):
    """ 用户信息 包括用户信息的修改"""

    def get(self, request):
        return render(request, 'user_info.html')  # 渲染用户信息页面

    # 修改用户信息
    def post(self, request):
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        age = int(request.POST.get('age', 0))
        sex = request.POST.get('sex', None)
        real_name = request.POST.get('real_name', None)
        nationality = request.POST.get('nationality', None)
        city = request.POST.get('city', None)
        # 获取上传的数据 如果没有 则返回None
        icon = request.FILES.get('user_icon', None)
        if not icon:
            return HttpResponse('没有选中任何文件')
        # 对于FileField类型不能用update（）去操作，update 会失效，因此应该使用save去实现
        current_user = request.user
        current_user.user_icon = icon
        current_user.phone = phone
        current_user.email = email
        current_user.sex = sex
        current_user.age = age
        current_user.real_name = real_name
        current_user.city = city
        current_user.nationality = nationality
        current_user.save()
        return self.get(request)


class UserListView(LoginRequiredMixin, View):
    """ 播客用户列表"""

    def get(self, request):
        # 获得从浏览器传来的页3码 默认第一页
        page_num = request.GET.get('page', 1)
        # 从数据库中查询数据，排除当前用户
        user_list = UserModel.objects.exclude(id=request.user.id)
        paginator = Paginator(user_list, 10)  # 每页显示十条信息
        # 获取页码范围
        page_range = paginator.page_range
        try:
            # 创建一个page对象
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
            # 如果传入的不是一个整数，则取第一页
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            # 如果获得的页码超出范围 则直接取最后一位
        # 查询当前用户已经关注的用户列表
        focus_ids = UserFocusModel.objects.filter(cur_user__id=request.user.id).values_list('focus_user__id', flat=True)
        # 将列表中嵌套的元组展开切一个列表

        # 往模板中传入数据
        return render(request, 'user_list.html',
                      {'user_page': page,
                       'page_range': page_range,
                       'current_page': page.number,
                       'focus_ids': focus_ids})


# 添加关注
@require_http_methods(['GET'])
def add_focus(request):
    """
    添加关注
    ：:param request: 请求参数中必须包含：被关注的用户ID
    ：retrun
    """
    focus_id = request.GET.get('focus_id')
    focus_user = UserModel.objects.get(id=focus_id)
    UserFocusModel.objects.create(cur_user=request.user, focus_user=focus_user)
    return redirect('/users/list_user/')


@require_http_methods(['POST'])
def submit_login(request):
    """ 用户登录"""
    day = int(request.POST.get('remember', '1'))
    # 接收表单数据
    user = auth.authenticate(
        request=request,  # 请求对象
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )

    # 判断用户是否为空
    if user:  # 用户登录成功
        print(user)
        auth.login(request, user)  # 设置session,将用户保存到session中
        request.session.set_expiry(day * 24 * 60 * 60)  # 设置session过期时间
        return redirect('/videos/index/')

    return redirect('/users/login/')  # 失败跳回登录页面


# 退出登录
@login_required(login_url='/users/login/')
def logout(request):
    auth.logout(request)
    return render(request, template_name='login.html')


@require_http_methods(['GET'])
@login_required(login_url='/users/login/')
def my_focus(request):
    # 从数据库中查询数据，先查询我的关注用户的所有ID列表
    ids = UserFocusModel.objects.filter(cur_user__id=request.user.id).values_list('focus_user__id', flat=True)
    # 根据IDS列表 过滤查询符合条件的所有博客
    user_list = UserModel.objects.filter(id__in=ids).all()

    # 往模板中传入数据
    return render(request, 'my_focus.html', {'user_list': user_list})



def delete_focus(request):
    """取消关注"""
    focus_id = request.GET.get('focus_id')
    focus_user = UserModel.objects.get(id=focus_id)
    current_user = request.user
    UserFocusModel.objects.filter(current_user__id=current_user.id, focus_user_id=focus_id).delete()
