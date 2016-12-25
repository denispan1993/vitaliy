# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

__author__ = 'AlexStarov'


@staff_member_required
def admin_panel(request,
                template_name=u'admin_panel.html', ):
    return render(request=request,
                  template_name=template_name,
                  content_type='text/html', )


@staff_member_required
def comment_search(request,
                   template_name=u'comment/comment_search.jinja2', ):
    error_message = u''
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'comment_search':
            comment_id = request.POST.get(u'comment_id', None, )
            if comment_id:
                try:
                    comment_id = int(comment_id, )
                except ValueError:
                    error_message = u'Некорректно введен номер Комментария.'
                else:
                    from apps.comment.models import Comment
                    try:
                        comment = Comment.objects.get(pk=comment_id, )
                    except Comment.DoesNotExist:
                        error_message = u'Комментария с таким номером не существует.'
                    else:
                        comment_id = '%06d' % comment_id
                        from django.shortcuts import redirect
                        return redirect(to='comment_edit', id=comment_id, )
    from apps.comment.models import Comment
    comments = Comment.objects.all()
    return render(request=request,
                  template_name=template_name,
                  context={'error_message': error_message,
                           'comments': comments, },
                  content_type='text/html', )


@staff_member_required
def comment_edit(request,
                 id,
                 template_name=u'comment/comment_edit.jinja2', ):
    error_message = u''
    from apps.comment.models import Comment
    from django.shortcuts import redirect
    if id:
        try:
            comment_id = int(id, )
        except ValueError:
            error_message = u'Некорректный номер комментария.'
        else:
            try:
                comment = Comment.objects.get(pk=comment_id, )
            except Comment.DoesNotExist:
                error_message = u'В базе отсутсвует комментарий с таким номером.'
            else:
                error_message = u'Отсутсвует номер комментария.'
    if not 'comment_id' in locals() and not 'comment_id' in globals()\
            or not 'comment' in locals() and not 'comment' in globals():
        return redirect(to='comment_search', )
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'comment_dispatch':
            comment_id = request.POST.get(u'comment_id', None, )
            if comment_id:
                try:
                    id = int(comment_id, )
                except ValueError:
                    error_message = u'Некорректный номер комментария. № 2'
    return render(request=request,
                  template_name=template_name,
                  context={'comment_id': comment_id,
                           'comment': comment, },
                  content_type='text/html', )
