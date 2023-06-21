from django.urls import reverse_lazy

from django.urls import reverse

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, MyModel

from datetime import datetime
from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

# импортируем функцию для перевода

from django.utils.translation import gettext as _

# from django.http import HttpResponse

from django.http.response import HttpResponse

from django.views.generic import View


from django.utils.translation import gettext as _

# from django.utils.translation import activate, get_supported_language_variant, LANGUAGE_SESSION_KEY

from django.views import View

from django.utils import timezone
from django.shortcuts import redirect
 
#  импортируем стандартный модуль для работы с часовыми поясами
import pytz



# Create your views here.
 
# class Index(View):
#     def get(self, request):
#         string = _('Hello world') 
   
#         return HttpResponse(string)


# ========== 1 ===========

# class Index(View):
#     def get(self, request):
#         string = _('')
   
#         context = {
#             'string': string
#         }

#         return HttpResponse(render(request, 'default.html', context))


# =========== 2 ===========

 
# Create your views here.
class Index(View):
    def get(self, request):

        curent_time = timezone.now()

        #. Translators: This message appears on the home page only
        models = MyModel.objects.all()
 
        context = {
            'models': models,

            'current_time': timezone.now(),

            #  добавляем в контекст все доступные часовые пояса
            'timezones': pytz.common_timezones
        }
 
        return HttpResponse(render(request, 'default.html', context))

    
    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')



class NewsList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'news.html'
    context_object_name = 'news'

    paginate_by = 7


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset

        pprint(context)
        return context

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = ('main.add_post')


    def form_valid(self, form):
        news = form.save(commit=False)
        news._type = 'NE'
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('main.add_post')


    def form_valid(self, form):
        article = form.save(commit=False)
        article._type = 'AR'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = ('main.change_post')



class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('main.change_post')



class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('main.delete_post')


class SearchList(ListView):
    model = Post
    template_name = 'search_page.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context



class CategoriesList(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'categories.html'
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'one_category.html'
    context_object_name = 'one_category'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['cat'] = category
        context['subscribers'] = category.subscribers.all()
        return context


def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)

    return HttpResponseRedirect(reverse('categories'))


def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)

    return HttpResponseRedirect(reverse('categories'))