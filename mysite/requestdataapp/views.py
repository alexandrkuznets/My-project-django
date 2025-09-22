from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from requestdataapp.forms import UserBioForm, UploadFileForm


def process_get_views(request: HttpRequest) -> HttpResponse:

    a = request.GET.get("a", '')
    b = request.GET.get("b", '')
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


# def handle_file_upload(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST" and request.FILES.get("myfile"):
#         myfile = request.FILES["myfile"]
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         print("saved file", filename)
#     return render(request, "requestdataapp/file-upload.html")

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data["file"]
            if myfile.size / (1024 * 1024) < 1:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                print("saved file", filename)
            context["size"] = myfile.size / (1024 * 1024)
    else:
        form = UploadFileForm()
    context["form"] = form

    return render(request, "requestdataapp/file-upload.html", context=context)