
from django.shortcuts import render,HttpResponse
from .models import BlogPost

# Create your views here.
def index(request):
  
  blog = BlogPost.objects.all()
  
  return render(request,"blog/index.html",{'blog':blog})


def blogpost(request,id):
  
  post = BlogPost.objects.filter(post_id = id)[0]
  print(post)
  
  return render(request,"blog/blogpost.html",{'post':post})
