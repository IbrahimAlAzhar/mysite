from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap): # use multiple sites using a single Django project
    changefreq = 'weekly' # changefreq of my post pages
    priority = 0.9

    def items(self): # items method returns the queryset of objects to include in this sitemap, by default django use get absoulate url
        return Post.published.all()

    def lastmod(self, obj): # the lastmod method receives each object returned by items() and returns the last time object was modified
        return obj.updated
