from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests

from pages.forms import BookmarkAddForm, BookmarkEditForm
from pages.models import Bookmark, Category

import marvin

from bs4 import BeautifulSoup
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

from summa import summarizer


def HomePageView(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "pages/home.html")
    else:
        return HttpResponseRedirect(reverse('bookmarks'))
    

@login_required(login_url='/accounts/login')
def BookmarksView(request, category=None):
    form = BookmarkAddForm()
    all_bookmarks = Bookmark.objects.all().filter(user=request.user)
    bookmarks = all_bookmarks.order_by('-created_at')

    # Filter by category
    if category:
        bookmarks = bookmarks.filter(category__name__icontains=category)

    # Sorting
    sort_by = request.GET.get('sort_by')
    sort_order = request.GET.get('sort_order', 'asc')  # Default sort order is ascending
    if sort_by == 'title':
        if sort_order == 'asc':
            bookmarks = bookmarks.order_by('title')
        else:
            bookmarks = bookmarks.order_by('-title')
    elif sort_by == 'category':
        if sort_order == 'asc':
            bookmarks = bookmarks.order_by('category__name')
        else:
            bookmarks = bookmarks.order_by('-category__name')
    elif sort_by == 'date':
        if sort_order == 'asc':
            bookmarks = bookmarks.order_by('created_at')
        else:
            bookmarks = bookmarks.order_by('-created_at')

    # Pagination
    page_number = request.GET.get('page')
    per_page = request.GET.get('per_page', settings.BOOKMARKS_PER_PAGE) 
    paginator = Paginator(bookmarks, per_page)
    page_obj = paginator.get_page(page_number)

    # Pagination variables
    next_page = page_obj.next_page_number() if page_obj.has_next() else None
    previous_page = page_obj.previous_page_number() if page_obj.has_previous() else None
    has_next = page_obj.has_next()
    
    categories = Category.objects.filter(approved=True, bookmark__in=all_bookmarks).distinct().order_by('name')
    return render(request, "pages/bookmarks.html", {
        'bookmarks': page_obj,
        'categories': categories,
        'filter_category': category,  # current category being viewed
        'form': form,
        'paginator': paginator,
        'page_obj': page_obj,
        'next_page': next_page,
        'previous_page': previous_page,
        'has_next': has_next,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required(login_url='/accounts/login')
def SearchBookmarksView(request):
    search_query = request.GET.get('q')
    if search_query:
         # Define the Q objects for searching in title, description, summary, notes, and category name
        q_objects = Q(title__icontains=search_query) | Q(description__icontains=search_query) | \
                    Q(summary__icontains=search_query) | Q(notes__icontains=search_query) | \
                    Q(category__name__icontains=search_query)  # Assuming 'name' is a field in 'Category'
        bookmarks = Bookmark.objects.filter(user=request.user).filter(q_objects).distinct()

        return render(request, "pages/search.html", {
            'bookmarks': bookmarks,
            'query': search_query,
        })
    else:
        return HttpResponseRedirect(reverse('bookmarks'))
    

@login_required(login_url='/accounts/login')
def add_bookmark(request):
    if request.method == 'POST':
        form = BookmarkAddForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.notes = form.cleaned_data['notes']

            # check if URL is reachable
            print(f"[{request.user}] Add bookmark: {bookmark.url}")
            response = requests.get(bookmark.url)
            if response.status_code != 200:
                messages.error(request, 'Error saving bookmark. Invalid URL or URL not reachable.')
                return HttpResponseRedirect(reverse('bookmarks'))
            
            # get og tags
            og_tags = get_og_tags(response.content)
            bookmark.title = og_tags['title'] if og_tags['title'] else bookmark.url.strip('https://').strip('http://')
            bookmark.description = og_tags['description'] if og_tags['description'] else None

            # strip html from content
            content = BeautifulSoup(response.content, 'html.parser').get_text()
            #bookmark.summary = get_content_summary(content[:20000])  # Marvin AI
            bookmark.summary = summarizer.summarize(content)  # Summa
            print(f"Bookmark summary: {bookmark.summary}")

            # classify bookmark
            categories = Category.objects.filter(approved=True)
            category = marvin.classify(
                f'{bookmark.title} {bookmark.description}',
                labels=[category.name for category in categories]
            )
            bookmark.category = Category.objects.get(name=category)

            bookmark.save()
            messages.success(request, 'Bookmark saved successfully.')
        else:
            messages.error(request, 'Error saving bookmark. (Did you complete the captcha?)')

    return HttpResponseRedirect(reverse('bookmarks'))


@login_required(login_url='/accounts/login')
def edit_bookmark(request, pk):
    try:
        bookmark = Bookmark.objects.get(pk=pk)
    except Bookmark.DoesNotExist:
        messages.error(request, 'Bookmark not found.')
        return HttpResponseRedirect(reverse('bookmarks'))
    
    if bookmark.user != request.user:
        messages.error(request, 'Unauthorised access.')
        return HttpResponseRedirect(reverse('bookmarks'))
    
    if request.method == 'POST':
        form = BookmarkEditForm(request.POST, instance=bookmark)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.title = form.cleaned_data['title']
            bookmark.description = form.cleaned_data['description']
            bookmark.notes = form.cleaned_data['notes']
            bookmark.category = form.cleaned_data['category']
            bookmark.save()

            messages.success(request, 'Bookmark updated successfully.')
            return HttpResponseRedirect(reverse('bookmarks'))
    else:
        form = BookmarkEditForm(instance=bookmark)

    return render(request, "pages/edit.html", {
        'bookmark': bookmark,
        'form': form,
    })


@login_required(login_url='/accounts/login')
def delete_bookmark(request, pk):
    try:
        bookmark = Bookmark.objects.get(pk=pk)
    except Bookmark.DoesNotExist:
        messages.error(request, 'Bookmark not found.')
        return HttpResponseRedirect(reverse('bookmarks'))
    
    if bookmark.user != request.user:
        messages.error(request, 'Unauthorised access.')
        return HttpResponseRedirect(reverse('bookmarks'))
    
    bookmark.delete()
    messages.success(request, 'Bookmark deleted successfully.')
    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        return HttpResponseRedirect(referrer)
    else:
        return HttpResponseRedirect(reverse('bookmarks'))


# Input: HTML content, Output: dict of OG tags
def get_og_tags(content: str) -> dict:
    try:
        soup = BeautifulSoup(content, 'html.parser')
        meta_title = soup.find('meta', attrs={'name': 'title'}) or soup.find('meta', attrs={'property': 'og:title'})
        meta_description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        meta_image = soup.find('meta', attrs={'name': 'image'}) or soup.find('meta', attrs={'property': 'og:image'})
        
        tags = {
            'title': meta_title['content'] if meta_title else None,
            'description': meta_description['content'] if meta_description else None,
            'image': meta_image['content'] if meta_image else None,
        }
        print(f"OG tags: {tags}")
        return tags
    except Exception as e:
        print(f"Error: {e}")
    return None


@marvin.fn
def get_content_summary(text: str) -> str:
    """
    Returns a summary of the content in 1-2 paragraphs.
    """


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class PrivacyPageView(TemplateView):
    template_name = "pages/privacy.html"


class TermsOfServicePageView(TemplateView):
    template_name = "pages/tos.html"