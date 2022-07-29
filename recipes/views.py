from multiprocessing import context
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm
from django.views.generic import CreateView, DeleteView, UpdateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model

user=get_user_model()

class PostList(generic.ListView):
    model = Post
    template_name = "index.html"
    paginate_by = 6

    def get_queryset(self):
        search=self.request.GET.get("search") if self.request.GET.get("search") != None else ''
        chef=self.request.GET.get("chef") if self.request.GET.get("chef") != None else ''
        all_obj=Post.objects.filter(title__icontains=search,author__username__icontains=chef).order_by("-created_on")
        return all_obj

    def get_context_data(self, **kwargs):
        search=self.request.GET.get("search") if self.request.GET.get("search") != None else ''
        chef=self.request.GET.get("chef") if self.request.GET.get("chef") != None else ''
        all_user=user.objects.all()
        kwargs["search"]=search
        kwargs["chef"]=chef
        kwargs["all_user"]=all_user
        return super().get_context_data(**kwargs)


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": comment_form,
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

class CreatePost(LoginRequiredMixin, CreateView):

    fields = ["title","content", "featured_image", "excerpt", "status", "prep_time", "cook_time", "servings"]
    model = Post
    template_name = "recipes/postcreate.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, DeleteView):

    model = Post
    success_url = reverse_lazy("home")
    template_name = "recipes/postdelete.html"

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

class Updatepost(LoginRequiredMixin, UpdateView):
    model = Post
    success_url = reverse_lazy("home")
    fields = ["title", "content", "featured_image", "excerpt", "status", "prep_time", "cook_time", "servings"]
    template_name = "recipes/postupdate.html"

class filterpost(LoginRequiredMixin,ListView):
    model = Post
    template_name = "index.html"
    paginate_by = 6

    def get_queryset(self):
        search=self.request.GET.get("search") if self.request.GET.get("search") != None else ''
        print(search)
        all_obj=Post.objects.filter(title__icontains=search).order_by("-created_on")
        return all_obj


