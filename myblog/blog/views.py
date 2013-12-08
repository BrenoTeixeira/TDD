from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post


class HomeView(ListView):

	template_name = 'index.html'
	queryset = Post.objects.order_by('-created_at')

home = HomeView.as_view()


class PostDetails(DetailView):
	model = Post

post_details = PostDetails.as_view()
