from django.shortcuts import render,redirect
from .forms import ItemCreateForm,UserLoginForm,UserRegisterForm
from datetime import datetime
from .models import AppUser,Item
#API
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from .serializers import AppUserSerializer,ItemSerializer
#PAGIANTION
from django.core.paginator import Paginator



# Create your views here.

class ItemApiView(APIView):

    def get(self, request):
        item_list = Item.objects.all()
        serializer = ItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

def item_search(request):
    if request.method=="POST":
        searched=request.POST['searched']
        itemss=Item.objects.filter(title__contains=searched) #title chai model ko item name 

        return render(request,'items/search.html',{'searched':searched,'itemss':itemss})

def item_index(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    item_list=Item.objects.all()
    p=Paginator(Item.objects.all(),2)  
    page=request.GET.get('page')
    venues=p.get_page(page)
    context={"item_list":item_list,"venues":venues}  # item_list pass garda all obj , venues pass garda chai defined no of objects
    return render(request, "items/index.html",context)

def item_show(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Item.objects.get(id=id)
    context = {"data": data}
    return render(request, "items/show.html", context)

def item_edit(request,id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data=Item.objects.get(id=id)
    context={"data":data}
    return render(request, "items/edit.html",context)
def item_delete(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data=Item.objects.get(id=id)
    context={"data":data}
    return render(request, "items/delete.html",context)
def item_update(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    if request.method == "POST":
        item_obj = Item.objects.get(id=request.POST.get("id"))
        user = AppUser.objects.get(id=1)
        item_obj.title = request.POST.get("title")
        item_obj.particular = request.POST.get("particular")
        item_obj.lf = request.POST.get("lf")
        item_obj.price = request.POST.get("price")
        item_obj.quantity = request.POST.get("quantity")
        item_obj.total = request.POST.get("total")
        item_obj.added_at = datetime.now()
        item_obj.user = user
        item_obj.save()

    return redirect("items.index")

def item_create(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    form=ItemCreateForm
    context={"form":form}
    if request.method=="POST":
        item=Item()
        user = AppUser.objects.get(id=1)
        item.title = request.POST.get("title")
        item.particular = request.POST.get("particular")
        item.lf = request.POST.get("lf")
        item.price = request.POST.get("price")
        item.quantity = request.POST.get("quantity")
        item.total = request.POST.get("total")
        item.added_at = datetime.now()
        item.user = user
        context.setdefault("msg", "Item Created Successfully")
        item.save()
    return render(request, "items/create.html",context)
def user_login(request):
    form = UserLoginForm()
    context = {"form": form}
    if request.method == "POST":
        req_email = request.POST.get("email")
        req_password = request.POST.get("password")
        user = AppUser.objects.get(email=req_email)
        if user.email == req_email and user.password == req_password:
            request.session["session_email"] = user.email
            #request.session.setdefault("session_email", user.email)
            #request.session.update({"session_email": user.email})
            return redirect("items.index")
        else:
            return redirect("users.login")
    return render(request, "users/login.html", context)
def user_logout(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    del request.session["session_email"]
    return redirect("users.login")
def user_register(request):
    form = UserRegisterForm()
    context = {"form": form}
    if request.method == "POST":
        user = AppUser()
        user.full_name = request.POST["full_name"]
        user.email = request.POST["email"]
        user.contact = request.POST["contact"]
        user.password = request.POST["password"]
        user.save()
    return render(request, "users/register.html", context)