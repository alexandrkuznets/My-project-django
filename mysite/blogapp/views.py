from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
from django.urls import reverse_lazy, reverse

class ArticlesListView(ListView):
    # template_name = 'blogapp/article_list.html'
    # context_object_name = 'articles'
    queryset = Article.objects.filter(published_at__isnull=False).order_by("-published_at")

class ArticlesDetailView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and additions blog articles"
    link = reverse_lazy("articles")

    def items(self):
        return Article.objects.filter(published_at__isnull=False).order_by("-published_at")[:5]

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.body[:200]


