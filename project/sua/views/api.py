from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import ListModelMixin

from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly
import project.sua.serializers as sirs
import project.sua.views.forms.serializers as firs
import project.sua.views.forms.mixins as mymixins
from project.sua.models import Sua, Proof, Application, Publicity, Activity, Student, Appeal, SuaGroup

from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = sirs.UserSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = sirs.GroupSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class StudentViewSet(
        viewsets.GenericViewSet,
        ListModelMixin,
        mymixins.AddFormMixin,
        mymixins.ChangeFormMixin,
        mymixins.DetailFormMixin,
        mymixins.DeleteFormMixin
    ):
    """
    API endpoint that allows students to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = sirs.StudentSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_fields = ('grade', 'classtype')

    template_name = None  # 请务必要添加这一行，否则会报错

    delete_success_url = '/'

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/student_form.html',  # 模板文件
        add_serializer_class=firs.AddStudentSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
        permission_classes = (IsAdminUser, )
    )
    def add(self, request):
        '''
        url: api/students/add/
        template: sua/student_form.html
        GET: 向模板代码提供空Student序列化器(serializer)，渲染并返回Student创建表单
        POST: 接受Student创建表单数据，创建Student实例，并重定向至Student实例详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(StudentViewSet, self).add(request)

    @detail_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/student_form.html',  # 模板文件
        change_serializer_class=firs.AddStudentSerializer,  # 序列化器
        change_success_url='/',  # 成功后的跳转url
        permission_classes = (IsAdminUser, )
    )
    def change(self, request, *args, **kwargs):
        '''
        url: api/students/<int:pk>/change/
        template: sua/student_form.html
        GET: 向模板代码提供pk对应的student的序列化器(serializer)，渲染并返回Student更新表单
        POST: 接受Student更新表单数据，更新Student实例及对应的User实例，并重定向至Student实例详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(StudentViewSet, self).change(request, *args, **kwargs)

    @detail_route(
        methods=['get'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        permission_classes = (IsTheStudentOrIsAdminUser,),
        template_name='sua/student_detail.html',  # 模板文件
        detail_serializer_class=firs.AddStudentSerializer,  # 序列化器
    )
    def detail(self, request, *args, **kwargs):
        '''
        url: api/students/<int:pk>/detail/
        template: sua/student_detail.html
        GET: 向模板代码提供pk对应的student的序列化器(serializer)，渲染并返回Student详情页面
        表单字段：表单字段与serializer.data一致
        '''
        return super(StudentViewSet, self).detail(request, *args, **kwargs)


class SuaGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows suagroups to be viewed or edited.
    """
    queryset = SuaGroup.objects.all()
    serializer_class = sirs.SuaGroupSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class SuaViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows suas to be viewed or edited.
    """
    queryset = Sua.objects.all()
    serializer_class = sirs.SuaSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/sua_form.html',  # 模板文件
        add_serializer_class=firs.AddSuaSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/suas/add/
        template: sua/sua_form.html
        GET: 返回空Sua序列化器，渲染Sua创建表单
        POST: 接受Sua创建表单数据，创建Sua实例，并重定向至对应的Activity详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(SuaViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows activities to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = sirs.ActivitySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/activity_form.html',  # 模板文件
        add_serializer_class=firs.AddActivitySerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/activities/add/
        template: sua/activity_form.html
        GET: 返回空Activity序列化器，渲染Activity创建表单
        POST: 接受Activity创建表单数据，创建Activity实例，并重定向至对应的Activity详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(ActivityViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows applications to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = sirs.ApplicationSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/application_form.html',  # 模板文件
        add_serializer_class=firs.AddApplicationSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/applications/add/
        template: sua/sua_form.html
        GET: 返回空Application序列化器，渲染Application创建表单
        POST: 接受Application创建表单数据，创建Application实例，并重定向至对应的Application详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(ApplicationViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class PublicityViewSet(
        viewsets.ReadOnlyModelViewSet,
        mymixins.AddFormMixin,
        mymixins.ChangeFormMixin,
        mymixins.DetailFormMixin,
        mymixins.DeleteFormMixin
        ):
    """
    API endpoint that allows publicities to be viewed or edited.
    """
    queryset = Publicity.objects.all()
    serializer_class = sirs.PublicitySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    delete_success_url = '/'

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/publicity_form.html',  # 模板文件
        add_serializer_class=firs.AddPublicitySerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/publicities/add/
        template: sua/gsua_publicity_form.html
        GET: 返回空Publicity序列化器，渲染Publicity创建表单
        POST: 接受Publicity创建表单数据，创建Publicity实例，并重定向至对应的Publicity详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(PublicityViewSet, self).add(request)

    @detail_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/publicity_form.html',  # 模板文件
        change_serializer_class=firs.AddPublicitySerializer,  # 序列化器
        change_success_url='/',  # 成功后的跳转url
        permission_classes = (IsAdminUser, )
    )
    def change(self, request, *args, **kwargs):
        '''
        url: api/publicities/<int:pk>/change/
        template: sua/gsua_publicity_form.html
        GET: 向模板代码提供pk对应的publicity的序列化器(serializer)，渲染并返回Publicity更新表单
        POST: 接受Publicity更新表单数据，更新Student实例及对应的User实例，并重定向至Publicity实例详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(PublicityViewSet, self).change(request, *args, **kwargs)

    @detail_route(
        methods=['get'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        permission_classes = (IsTheStudentOrIsAdminUser,),
        template_name='sua/publicity_detail.html',  # 模板文件
        detail_serializer_class=firs.AddPublicitySerializer,  # 序列化器
    )
    def detail(self, request, *args, **kwargs):
        '''
        url: api/appeals/<int:pk>/detail/
        template: sua/appeals_detail.html
        GET: 向模板代码提供pk对应的appeals的序列化器(serializer)，渲染并返回Appeals详情页面
        表单字段：表单字段与serializer.data一致
        '''
        return super(PublicityViewSet, self).detail(request, *args, **kwargs)
        

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class AppealViewSet(
        viewsets.ReadOnlyModelViewSet,
        mymixins.AddFormMixin,
        mymixins.ChangeFormMixin,
        mymixins.DetailFormMixin,
        mymixins.DeleteFormMixin
        ):
    """
    API endpoint that allows appeals to be viewed or edited.
    """
    queryset = Appeal.objects.all()
    serializer_class = sirs.AppealSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    delete_success_url = '/'

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/appeal_form.html',  # 模板文件
        add_serializer_class=firs.AddAppealSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/appeals/add/
        template: sua/appeals_form.html
        GET: 返回空Appeal序列化器，渲染Appeal创建表单
        POST: 接受Appeal创建表单数据，创建Appeal实例，并重定向至对应的Appeal详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(AppealViewSet, self).add(request)

    @detail_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/appeal_form.html',  # 模板文件
        change_serializer_class=firs.AddAppealSerializer,  # 序列化器
        change_success_url='/',  # 成功后的跳转url
        permission_classes = (IsAdminUser, )
    )
    def change(self, request, *args, **kwargs):
        '''
        url: api/appeals/<int:pk>/change/
        template: sua/appeal_form.html
        GET: 向模板代码提供pk对应的appeal的序列化器(serializer)，渲染并返回Appeal更新表单
        POST: 接受Appeal更新表单数据，更新Student实例及对应的User实例，并重定向至Appeal实例详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(AppealViewSet, self).change(request, *args, **kwargs)

    @detail_route(
        methods=['get'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        permission_classes = (IsTheStudentOrIsAdminUser,),
        template_name='sua/appeal_detail.html',  # 模板文件
        detail_serializer_class=firs.AddAppealSerializer,  # 序列化器
    )
    def detail(self, request, *args, **kwargs):
        '''
        url: api/appeals/<int:pk>/detail/
        template: sua/appeals_detail.html
        GET: 向模板代码提供pk对应的appeals的序列化器(serializer)，渲染并返回Appeals详情页面
        表单字段：表单字段与serializer.data一致
        '''
        return super(AppealViewSet, self).detail(request, *args, **kwargs)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class ProofViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows proofs to be viewed or edited.
    """
    queryset = Proof.objects.all()
    serializer_class = sirs.ProofSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/sua_form.html',  # 模板文件
        add_serializer_class=firs.AddProofSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/proofs/add/
        template: sua/sua_form.html
        GET: 返回空Proof序列化器，渲染Proof创建表单
        POST: 接受Proof创建表单数据，创建Proof实例，并重定向至对应的Proof详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(ProofViewSet, self).add(request)
    def perform_add(self,serializer):
        serializer.save(owner=self.request.user)