from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:wiki_page>', views.fetch_wiki_page, name="fetch_wiki_page"),
    path('process_search/', views.process_search, name='process_search'),
    path('new_wiki_form/', views.new_wiki_form, name="new_wiki_form"),
    path('create_new_wiki', views.create_new_wiki, name='create_new_wiki' ),
    path('edit_wiki/<str:wiki_page>', views.edit_wiki, name='edit_wiki'),
    path('save_wiki_edit/<str:wiki_page>', views.save_wiki_edit, name='save_wiki_edit'),
    path('random_wiki', views.random_wiki, name="random_wiki")
]
