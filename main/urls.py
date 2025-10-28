from django.urls import path
from main.views import product_list_partial, product_create_ajax, product_edit_ajax, product_delete_ajax
from main.views import login_ajax, register_ajax, logout_ajax
from main.views import show_main, create_product, product_detail, edit_product, delete_product
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path("create-product/", create_product, name="create_product"),
    path("product/<int:id>/", product_detail, name="product_detail"),
    path('product/<int:id>/edit/', edit_product, name='product_edit'),
    path('product/<int:id>/delete/', delete_product, name='product_delete'),

    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<str:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:id>/", show_json_by_id, name="show_json_by_id"),

    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login/ajax/', login_ajax, name='login_ajax'),
    path('register/ajax/', register_ajax, name='register_ajax'),
    path('logout/ajax/', logout_ajax, name='logout_ajax'),

    path('products/json/', product_list_partial, name='product_list_json'),
    path('products/create/ajax/', product_create_ajax, name='product_create_ajax'),
    path('products/<int:id>/edit/ajax/', product_edit_ajax, name='product_edit_ajax'),
    path('products/<int:id>/delete/ajax/', product_delete_ajax, name='product_delete_ajax'),
]