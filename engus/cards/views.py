from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class MyDeckListView(ListView):

    def get_queryset(self):
        pass