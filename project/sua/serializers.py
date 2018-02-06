from django.contrib.auth.models import User, Group
from project.sua.models import Student, SuaGroup, Sua, Application, Activity, Publicity, Appeal, Proof

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('url', 'student', 'username', 'is_staff', 'password', 'groups', 'applications', )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'suagroup', 'name', 'user_set')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('url', 'user', 'name', 'number', 'suahours', 'grade', 'classtype', 'phone', 'suas', 'appeals')


class SuaGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuaGroup
        fields = ('url', 'group', 'name', 'is_staff', 'contact', 'rank')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities')


class SuaSerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = Sua
        fields = ('url', 'student', 'activity', 'team', 'suahours', 'application', 'is_valid')


class StudentNameNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('name', 'number')


class SuaOnlySerializer(serializers.ModelSerializer):
    student = StudentNameNumberSerializer()
    class Meta:
        model = Sua
        fields = ('student', 'team', 'suahours')


class ActivityWithSuaSerializer(serializers.ModelSerializer):
    suas = SuaOnlySerializer(many=True)

    class Meta:
        model = Activity
        fields = ('title', 'date', 'detail', 'group', 'suas')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    sua = SuaSerializer()

    class Meta:
        model = Application
        fields = ('url', 'created', 'contact', 'sua', 'proof', 'is_checked', 'status', 'feedback')


class PublicitySerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivityWithSuaSerializer()

    class Meta:
        model = Publicity
        fields = ('url', 'activity', 'title', 'content', 'contact', 'is_published', 'begin', 'end', 'appeals')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    publicity = PublicitySerializer()

    class Meta:
        model = Appeal
        fields = ('url', 'created', 'student', 'publicity', 'content', 'is_checked', 'status', 'feedback')


class ProofSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file', 'applications')
