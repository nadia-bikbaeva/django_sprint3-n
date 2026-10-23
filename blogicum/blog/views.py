from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def get_base_post_queryset(queryset=None):
    if queryset is None:
        queryset = Post.objects.all()
    return queryset.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    post_list = get_base_post_queryset()[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_base_post_queryset(category.posts.all())
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list
    })


def post_detail(request, post_id):
    post = get_object_or_404(get_base_post_queryset(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})
