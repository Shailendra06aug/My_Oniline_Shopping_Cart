from django.shortcuts import render,HttpResponse,redirect
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.contrib.auth import authenticate,login,logout

#Shop views
# Create your views here.


# def searchMatch(query, item):
#     '''return true only if query matches the item'''
#     if query in  query in item.product_name.lower() or item.desc.lower() or query in item.category.lower():
#         return True
#     else:
#         return False

# def search(request):
#     query = request.GET.get('search','')
#     allProds = []
#     catprods = Product.objects.values('category', 'id')
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         prodtemp = Product.objects.filter(category=cat)
#         prod = [item for item in prodtemp if searchMatch(query, item)]
#         print(prod)
#         n = len(prod)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         if len(prod) != 0:
#             allProds.append([prod, range(1, nSlides), nSlides])
#     params = {'allProds': allProds, "msg": ""}
#     if len(allProds) == 0 or len(query)<4:
#         params = {'msg': "Please make sure to enter relevant search query"}
#     return render(request, 'shop/search.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False



def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        prod = []
        for item in prodtemp:
            if query in item.product_name.lower() or query in item.desc.lower():
                # print("this is item",item)
                prod.append(item)

        # print("prod is ",prod)

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<2:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/index.html', params)




def index(request):
  
  # products = Product.objects.all()
  # print(products)
  # n= len(products)
  # nSlide = n//4+ ceil((n/4)-(n//4))
  # params = {
  #   'products':products,
  #   'no_of_slides': nSlide,
  #   'range': range(1,nSlide)
  # }
  # allProds = [[products, range(1, nSlide),nSlide],
  #             [products, range(1, nSlide),nSlide]]
  # params = {"allProds":allProds}
  
  allProds=[]
  catProds= Product.objects.values('category','id')
  cats = {item['category'] for item in catProds}
  for cat in cats:
    prod = Product.objects.filter(category=cat)
    n= len(prod)
    nSlide = n//4+ ceil((n/4)-(n//4))
    allProds.append([prod, range(1, nSlide), nSlide])
    
    params = {"allProds":allProds}
  
  return render(request,"shop/index.html",params)


def productView(request, myid):
  #Fetch the product using id
  product = Product.objects.filter(id=myid)
  print(product)
  return render(request, "shop/productView.html", {'product':product[0]} )


def about(request):
  
  return render(request,"shop/about.html")

def contact(request):
  thank= False
  if request.method=="POST":
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('number', '')
    desc =  request.POST.get('desc', '')
    print(name,email,phone,desc)
    contact = Contact(name=name, email=email, phone=phone, desc=desc)
    contact.save()
    thank= True
  return render(request,"shop/contact.html",{'thank':thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def search(request):
  
  return render(request,"shop/search.html")



def checkout(request):
    if request.method=="POST":
         items_json = request.POST.get('itemJson', '')
         amount = request.POST.get('amount', '')
         name = request.POST.get('name', '')
         email = request.POST.get('email', '')
         phone = request.POST.get('phone', '')
         address = request.POST.get('address1', '') +" "+  request.POST.get('address2', '')
         state = request.POST.get('state', '')
         city = request.POST.get('city', '')
         zip_code = request.POST.get('zip_code', '')
         print(name,email,phone,address,state,city,zip_code)
         order = Order(items_json=items_json,amount=amount,name=name, email=email, phone=phone, address=address,
                  state=state,city=city,zip_code=zip_code)
         order.save()
         update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
         update.save()
         id= order.order_id
         thank= True
  
         return render(request,"shop/checkout.html",{'thank':thank, 'id':id})
    return render(request,"shop/checkout.html")
    

def Logout(request):
    logout(request)
    return redirect('login')  