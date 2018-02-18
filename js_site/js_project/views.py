from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UploadForm, UserForm, ProfileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views import View
from .models import Photo, Comment
from django.contrib import messages
from django.views.generic.base import TemplateView

# Create your views here.

@login_required
def index(request):
    photo_list = Photo.objects.filter(is_public=True)[:20]
    paginator = Paginator(photo_list, 6)
    page = request.GET.get('page')
    user = get_object_or_404(User, username=request.user.username)
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render(request, 'js_project/index.html', {'photos': photos, 'user': user})

@login_required
def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            form.save()

            messages.success(request, '프로젝트 등록!')
            return redirect('js_project:index')
    else:
        form = UploadForm()
    return render(request, 'js_project/upload.html', {'form': form})


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    photo_list = user.photo_set.filter(is_public=False)[:20]
    paginator = Paginator(photo_list, 6)
    page = request.GET.get('page')

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    context = {"user": user, "photos": photos}
    return render(request, 'js_project/profile.html', context)


class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

        if hasattr(user, 'profile'):
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname': profile.nickname,
                'profile_photo': profile.profile_photo,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'js_project/profile_update.html',
                      {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        pk = request.user.pk
        u = User.objects.get(id=pk)
        user_form = UserForm(request.POST, instance=u)
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES,
                                       instance=profile)
        else:
            profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = u
            profile.save()

        return redirect('js_project:profile', pk)



@login_required
def content(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    context = {"photo": photo}
    return render(request, 'js_project/content.html', context)

@login_required
def comment_new(request, pk):
    # 요청 메서드가 POST방식 일 때만 처리
    if request.method == 'POST':
        # Post인스턴스를 가져오거나 404 Response를 돌려줌
        photo = get_object_or_404(Photo, pk=pk)
        # request.POST데이터를 이용한 Bounded Form 생성
        comment_form = CommentForm(request.POST)
        # 올바른 데이터가 Form인스턴스에 바인딩 되어있는지 유효성 검사
        if comment_form.is_valid():
            # 유효성 검사에 통과하면 Comment객체 생성 및 DB저장
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 등록되었습니다')
        else:
            error_msg = '댓글 등록에 실패했습니다\n{}'.format(
                '\n'.join(
                    [f'- {error}'
                     for key, value in comment_form.errors.items()
                     for error in value]
                )
            )
            messages.error(request, error_msg)
        # 정상적으로 Comment가 생성된 후
        # 'post'네임스페이스를 가진 url의 'post_list'이름에 해당하는 뷰로 이동
        return redirect('js_project:content', pk)

@login_required
def delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.owner == User.objects.get(username = request.user.get_username()):
        photo.delete()
        return redirect('js_project:index')


def about(request):
    return render(request, 'js_project/about.html')

def first_project(request):
    return render(request, 'js_project/first.html')

def second_project(request):
    return render(request, 'js_project/second.html')

def second_report(request):
    return render(request, 'js_project/second_report.html')

def second_media(request):
    return render(request, 'js_project/second_video.html')

def first_report(request):
    return render(request, 'js_project/first_report.html')

def first_video(request):
    return render(request, 'js_project/first_video.html')

def first_ppt(request):
    return render(request, 'js_project/first_ppt.html')


