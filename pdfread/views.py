from django.shortcuts import render
import pdfplumber
# Create your views here.
def pdfreader(request):
    if request.method == 'POST':
        p = request.FILES.get('pdf')
        pdf = pdfplumber.open(p)
        t = ""

        for i in range(len(pdf.pages)):
            t += f"Page {i+1} Text Start?" + "\n" + '┌'+ "·-"*75 + "·┐"
            t += pdf.pages[i].extract_text()
            t += "\n" + '└'+ "·-"*75 + '·┘' +'\n'+ f"Page {i+1} Text End!\n" 

        pdf.close()

        context ={ 't' : t }
        return render(request, 'pdfread/pdfreader.html', context)
    return render(request, 'pdfread/pdfreader.html')