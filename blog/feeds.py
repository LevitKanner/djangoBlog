from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostFeed(Feed):
    title = "Levitate"
    link = reverse_lazy('blog:post_list')
    description = "New posts on Levitate."
    
    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item: Post) -> str:
        return item.title
    
    def item_description(self, item: Post) -> str:
        return truncatewords(item.body,20)