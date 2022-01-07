import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse, resolve
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Article, Languages, Categories, Response
from .forms import ArticleForm, ResponseForm


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
        print(art.response_comments.all())
        article_comments_with_responses = []
        for resp in art.response_comments.all():
            article_comments_with_responses.append(
                {"response" : resp,
                 "commented" : len(resp.responded_by.all()) > 0
                 }
            )
        ctx = {"art" : art, "resp_form" : ResponseForm(), "responses": article_comments_with_responses}
        return render(request, self.template_name, ctx)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name =  'arts/art_update.html'
    form_class = ArticleForm

    def get_form_kwargs(self):
        kwargs = super(ResponseView, self).get_form_kwargs()
        print("kwargs are: " + str(kwargs))
        kwargs['user_to_add'] = self.request.user
        return kwargs

    def get(self, request, pk=None):
        art = get_object_or_404(Article, id=pk, author=self.request.user)
        form = ArticleForm(instance=art)
        return render(self.request, self.template_name, {"form": form,
                                                         "art": art})

    def post(self, request, pk=None):
        form = ArticleForm(request.POST)
        if form.is_valid():
            art = get_object_or_404(Article, id=pk, author=self.request.user)
            art.title = request.POST["title"]
            art.text = request.POST["text"]
            art.language = request.POST["language"]
            art.category = request.POST["category"]
            art.snippet = request.POST["snippet"]
            art.background_picture = request.POST["background_picture"]

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

class ResponseView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm

    def get_form_kwargs(self):
        kwargs = super(ResponseView, self).get_form_kwargs()
        print("kwargs are: " + str(kwargs))
        kwargs['user_to_add'] = self.request.user
        return kwargs

    def post(self, request, pk):
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            print("Post is:"  + str(request.POST))
            response.author = self.request.user;
            print(self.kwargs)
            to_article = get_object_or_404(Article, id = pk)
            response.response_to_article = to_article
            response.save()
            print("Body is:"  + str(response.body))

            #return redirect(reverse_lazy("arts:article", kwargs={'pk': pk}))
            return redirect(response.response_to_article.get_absolute_url())

        else:
            return HttpResponse("Invalid")

class ResponseUpdateView(ResponseView):
    form_class = ResponseForm
    model = Response
    template_name = "arts/response_update.html"

    def get(self, request, **kwargs):
        print("Second key is: " + str(kwargs['pk_2']))
        response = get_object_or_404(Response, id=kwargs['pk_2'])
        form = ResponseForm(instance=response)
        print("form is: " + str(form))
        return render(request, self.template_name, {"form": form})


    def post(self, request, **kwargs):
        print("hey");
        article = get_object_or_404(Article, id=kwargs['pk']);
        form = ResponseForm(request.POST);
        if form.is_valid():
            response = get_object_or_404(Response, id=kwargs['pk_2'])
            response.body = form.cleaned_data['body'];
            response.save();
            return redirect(reverse_lazy("arts:article", kwargs = {"pk" : kwargs['pk']}))
        else:
            return HttpResponse(reverse_lazy("arts:article", kwargs = {"pk" : kwargs['pk']}))

    def form_valid(self, form):
        ## ONLY called when the view does not have any default implementation of POST or GET
        print("BIG MOM")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("KAIDO")
        return HttpResponse("FORM IS INVALID FOOL")

class ResponseDeleteView(DeleteView):
    model = Response
    template_name = "arts/response_delete_confirm.html"

    def get_success_url(self, **keyword_arguments):
        ## I got it... kwargs is here than the name of a dict for all named ones :)
        return reverse_lazy("arts:article", kwargs = {"pk" : keyword_arguments['pk']})

    def post(self, request, **kwargs):
        resp = Response.objects.get(id=kwargs['pk_2'])
        resp.delete()
        print("Delete article of id: " + str(kwargs['pk_2']))
        ###WHY THE FUCK DOES THIS WHOLE KEYWORD ISSUE NOT WORK??
        ### APARENTLY, PK's in URLS are KEYWORD WITH DICTIONARY OF VALUES
        return redirect(self.get_success_url(pk = kwargs['pk']))


    def get(self, request, **kwargs):
        print("Getting...")
        return render(request, self.template_name, {})

class ResponseToResponseView(View):
    def post(self, request, **kwargs):

        print("In post")
        print("cookies are: " + str(request.COOKIES))
        print("body is: " + str(request.body))
        print("POST is: " + str(request.POST))
        data = json.loads(request.body)
        print("ID is: " + str(kwargs['pk']))
        print("data is: " + str(data['content']))

        target_response = get_object_or_404(Response, id=kwargs['pk'])

        response = Response(body=data['content'], author=self.request.user, response_to_response=target_response)
        response.save()

        return JsonResponse({"post": "post"})

    def get(self, request, **kwargs):
        return JsonResponse({"get": "get"})

class ShowResponsesToResponseView(View):
    def get(self, request, **kwargs):
        print("Start")
        response = get_object_or_404(Response, id=kwargs['pk'])
        all_responses = response.responded_by.all();
        all_responses_list = []
        for resp in all_responses:
            all_responses_list.append(
                {
                    "body": resp.body,
                    "id": resp.id,
                    "commented" : len(resp.responded_by.all()) > 0
                }
            )
        return JsonResponse(data=all_responses_list, safe=False)

def show_categories(request):

    cats = Categories.choices()
    cats_list = []

    for cat in cats:
        cats_list.append(cat[0])

    ctx = {"enums": cats_list}
    return render(request, 'arts/enum_list.html', ctx)

def show_languages(request):
    langs = Languages.choices()
    lang_list = []

    for lang in langs:
        lang_list.append(lang[0])


    ctx = {"enums": lang_list}
    return render(request, 'arts/enum_list.html', ctx)

class ArticleByLanguageView(ListView):
    model = Article

    def get(self, request, lang):
        print(lang)
        for choice in Languages.choices():
            if lang == choice[0]:
                articles_with_language = Article.objects.filter(language=lang)
                article_list = []

                for article in articles_with_language:
                    article_dict = {}
                    article_dict["id"] = article.id
                    article_dict["title"] = article.title
                    article_list.append(article_dict);

                return JsonResponse(article_list, safe=False)

        for choice in Categories.choices():
            if lang == choice[0]:
                articles_with_category = Article.objects.filter(category=lang)
                article_list = []

                for article in articles_with_category:
                    article_dict = {}
                    article_dict["id"] = article.id
                    article_dict["title"] = article.title
                    article_list.append(article_dict);

                return JsonResponse(article_list, safe=False)





