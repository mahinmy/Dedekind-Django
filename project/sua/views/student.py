from django.utils import timezone
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

from project.sua.models import Publicity
from project.sua.models import Sua
from project.sua.models import Application

from project.sua.serializers import PublicitySerializer
from project.sua.serializers import SuaSerializer,StudentSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import AddAppealSerializer

from .utils.base import BaseView
from .utils.mixins import NavMixin

from .forms.serializers import AddStudentSerializer,AddPublicitySerializer


class IndexView(BaseView, NavMixin):
    template_name = 'sua/index.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(IndexView, self).serialize(request)

        user = request.user

        publicity_set = Publicity.objects.filter(  # 获取在公示期内的所有公示
            is_published=True,
            begin__lte=timezone.now(),
            end__gte=timezone.now()
        )
        publicity_data = PublicitySerializer(  # 序列化公示
            publicity_set,
            many=True,
            context={'request': request}
        )

        application_data = ApplicationSerializer(  # 序列化当前用户的所有申请
            user.applications,
            many=True,
            context={'request': request}
        )

        serialized.update({
            'publicities': publicity_data.data,
            'applications': application_data.data
        })

        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student

            sua_data = SuaSerializer(  # 序列化当前学生的所有公益时记录
                student.suas.filter(is_valid=True),
                many=True,
                context={'request': request}
            )

            appeal_data = AppealSerializer(  # 序列化当前学生的所有申诉
                student.appeals,
                many=True,
                context={'request': request}
            )

            serialized.update({
                'suas': sua_data.data,
                'appeals': appeal_data.data
            })

        return serialized


class TestBaseView(BaseView, NavMixin):  # 例子：这是一个创建学生的View（怕你们踩坑了）
    template_name = 'sua/tmp/test.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(TestBaseView, self).serialize(request)
        serializer = AddStudentSerializer()
        serialized.update({
            'serializer': serializer,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        serializer = AddStudentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            self.url = serializer.data['url']
            return True
        else:
            return False
            
            
class AppealView(BaseView,NavMixin):
    template_name = 'sua/appeal.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        publicity_id = kwargs['pk']
        publicity = AddPublicitySerializer(Publicity.objects.get(id=publicity_id),context={'request':request})
        serialized = super(AppealView, self).serialize(request)
        serializer = AddAppealSerializer(context={'request':request})
        serialized.update({
            'serializer': serializer,
            'publicity':publicity.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        assert hasattr(user,'student') # 判断当前用户是否为学生
        student = user.student
        
        publicity_id = kwargs['pk']
        serializer = AddAppealSerializer(data=request.data, context={'request': request,})
        if serializer.is_valid():

            serializer.save(publicity=Publicity.objects.get(id=publicity_id),owner=user,student=student)
            self.url = serializer.data['url']
            return True
        else:
            return False 
            
       
class SuasExportView(BaseView,NavMixin):
    template_name = 'sua/suas_export.html'
    components = {
        'nav': 'nav',
    }
        
        
    def serialize(self, request, *args, **kwargs):
        serialized = super(SuasExportView, self).serialize(request)

        user = request.user
    
        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student
            
            sua_data = SuaSerializer(# 序列化当前学生的所有公益时记录
                student.suas.filter(is_valid=True),
                many=True,
                context={'request': request}
            )
        
        serialized.update({
            'suas': sua_data.data,
            'name':student.name,
            'number':student.number,
            'hour':student.suahours,
            })
            

        return serialized
#        filename = 'project/media/suasexport/file.pdf'


def Download(request):
    
    user = request.user
    
    student = user.student
    Filename = str(student.name)
   
    sua_data = SuaSerializer(# 序列化当前学生的所有公益时记录
        student.suas.filter(is_valid=True),
        many=True,
        context={'request': request}
    )
        
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="公益时记录"'

    buffer = BytesIO()
    bianju = 40
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 22) 
    p.drawString(bianju,780,"The suas'record",)
    p.drawImage('project/sua/static/sua/images/logo-icon.png',460,705,width=90,height=90)
    p.setFont("Helvetica", 15) 
    p.drawString(bianju,750,'Number:'+str(user))
    p.drawString(bianju,720,'Total suahours:'+str(student.suahours)+'h')
    
    location = 650
    p.drawString(bianju,670,"Title")
    for sua in sua_data.data:
        p.drawString(bianju,location,str(sua['activity']['title']))
        location -= 50
    
    location = 650
    p.drawString(bianju+200,670,"Group")
    for sua in sua_data.data:
        p.drawString(bianju+200,location,str(sua['activity']['group']))
        location -= 50
    
    location = 650
    p.drawString(bianju+400,670,"Suahours")
    for sua in sua_data.data:
        p.drawString(bianju+400,location,str(sua['suahours'])+'h')
        location -= 50

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
        

        

        