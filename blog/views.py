"""Blog list, detail, and comment views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import BlogCommentForm
from .models import BlogPost, BlogCategory, BlogComment


class BlogListView(ListView):
    """Blog posts with category and type filtering."""

    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True).select_related('author', 'category')
        category_slug = self.request.GET.get('category')
        post_type = self.request.GET.get('type')
        q = self.request.GET.get('q')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['post_types'] = BlogPost.POST_TYPE_CHOICES
        return context


class BlogDetailView(DetailView):
    """Blog post detail with comments."""

    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get_object(self):
        obj = super().get_object()
        BlogPost.objects.filter(pk=obj.pk).update(views_count=obj.views_count + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['comment_form'] = BlogCommentForm()
        context['related_posts'] = BlogPost.objects.filter(
            category=self.object.category, is_published=True
        ).exclude(pk=self.object.pk)[:3]
        return context


@login_required
def add_comment(request, slug):
    """Add a comment to a blog post."""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
    return redirect('blog:detail', slug=slug)
