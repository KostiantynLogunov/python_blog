from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import News
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    data = {
        'news': News.objects.all(),
        'title': 'Main page of blog'
    }
    # return HttpResponse('<h2>Hello world !</h2>')
    return render(request, 'blog/home.html', data)


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        else:
            return False


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 5

    def get_context_data(self, **kwards):
        ctx = super(ShowNewsView, self).get_context_data(**kwards)
        ctx['title'] = "Blogs main page"
        return ctx


class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author = user).order_by('-date')

    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)
        ctx['title'] = f"All posts from user {self.kwargs.get('username')}"
        return ctx


class NewsDetailView(DetailView):
    # blog/news_detail.html
    model = News
    template_name = 'blog/news_detail.html'
    context_object_name = 'post'    # якщо без цього то в html буде фігурувати object а не post

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        ctx['title'] = News.objects.filter(pk=self.kwargs['pk']).first()
        return ctx


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdateNewsView, self).form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        else:
            return False


class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title', 'text']
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super(CreateNewsView, self).form_valid(form)



def contacts(request):
    # return HttpResponse('<h2>Contacts page</h2>')
    return render(request, 'blog/contacts.html', {'title': 'About as'})
