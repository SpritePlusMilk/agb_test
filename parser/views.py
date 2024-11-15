from django.http import HttpResponse


def view(request):
    return HttpResponse(open('preview.xml').read(), content_type='text/xml')
