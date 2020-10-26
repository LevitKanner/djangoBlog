from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


# Create your views here.
class PostListView(ListView): 
    queryset = Post.published.all() 
    context_object_name = 'posts' 
    paginate_by = 5
    template_name = 'blog/post/list.html'
    
   
   
    
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
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'form': form})




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

