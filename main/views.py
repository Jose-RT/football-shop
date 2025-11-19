import datetime, requests
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
from zoneinfo import ZoneInfo
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json
from django.http import JsonResponse

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'
    sort_by = request.GET.get('sort') 

    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)
        
    if sort_by == 'price-asc': 
        products = products.order_by('price') 
    elif sort_by == 'price-desc': 
        products = products.order_by('-price')

    context = {
        "products": products,
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
        wib_time = datetime.datetime.now(tz=ZoneInfo("Asia/Jakarta"))
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(wib_time))
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

@require_POST
def login_ajax(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = JsonResponse({'success': True, 'redirect': reverse('main:show_main')})
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
    else:
        # return form errors in JSON-friendly format
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Account created'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
def logout_ajax(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect': reverse('main:login')})

@login_required
@require_POST
def product_create_ajax(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        # render single product card partial to send back
        html = render_to_string('partials/product_card.html', {'product': product}, request=request)
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
    html = render_to_string('partials/product_list.html', {'products': products}, request=request)
    return JsonResponse({'html': html})

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_news_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = strip_tags(data.get("title", ""))  # Strip HTML tags
        content = strip_tags(data.get("content", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        user = request.user
        
        new_news = News(
            title=title, 
            content=content,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_news.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)