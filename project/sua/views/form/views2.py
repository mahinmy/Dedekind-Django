from .base import BaseViewSet

from rest_framework.permissions import IsAdminUser
from project.sua.views.utils.mixins import NavMixin
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly,IsAdminUserOrActivity
from project.sua.models import Student, Sua, Activity, Application, Publicity, Appeal, Proof
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

class SuaViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddSuaSerializer
    queryset = Sua.objects.filter(deletedAt=None)
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/sua_form.html']
        elif self.action == 'detail':
            return ['sua/sua_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddSuaSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes == (IsTheStudentOrIsAdminUser,)
        else:
            permission_classes = (IsAdminUserOrReadOnly,)

        return [permission() for permission in permission_classes]

class ActivityViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddActivitySerializer
    queryset = Activity.objects.filter(deletedAt=None)
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/activity_form.html']
        elif self.action == 'detail':
            return ['sua/activity_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddActivitySerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['add', 'change', 'detail']:
            permission_classes = (IsAdminUserOrActivity,)
        else:
            permission_classes = (IsAdminUserOrActivity, )

        return [permission() for permission in permission_classes]

class ApplicationViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddApplicationSerializer
    queryset = Application.objects.filter(deletedAt=None)
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/application_form.html']
        elif self.action == 'detail':
            return ['sua/application_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddApplicationSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser,)
        else:
            permission_classes = (IsAdminUserOrReadOnly,)

        return [permission() for permission in permission_classes]

class PublicityViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddPublicitySerializer
    queryset = Publicity.objects.filter(deletedAt=None)
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/publicity_form.html']
        elif self.action == 'detail':
            return ['sua/publicity_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddPublicitySerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser,)
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]

class AppealViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddAppealSerializer
    queryset = Appeal.objects.filter(deletedAt=None)
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/appeal_form.html']
        elif self.action == 'detail':
            return ['sua/appeal_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddAppealSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]

class ProofViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddProofSerializer
    queryset = Proof.objects.filter(deletedAt=None)
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/sua_form.html']
        elif self.action == 'detail':
            return ['sua/proof_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddProofSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser,)
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]
