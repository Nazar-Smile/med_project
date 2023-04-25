from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from apps.blog.models import Post
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView
)

from apps.blog.models import Category


class PostListView(ListView):
    template_name = "apps.blog.post_list.html"
    model = Post
    queryset = Post.objects.filter(is_draft=False).order_by('-id')
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:4]

        context["categories"] = Category.objects.all()

        return context

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            qs = Post.objects.filter(is_draft=False, category__slug=category_slug)
            return qs
        return Post.objects.filter(is_draft=False)


class PostDetailView(DetailView):
    template_name = "post_detail.html"
    model = Post
    # pk=id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:4]

        context["categories"] = Category.objects.all()
        # context["comment_form"] = CommentCreateForm()

        return context

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            qs = Post.objects.filter(is_draft=False, category__slug=category_slug)
            return qs
        return Post.objects.filter(is_draft=False)


def my_view(request):
    items = Post.objects.all()
    paginator = Paginator(items, 10)  # 10 items per page
    page = request.GET.get('page')
    items_on_page = paginator.get_page(page)
    return render(request, 'apps.blog.post_list.html', {'items': items_on_page})


class Search(ListView):
    """Поиск"""
    # template_name = 'index.html'
    # context_object_name = 'films'
    # paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get("q")).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context