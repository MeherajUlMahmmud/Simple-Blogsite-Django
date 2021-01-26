from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .forms import EntryForm
from .models import *


@login_required(login_url='login')
def home(request):
    entries = Entry.objects.all().order_by('-entry_date')

    entry_search = ""
    entry_search = request.GET.get('q')

    if entry_search is not None:
        entries = Entry.objects.filter(Q(entry_title__icontains=entry_search))

    context = {
        'blog_entries': entries,
        'entry_search': entry_search,
    }
    return render(request, 'entries/index.html', context)


@login_required(login_url='login')
def detail_view(request, entry_slug):
    blog = Entry.objects.get(entry_slug=entry_slug)
    context = {
        'blog': blog,
    }
    return render(request, 'entries/entry_detail.html', context)


@login_required(login_url='login')
def add_blog_view(request):
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            blog = form.save()
            blog.entry_author = request.user
            slug_str = "%s %s" % (blog.entry_title, blog.entry_date)
            blog.entry_slug = slugify(slug_str)
            form.save()
            return redirect('blog-home')
        else:
            return redirect('create-entry')

    context = {
        'form': form,
    }
    return render(request, 'entries/create_entry.html', context)


@login_required(login_url='login')
def edit_blog_view(request, pk):
    blog = Entry.objects.get(id=pk)
    form = EntryForm(instance=blog)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save()
            slug_str = "%s %s" % (blog.entry_title, blog.entry_date)
            blog.entry_slug = slugify(slug_str)
            form.save()
            return redirect('entry-detail', blog.id)
        else:
            return redirect('edit-entry', request.BlogModel.id)

    context = {
        'form': form,
    }
    return render(request, 'entries/edit_entry.html', context)


@login_required(login_url='login')
def delete_blog_view(request, pk):
    blog = Entry.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog-home')

    context = {
        'item': blog,
    }
    return render(request, 'entries/delete_entry.html', context)
