from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def index(request):
    cate = request.GET.get("cate","")
    kw = request.GET.get("kw","")
    pg = request.GET.get("page",1)

    if kw:
        if cate == 'sub':
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == 'con':
            b = Board.objects.filter(content__contains=kw)
        else:
            from acc.models import User
            try: 
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
    else:
        b = Board.objects.all()

    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context={
        'blist' : obj,
        'cate' : cate,
        'kw' : kw

    }
    return render(request, "board/index.html", context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        'b' : b,
        'rlist' : r
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
        b = Board.objects.get(id=bpk)
        if b.writer == request.user:
            b.delete()
        else:
            messages.warning(request, "권한이 없습니다.")
        return redirect("board:index")

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    context={
        "b": b
    }
        # 다른사람이 악의적으로 접근했을 때 (19일차)
    if request.user != b.writer:
        messages.warning(request, "권한이 없습니다.")
        return redirect('board:index')

    if request.method == "POST":
        us = request.POST.get('usub')
        uc = request.POST.get('ucon')
        b.subject = us
        b.content = uc
        b.pubdate = timezone.now()
        b.save()
        messages.success(request, "정보가 변경되었습니다.")
        return redirect('board:detail', bpk)
    return render(request, "board/update.html", context)

def create(request):
    if request.method == 'POST':
        us = request.POST.get('usub')
        uc = request.POST.get('ucon')
        Board(subject=us, writer=request.user, content=uc, pubdate=timezone.now()).save()
        messages.success(request, "게시글 작성하였습니다.")
        return redirect("board:index")   
    return render(request, 'board/create.html')
    

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    messages.success(request, "댓글을 작성하였습니다.")
    return redirect("board:detail", bpk)

def dreply(request,bpk,rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()

    else: #19일차 에러 메세지 띄울 예정!
        messages.warning(request,"권한이 없습니다.")
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect('board:detail', bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect('board:detail', bpk)