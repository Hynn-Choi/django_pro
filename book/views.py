from django.shortcuts import render, redirect
from .models import Book
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    # b = Book.objects.all().order_by("-pubdate")
    b = request.user.book_set.all().order_by('-pubdate')
    pg = request.GET.get("page",1)
    
    pag = Paginator(b, 6)
    obj =pag.get_page(pg) 
    context={
        'blist' : obj,
    }
    return render(request, 'book/index.html', context)

def delete(request, bpk):
    b = Book.objects.get(id=bpk)
    b.delete()
    return redirect('book:index')

def create(request):
    if request.method == "POST":
        n = request.POST.get('sn')
        u = request.POST.get('su')
        c = request.POST.get('con')
        imp = request.POST.get('impo')
        if imp:
            imp=True
        else: 
            imp=False
        Book(site_name=n, site_url=u, content=c, user=request.user ,impo=imp, pubdate=timezone.now()).save()
        return redirect('book:index')
    return render(request, 'book/create.html')