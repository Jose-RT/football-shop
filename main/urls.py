from django.urls import path
from main.views import show_main, create_product, product_detail, edit_product, delete_product
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path("create-product/", create_product, name="create_product"),
    path("product/<str:id>/", product_detail, name="product_detail"),
    path('product/<int:id>/edit/', edit_product, name='product_edit'),
    path('product/<int:id>/delete/', delete_product, name='product_delete'),
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<str:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:id>/", show_json_by_id, name="show_json_by_id"),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]