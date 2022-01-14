from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm
from .models import Board
from user.models import User
from user.decorators import login_required
from datetime import date, datetime, timedelta
from .pagination import pagination


# Create your views here.


def board_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    page = pagination(request, Board)
    context.update(page)

    return render(request, 'board/board_list.html', context)


@login_required
def board_write(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    if request.method == 'GET':
        write_form = BoardWriteForm()
        context['forms'] = write_form
        return render(request, 'board/board_write.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id=login_session)
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
                board_name=write_form.board_name
            )
            board.save()
            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
                return render(request, 'board/board_write.html', context)


def board_detail(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(Board, id=pk)
    context['board'] = board
    context['page'] = request.GET['page']

    if board.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    response = render(request, 'board/board_detail.html', context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard', '_')

    if f'_{pk}_' not in cookie_value:
        cookie_value += f'{pk}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        board.hits += 1
        board.save()
    return response



def board_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(Board, id=pk)
    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board')
    else:
        return redirect(f'/board/detail/{pk}/')

@login_required
def board_modify(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    if board.writer.user_id != login_session:
        return redirect(f'/board/detail/{pk}/')

    if request.method == 'GET':
        write_form = BoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board/board_modify.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():

            board.title=write_form.title
            board.contents=write_form.contents
            board.board_name=write_form.board_name

            board.save()
            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
                return render(request, 'board/board_modify.html', context)
