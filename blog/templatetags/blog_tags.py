from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

# created a simple template tag that returns the number of posts
# this variable is instance of the template library
register = template.Library()
# register the function as a simple tag
@register.simple_tag
# django use the function's name as a tag name
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
# here counts occurs the maximum no of posts shows
def show_latest_posts(count=5):
    # here latest_posts holds the posts in descending order
    latest_posts = Post.published.order_by('-publish')[:count]
    # here applying latest_posts html file
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    # using annotate function to aggregate the total number of comments for each post
    # use the count aggregation to store the number of comments in the computed field total_comments
    # and total comments displays descending order up to 5
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]

# django escapes the html code generate by filters,use mark_safe function provided by django to mark the
# result as safe HTML to be rendered in the template, Django will not trust any HTML code
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
# allows to create exceptions for returning safe HTML (converting text to HTML)
