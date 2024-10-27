from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View

from newspaper.forms import (
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorSearchForm,
    NewspaperForm,
    RedactorCreationForm,
    RedactorYearsOfExperienceUpdateForm,
    SignUpForm
)
from newspaper.models import Redactor, Newspaper, Topic


@login_required
def index(request):
    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
    }

    return render(request, "newspaper/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspaper/topic_list.html"
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={"name": name})
        return context

    def get_queryset(self):
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return Topic.objects.filter(
                name__icontains=form.cleaned_data["name"])
        return Topic.objects.all()


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspaper:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title})
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.prefetch_related(
            "topics", "publishers").order_by("-published_date")
        title = self.request.GET.get("title")
        if title:
            return queryset.filter(title__contains=title)
        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username})
        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return Redactor.objects.filter(
                username__icontains=form.cleaned_data["username"])
        return Redactor.objects.all()


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related(
        "groups__redactor_set__newspapers"
    )


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorYearsOfExperienceUpdateView(LoginRequiredMixin,
                                          generic.UpdateView):
    model = Redactor
    form_class = RedactorYearsOfExperienceUpdateForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("newspaper:redactor-list")


class ToggleAssignToNewspaperView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk, *args, **kwargs):
        newspaper = get_object_or_404(Newspaper, pk=pk)
        redactor = request.user

        if newspaper in redactor.newspapers.all():
            redactor.newspapers.remove(newspaper)
        else:
            redactor.newspapers.add(newspaper)

        return redirect("newspaper:newspaper-detail", pk=pk)


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("/")
    return render(request, "registration/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
        msg = "Form is not valid"
    else:
        form = SignUpForm()
        msg = None

    return render(request,
                  "registration/register.html",
                  {"form": form, "msg": msg})
