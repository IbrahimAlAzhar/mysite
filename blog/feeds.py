from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    # the title,link,description attributes correspond to the RSS elements
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # items method retrives the objects to be included in the field(last 5 published posts)
    def items(self):
        return Post.published.all()[:5]

    # returns item title means post title
    def item_title(self, item):
        return item.title

    # returns item body means post body of first 30 words
    def item_description(self, item):
        return truncatewords(item.body, 30)

