from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.db.models import Count


def post_list(request, tag_slug=None): # tag_slug is come from url,
    object_list = Post.published.all() # take all posts,pulished is custom user and objects is build in user
    tag = None

    if tag_slug: # if tag_slug is not none which is come from url
        # here Tag is django build in
        tag = get_object_or_404(Tag, slug=tag_slug) # we get the tag object with the given slug using the get_obj_or_404 shortcut,here slug is tag_slug which use in url
        object_list = object_list.filter(tags__in=[tag]) # for retrieving all posts of this tag

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')  # take the current page number
    try:
        posts = paginator.page(page)  # take the all posts in current page
    except PageNotAnInteger:
        # If page is not an integer deliver the posts of first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the posts of last page
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, # take the year,month,day values using get method and pass it through function's parameter,take the slugfield of post object in Post class
                             status='published', # use custom user in place of object user(build in)
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted,then take the comment form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # new_comment is the instance of commentForm which using Comment model,after posting a new comment then take the comment on post attribute
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm() # in get method,show a empty form

    # List of similar posts
    # retrieve a python list of id's for the tags of the current post
    post_tags_ids = post.tags.values_list('id', flat=True) # take the all tags of current post,post is current post and tags is form of taggable manager(taggit) which defines all tags of this post
    # get all posts that contain any of these tags,excluding the current post itself
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
                                   .exclude(id=post.id)
    # here count 4 and order the result by the number of shared tags then publish(recent)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4] # if some post has same tag then here choose the recent one
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            # subject is pass to receiver,and receiver see like "azhar,ibra@ recommends you reading Covid 19 article
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            # message shows in receiver like "read Covid19 at Imp of covid 19 comments: "
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'ibrahimalazhar264@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm() # in case of get method
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
