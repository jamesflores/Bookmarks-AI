from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required



def HomePageView(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "pages/home.html")
    else:
        return HttpResponseRedirect(reverse('bookmarks'))
    

@login_required(login_url='login')
def BookmarksView(request):
    return render(request, "pages/bookmarks.html")
    

class AboutPageView(TemplateView):
    template_name = "pages/about.html"
