import datetime
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    context = {
        "products": products,
        'user': request.user.username,
        'shop': 'Football Shop',
        'name': 'Manchaland Store',
        'class': 'PBP E',
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')
    
    context = {
        'form': form
    }
    return render(request, "create_product.html", {"form": form})

@login_required(login_url='/login')
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

@login_required(login_url=reverse_lazy('main:login'))
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    # hanya pemilik boleh edit
    if product.user and product.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this product.")

    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:show_main')

    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required(login_url=reverse_lazy('main:login'))
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)

    # hanya pemilik boleh delete
    if product.user and product.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this product.")

    if request.method == "POST":
        product.delete()
        return redirect('main:show_main')

    # kalau ingin halaman ada konfirmasi delete, render template konfirmasi
    return render(request, 'confirm_delete_product.html', {'product': product})

# XML, JSON, XML by ID, dan JSON by ID.
def show_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type="application/json")

def show_xml_by_id(request, id):
    data = serializers.serialize("xml", Product.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/xml")

def show_json_by_id(request, id):
    data = serializers.serialize("json", Product.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required
@require_POST
def product_create_ajax(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        # render single product card partial to send back
        html = render_to_string('partials/product_card.html', {'product': product, 'user': request.user}, request=request)
        return JsonResponse({'success': True, 'html': html})
    else:
        # return form errors
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
@login_required
@require_POST
def product_edit_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user and product.user != request.user:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        product = form.save()
        html = render_to_string('partials/product_card.html', {'product': product, 'user': request.user}, request=request)
        return JsonResponse({'success': True, 'html': html})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def product_delete_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user and product.user != request.user:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)
    product.delete()
    return JsonResponse({'success': True})

def product_list_partial(request):
    products = Product.objects.all()
    html = render_to_string('partials/product_list.html', {'products': products, 'user': request.user}, request=request)
    return JsonResponse({'html': html})
