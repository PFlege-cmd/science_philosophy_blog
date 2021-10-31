from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Article, Languages, Categories
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
    success_url = reverse_lazy('arts:all')

    def get_queryset(self):
        qs = super().get_queryset().order_by('time_created').reverse()

        if self.request.GET.get("search") is not None:
            strval = self.request.GET["search"]
            q = Q(title__icontains=strval)|Q(text__icontains=strval)
            return qs.filter(q)

        return qs

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'arts/art_detail.html'

    def get(self, request, **kwargs):
        art = Article.objects.get(id=self.kwargs.get('pk'))
        ctx = {"art" : art}
        return render(request, self.template_name, ctx)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name =  'arts/art_update.html'
    form_class = ArticleForm

    def get(self, request, pk=None):
        art = get_object_or_404(Article, id=pk, author=self.request.user)
        form = ArticleForm(instance=art)
        return render(self.request, self.template_name, {"form": form,
                                                         "art": art})

    def post(self, request, pk=None):
        form = ArticleForm(request.POST)
        if form.is_valid():
            art = form.save(commit=False)
            art.author = self.request.user
            art.save()
            return redirect(reverse('arts:all'))

        art = get_object_or_404(Article, id=pk, author=self.request.user)
        return render(request, self.template_name, {"form": form,
                                                    "art": art})



class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('arts:all')
    template_name = 'arts/article_delete_confirm.html'
    model = Article

    def get_queryset(self):
        qs = super(DeleteView, self).get_queryset()
        return qs.filter(author=self.request.user)

#class CategoryView(LoginRequiredMixin, ListView):
#    model = Languages;
#    template_name = "arts/category_list.html"

def show_categories(request):

    cats = Categories.choices()
    cats_list = []

    for cat in cats:
        cats_list.append(cat[0])

    ctx = {"categories": cats_list}
    return render(request, 'arts/category_list.html', ctx)

def show_languages(request):
    langs = Languages.choices()
    lang_list = []

    for lang in langs:
        lang_list.append(lang[0])

    ctx = {"languages": lang_list}
    return render(request, 'arts/language_list.html', ctx)

class ArticleByLanguageView(ListView):
    model = Article

    def get(self, request, lang):
        articles_with_language = Article.objects.filter(language=lang)
        article_dict = {}

        for article in articles_with_language:
            article_dict[article.id] = article.title

        return JsonResponse(article_dict)




