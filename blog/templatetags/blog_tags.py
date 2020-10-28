from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

#Name of tag can be specified such as @register. simple_tag(name='my_tag')
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def most_commented(count=5):
    return Post.published\
        .annotate(total_comments=Count('comments'))\
            .order_by('-total_comments')[:count]