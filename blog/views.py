from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3) #!0 pages to be displayed on each page
    page = request.GET.get('page')
    try:
        ob_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        ob_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        ob_list = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {'page': page, 'posts': ob_list})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                              status='published',
                               publish__year=year, 
                               publish__month=month,
                                publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})