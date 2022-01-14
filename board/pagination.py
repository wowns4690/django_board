from django.core.paginator import Paginator


# Board : 가져올 게시글들
# contents_num : 한 페이지에 표시할 게시글 개수
# 표시할 페이지 수 : 7개
def pagination(request, Board, contents_num=5) -> dict:
    # 객체 역순으로 불러오기
    all_boards = Board.objects.order_by('-id')
    # get에서 요청받은 페이지 가져오기, 기본값 = 1
    board_page = int(request.GET.get('page', 1))
    # 페이지당 표시할 게시글 수
    paginator = Paginator(all_boards, contents_num)
    # 요청받은 페이지에서 나타낼 게시글들
    boards = paginator.get_page(board_page)

    # 현재 페이지
    now_page = boards.number

    # 마지막 페이지
    end_page = boards.paginator.num_pages

    # 마지막 페이지가 7 이상일 때
    if end_page >= 7:
        min_page = 7

    # 마지막 페이지가 7 미만일 때
    else:
        min_page = end_page

    # 보여줄 페이지(min_page개)
    display_page = {}
    if now_page <= 4:
        for k in range(min_page):
            display_page[k] = k+1
    elif now_page >= end_page-3:
        for k in range(min_page):
            display_page[k] = (end_page-7)+(k+1)
    else:
        for k in range(min_page):
            display_page[k] = (now_page-4) + (k+1)

    # 이전 페이지묶음
    previous_page_chunk = now_page-7
    if previous_page_chunk < 1:
        previous_page_chunk = 1

    # 다음 페이지묶음
    next_page_chunk = now_page+7
    if next_page_chunk > end_page:
        next_page_chunk = end_page

    # 이전 페이지묶음 이동 아이콘 활성화여부
    if 4 < now_page:
        active_previous_page_chunk = True
    else:
        active_previous_page_chunk = False

    # 다음 페이지묶음 이동 아이콘 활성화여부
    if now_page < (end_page-3):
        active_next_page_chunk = True
    else:
        active_next_page_chunk = False

    context = {
        'boards': boards,
        'now_page': now_page,
        'end_page': end_page,
        'display_page': display_page,
        'previous_page_chunk': previous_page_chunk,
        'next_page_chunk': next_page_chunk,
        'active_previous_page_chunk': active_previous_page_chunk,
        'active_previous_page_chunk': active_previous_page_chunk
    }
    return context


