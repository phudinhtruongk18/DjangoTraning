from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from .models import Comment

@login_required(login_url='login')
def delete_comment(request, comment_id):
    url = request.META.get('HTTP_REFERER')
    try:
        comment = Comment.objects.get(id = int(comment_id))
    except Comment.DoesNotExist:
        messages.error(request, "comment does not exist!")
        return redirect(url)

    if comment.user.id == request.user.id:
        comment.delete()
        messages.success(request, "Your review has been deleted!")
        return redirect(url)
    
    messages.error(request, "Delete comment false!")
    return redirect(url)

@login_required(login_url='login')
def submit_comment(request, product_id):
    """For product: Update comment if it exists, otherwise create a new one """
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(user__id=request.user.id, product__id=product_id)
            form = CommentForm(request.POST, instance=comment)
            form.save()
            messages.success(request, "Thanks for the updating review!")
            return redirect(url)
        except Exception as e:
            print(e)
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.content = form.cleaned_data['content']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thanks for the review!")
                return redirect(url)
