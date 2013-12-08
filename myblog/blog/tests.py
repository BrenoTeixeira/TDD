from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from .models import Post, Comment


class PostModelTest(TestCase):

    def test_unicode_representation(self):
        post = Post(title=u'My post title')
        self.assertEqual(unicode(post), post.title)

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username='some_user')
        post = Post.objects.create(title="My post title", author=user)
        self.assertIsNotNone(post.get_absolute_url())    


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ListPostsOnHomePage(TestCase):
    """
    Test whether our blog posts show up on the homepage.
    """

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')

    def test_one_post(self):
        Post.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_posts(self):
        Post.objects.create(title='1-title', body='1-body', author=self.user)
        Post.objects.create(title='2-title', body='2-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-title')

    def test_no_post(self):
        response = self.client.get('/')
        self.assertContains(response, 'No blog post entries yet.')


class BlogPostViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")
        self.post = Post.objects.create(title='1-title', body='1-body', author=self.user)

    def test_basic_view(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_blog_title_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.title)

    def test_blog_body_in_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.body)

class CommentModelTest(TestCase):

    def test_unicode_representation(self):
        comment = Comment(body=u'My comment body')
        self.assertEqual(unicode(comment), u'My comment body')

class ListCommentsOnDetailPage(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")
        self.post = Post.objects.create(title='1-title', body='1-body', author=self.user)
        self.comm = Comment.objects.create(post_id=1, name='1-comment', body='1-body')
        self.resp = self.client.get('/post/%s/' % self.post.pk)
        
    def test_get(self):
        """
        GET /post/1/ should return status 200.
        """
        self.assertEqual(200, self.resp.status_code)

    def test_comment_post(self):
        self.assertContains(self.resp, '1-comment')
