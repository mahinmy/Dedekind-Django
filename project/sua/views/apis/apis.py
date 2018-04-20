from rest_framework import viewsets
from project.sua.permissions import IsAdminUserOrReadOnly

from django.contrib.auth.models import User

from project.sua.models import Student,Proof,Sua,Activity,Publicity,Application,Appeal

from project.sua.views.apis.serializer import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class PublicityViewSet(viewsets.ModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer

class SuaViewSet(viewsets.ModelViewSet):
    queryset = Sua.objects.all()
    serializer_class = SuaSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer

class ProofViewSet(viewsets.ModelViewSet):
    queryset = Proof.objects.all()
    serializer_class = ProofSerializer
