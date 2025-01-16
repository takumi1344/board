from django.shortcuts import get_object_or_404, render, redirect
from .forms import BoardForm, SignUpForm, CommentForm
from .models import Board, Comment
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from functools import wraps

# Create your views here.
def user_owns_board(view_func):
    @wraps(view_func)
    def wrapper(request, pk):
        board = get_object_or_404(Board, pk=pk)
        if board.user == request.user:
            return view_func(request, pk)
        else:
            return redirect('index')
    return wrapper


def index(request):
    boards = Board.objects.all().order_by('-updated_at')
    return render(request, 'index.html', {'boards':boards})

@login_required
def new(request):
    form = BoardForm()
    return render(request, 'new.html', {'form':form})

@login_required
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
    else:
        form = BoardForm()
    return render(request, 'new.html', {'form':form})


@login_required
def show(request, pk):
    board = Board.objects.get(pk=pk)
    comments = Comment.objects.filter(board=pk).order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'show.html', {'board':board, 'comments':comments, 'comment_form':comment_form})

@login_required
@user_owns_board
def edit(request, pk):
    board = Board.objects.get(pk=pk)
    form = BoardForm(instance=board)
    return render(request, 'edit.html', {'form':form, 'board':board})

@login_required
@user_owns_board
def update(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('show', pk=pk)
    else:
        form = BoardForm(instance=board)
    return render(request, 'edit.html', {'form':form, 'board':board})

@login_required
@user_owns_board
def delete(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        board.delete()
        return redirect('index')
    return redirect('index')

@login_required
def my_boards(request):
    user = request.user
    boards = user.boards.all()
    return render(request, 'my_boards.html', {'boards':boards})


@login_required
def comment_create(request, pk):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.board_id = pk
            comment_form.save()
    return redirect('show', pk=pk)

@login_required
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('show', pk=board_pk)



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user':user})
