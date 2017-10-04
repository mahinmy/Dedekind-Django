from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import LoginForm, SuaForm, Sua_ApplicationForm, ProofForm, AppealForm
from .models import Proof, Sua_Application, GSuaPublicity, GSua


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['user_password']
            loginstatus = form.cleaned_data['loginstatus']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if(loginstatus):
                    request.session.set_expiry(15 * 24 * 3600)
                else:
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login')
    else:
        form = LoginForm()
    return render(request, 'sua/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def index(request):
    usr = request.user
    sua_list = []  # 公益时记录
    sa_list = []  # 公益时申请
    appeals_list = []  # 申诉记录
    gsap_list = []  # 活动记录
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
        i = 0
        for sua in stu.sua_set.filter(is_valid=True).order_by('-date'):
            i += 1
            sua_list.append((i, sua))
        i = 0
        for sua in stu.sua_set.order_by('-sua_application__date'):
            if hasattr(sua, 'sua_application'):
                i += 1
                sa_list.append((i, sua.sua_application))
        # 获取申诉列表
        i = 0
        for appeal in stu.appeal_set.order_by('-date'):
            i += 1
            appeals_list.append((i, appeal))

    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
        suahours = '-.-'
    # 组织公益时活动的公示
    gsaps = GSuaPublicity.objects.filter(
        is_published=True,
        published_begin_date__lte=timezone.now(),
        published_end_date__gt=timezone.now()
    )
    for gsap in gsaps:
        teams = dict()
        suass = gsap.gsua.suas.order_by('team', 'suahours', 'student__name')
        i = 0
        for sua in suass:
            i += 1
            if sua.team not in teams:
                teams[sua.team] = dict()
            if sua.suahours not in teams[sua.team]:
                teams[sua.team][sua.suahours] = []
            teams[sua.team][sua.suahours].append(sua.student.name)
        gsap_list.append((gsap, teams))
    return render(request, 'sua/index.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'sua_list': sua_list,
        'sa_list': sa_list,
        'ap_list': appeals_list,
        'gsap_list': gsap_list,
    })


@login_required
def apply_sua(request):
    usr = request.user
    stu = None
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
    date = timezone.now()
    year = date.year
    month = date.month
    if month < 9:
        year_before = year - 1
        year_after = year
    else:
        year_before = year
        year_after = year + 1

    # 表单处理
    if request.method == 'POST':
        suaForm = SuaForm(request.POST, prefix='suaForm')
        proofForm = ProofForm(request.POST, request.FILES, prefix='proofForm')
        sua_ApplicationForm = Sua_ApplicationForm(
            request.POST,
            prefix='sua_ApplicationForm',
        )
        if suaForm.is_valid() and\
                proofForm.is_valid() and\
                sua_ApplicationForm.is_valid() and\
                stu is not None:
            # 生成Models
            if proofForm.cleaned_data['is_offline']:
                offlineProofSet = Proof.objects.filter(is_offline=True)
                if offlineProofSet.count == 0:
                    assert(User.objects.filter(is_superuser=True).count != 0)
                    proof = Proof.objects.create(
                        user=User.objects.filter(is_superuser=True)[0],
                        date=date,
                        is_offline=True,
                    )
                    proof.save()
                else:
                    proof = offlineProofSet[0]
            else:
                proof = proofForm.save(commit=False)
            sua = suaForm.save(commit=False)
            sua_Application = sua_ApplicationForm.save(commit=False)
            # 处理proof
            if not proofForm.cleaned_data['is_offline']:
                proof.user = usr
                proof.date = date
                proof.save()
            # 处理sua
            sua.student = stu
            sua.last_time_suahours = 0.0
            sua.is_valid = False
            sua.save()
            # 处理sua_Application
            sua_Application.sua = sua
            sua_Application.date = date
            sua_Application.proof = proof
            sua_Application.is_checked = False
            sua_Application.save()
            return HttpResponseRedirect('/')
    else:
        suaForm = SuaForm(prefix='suaForm')
        proofForm = ProofForm(prefix='proofForm')
        sua_ApplicationForm = Sua_ApplicationForm(
            prefix='sua_ApplicationForm',
        )

    return render(request, 'sua/apply_sua.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'apply_date': date.date(),
        'apply_year_before': year_before,
        'apply_year_after': year_after,
        'proofForm': proofForm,
        'suaForm': suaForm,
        'sua_ApplicationForm': sua_ApplicationForm,
    })


@login_required
def appeal_for(request):
    usr = request.user
    stu = None
    gsuap = GSuaPublicity.objects.get(pk=int(request.GET.get('gsuap_id')))
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
    date = timezone.now()
    year = date.year
    month = date.month
    if month < 9:
        year_before = year - 1
        year_after = year
    else:
        year_before = year
        year_after = year + 1
    # 表单处理
    if request.method == 'POST':
        print(gsuap)
        appealForm = AppealForm(request.POST, prefix='appealForm')
        if appealForm.is_valid() and\
                stu is not None and\
                gsuap is not None:
            if date <= gsuap.published_end_date:
                # 生成Models
                appeal = appealForm.save(commit=False)
                # 处理appeal
                appeal.student = stu
                appeal.date = date
                appeal.gsua = gsuap.gsua
                appeal.is_checked = False
                appeal.feedback = ''
                appeal.save()
                return HttpResponseRedirect('/')
    else:
        print(gsuap)
        appealForm = AppealForm(prefix='appealForm')
    return render(request, 'sua/appeal_for.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'appealYearBefore': year_before,
        'appealYearAfter': year_after,
        'appealDate': date.date(),
        'appealForm': appealForm,
        'gsuap': gsuap,
    })


class ApplicationDetailView(generic.DetailView):
    model = Sua_Application
    template_name = 'sua/application_detail.html'
    context_object_name = 'sa'

    def get_queryset(self):
        user = self.request.user
        return Sua_Application.objects.filter(
            sua__student__user=user
        )

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        sa = self.get_object()
        usr = self.request.user
        stu = None
        suahours = 0
        if hasattr(usr, 'student'):
            stu = usr.student
            name = stu.name
            number = stu.number
            suahours = stu.suahours
        else:
            if usr.is_staff:
                name = 'Admin.' + usr.username
            else:
                name = 'NoStuInfo.' + usr.username
            number = '------'
        year = sa.date.year
        month = sa.date.month
        if month < 9:
            year_before = year - 1
            year_after = year
        else:
            year_before = year
            year_after = year + 1
        print(context)
        context['year_before'] = year_before
        context['year_after'] = year_after
        context['stu_name'] = name
        context['stu_number'] = number
        context['stu_suahours'] = suahours
        return context


@login_required
def adminIndex(request):
    usr = request.user
    sua_list = []  # 公益时记录
    sa_list = []  # 公益时申请
    appeals_list = []  # 申诉记录
    gsap_list = []  # 活动记录
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
        i = 0
        for sua in stu.sua_set.filter(is_valid=True).order_by('-date'):
            i += 1
            sua_list.append((i, sua))
        i = 0
        for sua in stu.sua_set.order_by('-sua_application__date'):
            if hasattr(sua, 'sua_application'):
                i += 1
                sa_list.append((i, sua.sua_application))
        # 获取申诉列表
        i = 0
        for appeal in stu.appeal_set.order_by('-date'):
            i += 1
            appeals_list.append((i, appeal))

    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
        suahours = '-.-'
    # 组织公益时活动的公示
    gsaps = GSuaPublicity.objects.filter(
        is_published=True,
        published_begin_date__lte=timezone.now(),
        published_end_date__gt=timezone.now()
    )
    for gsap in gsaps:
        teams = dict()
        suass = gsap.gsua.suas.order_by('team', 'suahours', 'student__name')
        i = 0
        for sua in suass:
            i += 1
            if sua.team not in teams:
                teams[sua.team] = dict()
            if sua.suahours not in teams[sua.team]:
                teams[sua.team][sua.suahours] = []
            teams[sua.team][sua.suahours].append(sua.student.name)
        gsap_list.append((gsap, teams))
    return render(request, 'sua/admin_index.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'sua_list': sua_list,
        'sa_list': sa_list,
        'ap_list': appeals_list,
        'gsap_list': gsap_list,
    })