from .base import BaseViewSet

from rest_framework.permissions import IsAdminUser
from project.sua.views.utils.mixins import NavMixin
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly,IsAdminUserOrActivity
from project.sua.models import Student
import project.sua.views.form.serializers as firs


class StudentViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddStudentSerializer
    queryset = Student.objects.filter(deletedAt=None)
    filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/student_form.html']
        elif self.action == 'detail':
            return ['sua/student_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change']:
            return firs.AddStudentSerializer
        elif self.action == 'detail':
            return firs.detailofstudentSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['add', 'change']:
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]