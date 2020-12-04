from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EntryForm
from .models import Entry


@login_required(login_url='login')
def home(request):
    entries = Entry.objects.all().order_by('-entry_date')

    entry_search = request.GET.get('q')

    if entry_search is not None:
        entries = Entry.objects.filter(Q(entry_title__icontains=entry_search))

    context = {
        'blog_entries': entries,
    }
    return render(request, 'entries/index.html', context)


@login_required(login_url='login')
def detail_view(request, pk):
    blog = Entry.objects.get(id=pk)
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
            blog = form.save(commit=False)
            blog.entry_author = request.user
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
            form.save()
            return redirect('entry-detail', blog.id)
        else:
            return redirect('edit-entry', request.BlogModel.id)

    context = {
        'form': form,
    }
    return render(request, 'entries/edit_entry.html', context)


class DeleteEntryView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'entries/delete_entry.html'

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        return super().form_valid(form)
