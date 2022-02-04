from django.shortcuts import render
import googletrans
from googletrans import Translator

# Create your views here.
def translator(request):
    context = {
        "ndict" : googletrans.LANGUAGES
    }
    if request.method == "POST":

        tx = request.POST.get('intext')

        bl = request.POST.get("bl")
        al = request.POST.get("al")

        translator = Translator()
        rs = translator.translate(tx, src=bl, dest=al)
        context.update({
            'al' : al,
            'bl' : bl,
            'tx' : tx,
            'rs' : rs.text,
        })
    # else
    return render(request, 'trans/translator.html', context)