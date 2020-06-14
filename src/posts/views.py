from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Author, Post, PostView, Category, CategoryView
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegisterForm, CommentForm
from django.contrib.auth import authenticate, get_user_model, login, logout
# Create your views here.


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists:
        return qs[0]
    return None

class IndexView(View):
    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        sidebar = Post.objects.order_by('-timestamp')[0:6]
        all_cats = Category.objects.all()[0:6]
        context = {
            'object_list': featured,
            'latest': latest,
            'sidebar': sidebar,
            'all_cats': all_cats
        }
        return render(request, "index.html", context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'single-standard.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        # category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        sidebar = Post.objects.order_by('-timestamp')[0:6]
        all_cats = Category.objects.all()[0:6]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['sidebar'] = sidebar
        context['all_cats'] = all_cats
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))



class ContactView(View):
    def get(self, request, *args, **kwargs):
        sidebar = Post.objects.order_by('-timestamp')[0:6]
        all_cats = Category.objects.all()[0:6]
        context = {
            'sidebar': sidebar,
            'all_cats': all_cats
        }
        return render(request, "page-contact.html", context)

class AboutView(View):
    def get(self, request, *args, **kwargs):
        sidebar = Post.objects.order_by('-timestamp')[0:6]
        all_cats = Category.objects.all()[0:6]
        context = {
            'sidebar': sidebar,
            'all_cats': all_cats
        }
        return render(request, 'page-about.html', context)


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    sidebar = Post.objects.order_by('-timestamp')[0:6]
    all_cats = Category.objects.all()[0:6]
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
        'sidebar': sidebar,
        'all_cats': all_cats
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    sidebar = Post.objects.order_by('-timestamp')[0:6]
    all_cats = Category.objects.all()[0:6]
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
   
    context = {
        'form': form,
        'sidebar': sidebar,
        'all_cats': all_cats
    }
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')

def post_list(request):
    # category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        # 'category_count': category_count,
        # 'form': form
    }
    return render(request, 'blog.html', context)
