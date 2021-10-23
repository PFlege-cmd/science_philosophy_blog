from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .models import Article
from .forms import ArticleForm


class ArticleCreateView(CreateView, LoginRequiredMixin):
    model = Article
    template_name = 'arts/art_form.html'
    success_url = reverse_lazy('about')

    def get(self, request):
        form = ArticleForm()
        for i in request:
            print(request[i])

        return render(request, self.template_name, { "form": form})

    def post(self, request):
        print("Posting ....")
        form = ArticleForm(request.POST, request.FILES)
        print(request.FILES)
        if not form.is_valid():
            print(form.errors.as_json())
            ctx = {"form": form}
            print("FOrm invalid")
            return render(request, self.template_name, ctx)

        art = form.save(commit = False)
        art.author = self.request.user

        art.save()
        return redirect(self.success_url)

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'arts/art_list.html'
    success_url = reverse_lazy('all')