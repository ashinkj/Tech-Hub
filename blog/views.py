from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Comment
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import CommentForm


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))

def search_user(request):
    searched = request.GET.get('searched')
    if searched and searched.strip():
        post = Post.objects.filter(author__username__icontains=searched).first()
        
        if post:
            return redirect(reverse('user-posts', kwargs={'username': post.author.username}))
    return render(request, 'blog/search_user.html', {'searched': searched})

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
     
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post

class CommentCreateView(ListView):
    model = Post
    template_name = 'blog/add_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Add the CommentForm to the context
        return context

    def post(self, request, *args, **kwargs):
        post_id = kwargs['pk']  # Get the post ID from the URL parameters
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.user = request.user
            comment.save()
            return redirect('post-detail', pk=post_id)

        # If the form is not valid, re-render the page with the form errors
        return render(request, self.template_name, {'form': form})

  

# def user_comment(request, *args, **kwargs):
#         post = get_object_or_404(Post, pk=kwargs['pk'])  # Fetch the specific post using pk from kwargs
#         comments = Comment.objects.filter(post=post).order_by('-date')

#         if request.method == 'POST':
#             form = CommentForm(request.POST, request.FILES)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.user = request.user
#                 comment.post = post
#                 comment.save()
#                 return HttpResponseRedirect(reverse('post_list.html'))

#         else:
#             form = CommentForm()

#         context = {
#             'form': form,
#             'post': post,
#             'comments': comments  
#         }

#         return render(request, 'post_list.html', context)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
