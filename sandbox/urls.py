
from django.urls import path
from . import views

urlpatterns = [
    path("lists/", views.list_edit, name="list_edit"),
    path("list_operations", views.list_operations, name="list_operations"),
    path("solve/", views.solve_for_x, name="solve_for_x"),
    path("tuples/", views.tuple_edits, name="tuple_edits"),
    path("dictionaries/", views.dict_edits, name="dict_edits"),
    path("forms/", views.render_form, name="render_form" ),
    path("basic_form/", views.basic_form, name="basic_form"),
    path("basic_form_action/", views.basic_form_action, name="basic_form_action"),
    path("fave_bands/", views.fave_bands_form, name="fave_bands_form"),
    path("fave_bands_form_action/", views.fave_bands_form_action, name="fave_bands_form_action"),
    path("comix/", views.comix_form, name = 'comix_form'),
    path("planets/",views.planets_form, name = 'planets_form'),
    path("instruments/", views.instruments_form, name='instruments_form'),
    path('bones/', views.bones_urls, name='bones_urls'),
    path('bones/<str:username>/<str:user_id>', views.bones_users, name='bones_users'),
    path('target/', views.hit_target, name='hit_target'),
    path('dynamic_target/<str:target>', views.hit_target, name='hit_moving_target'),
    path('process_target/', views.process_target, name='process_target'),
    path('process_target/<str:target>', views.process_target, name='process_moving_target'),
    path('test/', views.test_form, name='test_page'),

        
    path('file_ops', views.file_ops, name='file_ops'),
    path('regex', views.regex, name='regex')
]



