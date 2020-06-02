from django.shortcuts import render,redirect
from.forms import UserLoginForm
from rest_framework import viewsets,generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Post,Category,Comment
from .serializers import PostSerializer,CategorySerializer,ReadPostSerializer,CommentSerializer,NestedPostSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)

@api_view()
def likes_api(request,id):
    post = Post.objects.get(id=id)
    serializer = ReadPostSerializer(post)
    user = request.user 

    if user in post.hearts.all():
        post.hearts.remove(user)
    if user in post.likes.all():
        post.likes.remove(user)
    if user in post.sads.all():   
        post.sads.remove(user)
    else: 
        post.likes.add(user)   
    return Response(serializer.data)

@api_view()
def hearts_api(request,id):
    post = Post.objects.get(id=id)
    serializer = ReadPostSerializer(post)
    user = request.user 
    if user in post.likes.all():
        post.likes.remove(user)  
    if user in post.sads.all():
        post.sads.remove(user)
    if user in post.hearts.all():   
        post.hearts.remove(user)
    else: 
        post.hearts.add(user)   
    return Response(serializer.data)

@api_view()
def sads_api(request,id):
    post = Post.objects.get(id=id)
    serializer = ReadPostSerializer(post)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    if user in post.hearts.all():
        post.hearts.remove(user) 
    if user in post.sads.all():   
        post.sads.remove(user)
    else: 
        post.sads.add(user)   
    return Response(serializer.data)    

# Create your views here.
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        login(request,user)
        print(request.user.is_authenticated)
        return redirect('/home')
    return render(request,'login.html',{'form':form})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')    

@login_required(login_url='/login')
def home(request):
    cats = Category.objects.all()
    context={'message':'hello world','num':30, 'categories':cats}
    return render(request,'home.html',context)

@login_required(login_url='/login')
def byCategory(request,id):
    return render(request, 'bycategory.html',{'pk':id, 'categories':Category.objects.all()})

@login_required(login_url='/login')
def about(request):
    return render(request,'abouts.html')

def page(request):
    return render(request,'page.html')
    
def blog(request):
    return render(request,'blogs.html')
        
@login_required(login_url='/login')
def contacts(request):
    return render(request,'contacts.html')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,JSONParser)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'


class ReadPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = ReadPostSerializer

class PostByCategory(generics.ListAPIView):
    serializer_class = ReadPostSerializer
    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
    
        cat = Category.objects.get(id=cat_id)
        return Post.objects.filter(category = cat).order_by('-date_created')

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-date_created')
    serializer_class = CommentSerializer        

class NestedPostList(generics.ListAPIView):
    serializer_class = NestedPostSerializer
    def get_queryset(self):
        return Post.objects.all().order_by('-date_created')