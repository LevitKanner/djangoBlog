
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# Create your views here.
# class PostListView(ListView): 
#     queryset = Post.published.all() 
#     context_object_name = 'posts' 
#     paginate_by = 5
#     template_name = 'blog/post/list.html'
    
def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag':tag})
    
    
    
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                              status='published',
                              publish__year=year, 
                              publish__month=month,
                              publish__day=day)
    #list active comments 
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        #a comment was posted
        form = CommentForm(data=request.POST)
        if form.is_valid():
            #create comment object but don't save to database yet.
            new_comment = form.save(commit=False)
            #assign comment to current post
            new_comment.post = post
            #save comment to database
            new_comment.save()
    else:
        form = CommentForm()  
    #List posts with similar tags
    post_tags_ids = post.tags.values_list('id', flat=True) 
    similar_posts = Post.published.filter(tags__in=post_tags_ids) .exclude(id=post.id) 
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]
    
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'form': form,
                                                     'similar_posts': similar_posts})





def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    
    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form is validated
            cd = form.cleaned_data
            #send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read "\
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent })


def post_search(request):
    form = SearchForm()
    query = None
    result = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            
            result = Post.published.annotate(
                search=search_vector,
                rank = SearchRank(search_vector, search_query)
                ).filter(rank__gte=0.3).order_by('-rank')
            
    return render(request, 'blog/post/search.html', {'form': form, 
                                                     'query': query, 
                                                     'result': result
                                                     })