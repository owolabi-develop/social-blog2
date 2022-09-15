
from multiprocessing import reduction
from django.utils import timezone
from datetime import datetime
from django.core import serializers
from django.db.models.query_utils import Q
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from . forms import UserCreationForm, UserPasswordResetForm,UserSetPassword,ProfileForm,UserEditForm,UserChangePassword,ArticleForm,CommentForm
from . models import Profile,User
from django.contrib.auth.tokens import PasswordResetTokenGenerator as default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str,force_bytes
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from . tokens import account_activation_token
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from .models import Article,Comment,Article_Category


# Create your views here.
def post_save_Profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.get_or_create(User=instance)
post_save.connect(post_save_Profile, sender=settings.AUTH_USER_MODEL)
        

def index(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        query = request.GET.get('query',None)
        Articledata = Article.objects.filter(Q(headlines__icontains=query)|Q(body__icontains=query))
        user = User.objects.filter(article__headlines__icontains=Articledata)
       
        if len(query) > 0 and len(Articledata) > 0:
            data = []
           
            for query in Articledata:
                item = {
                    'id':query.id,
                    'headlines':query.headlines,
                    'body':query.body,
                    'Article_pic':query.Article_pic.url,
                    'pub_date':query.pub_date,
                    'author':query.author_id,
                }
                data.append(item)
            result = data
            category = Article_Category.objects.all()
        else:
            result = "No Article Found"
        return JsonResponse({'data':result})
                

    try:
        category = Article_Category.objects.all()
        recentArt = Article.objects.earliest('pub_date')
        allArtticle  = Article.objects.all()
        paginator = Paginator(allArtticle,5)
        page_number = request.GET.get('page')
        allArt = paginator.get_page(page_number)
        recentArt2 = Article.objects.order_by('headlines')[:2]
        recentArt3 = Article.objects.order_by('-last_modified')[:6]
    except Article.DoesNotExist:
        return {}
    return render(request,'blog/index.html',
    {'recent':recentArt,
    'Article':allArt,
    'recent2':recentArt2, 
    'recentArt3': recentArt3,
    'category':category
    })

def UserLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email,password=password)
        
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("blog:Profile",args=(user.get_username(),)))
        else:
             messages.error(request,'Email or Password is incorrect try again')

    return render(request,'blog/login.html')


def UserSignUp(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject_email = "Activate Your Email"
            message = render_to_string('blog/email_template.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
                'protocol':'http',
            })
            to_email = form.cleaned_data['email']
            from_email='owolabidevelop84@gmail.com'
            print(to_email)
            msg = EmailMultiAlternatives(subject_email,'Confirmation Form Owolabiblog',from_email,[to_email])
            msg.attach_alternative(message,'text/html')
            msg.send()
            return HttpResponseRedirect(reverse("blog:Signup_success"))
    else:
        form = UserCreationForm() 
    return render(request,"blog/signup.html",{'form':form})

class password_reset(PasswordResetConfirmView):
    template_name = "blog/UserSetpassword.html"
    success_url = reverse_lazy("blog:password_reset_complete")


def password_reset_complete(request):
    return render(request,'blog/passwordchange.html')
     
        

def email_confirm(request,uidb64,token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(),pk=uid)
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return HttpResponseRedirect(reverse("blog:Profile",args=(user.get_username(),)))
    else:
        return HttpResponse("Activation link invalid")

def Signup_success(request):
    return render(request,'blog/Signup_success.html')

@login_required(login_url="/login/")
def UserProfile(request,email):
    user = get_object_or_404(get_user_model(),email=email)
    category = Article_Category.objects.all()
    if request.method =="POST":
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm()

    return render(request,"blog/profile.html",{'user':user,'form':form,'category':category})

def details(request,headlines):
    category = Article_Category.objects.all()
    ComArticle = get_object_or_404(Article,headlines=headlines)
    #user = get_object_or_404(get_user_model(),email=request.user)
    related = Article.objects.filter(headlines__icontains=ComArticle)[:3]
    author = Article.objects.filter(author__username=request.user)
    if request.method =="POST":
        comment = CommentForm(request.POST)
        if comment.is_valid():
            instance = comment.save(commit=False)
            instance.Article = ComArticle
            instance.save()
    else:
        comment = CommentForm()
    return render(request,"blog/details.html",{'category':category,"blog":ComArticle,'related':related,'form':comment,'author':author})

@login_required(login_url="/login/")
def ArticleEdit(request,article_id):
     article = get_object_or_404(Article,pk=article_id)
     category = Article_Category.objects.all()
     if request.method =="POST":
        form = ArticleForm(request.POST,request.FILES,instance=article)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request,'{} Article was published successfully'.format(form.cleaned_data['headlines']))
     else:
        form = ArticleForm(instance=article)

     return render(request,'blog/EdithArticle.html',{'category':category,"form":form,"article":article})
     
@login_required(login_url="/login/")
def ArticleDelete(request,article_id):
      Article.objects.get(pk=article_id).delete()
      user = get_object_or_404(get_user_model(),email=request.user)
      messages.success(request,'')
      return HttpResponseRedirect(reverse("blog:Article-Management",args=(user.get_username(),)))



def forgotPassword(request):
    if request.method =="POST":
        form = UserPasswordResetForm(data=request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['email']
            form.save(get_current_site(request),email_template_name='blog/pwd_email_reset.html')
            return HttpResponseRedirect(reverse("blog:password-down"))
    else:
        form = UserPasswordResetForm()

    return render(request,"blog/forgetpassword.html",{"form":form})

def User_logOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("blog:Login"))

def password_down(request):
    return render(request,'blog/password-down.html')


@login_required(login_url="/login/")
def accountManagement(request,email):
    category = Article_Category.objects.all()
    user = get_object_or_404(get_user_model(),email=email)
    if request.method == "POST":
        PasswordChangeform = UserChangePassword(user=request.user, data=request.POST)
        userEditform = UserEditForm(request.POST,instance=request.user)
        if userEditform.is_valid():
            userEditform.save()
            messages.success(request,'User info Update Successful')
        if PasswordChangeform.is_valid():
            PasswordChangeform.save()
            update_session_auth_hash(request, PasswordChangeform.user)
            messages.success(request,'Password Update Successful')
    else:
        PasswordChangeform = UserChangePassword(user=request.user)
        userEditform = UserEditForm()
    return render(request,"blog/accountmanage.html",{'category':category,'form1':PasswordChangeform,'form2': userEditform,'user':user})


@login_required(login_url="/login/")
def ArticleManagement(request,email):
    category = Article_Category.objects.all()
    user = get_object_or_404(get_user_model(),email=email)
    Article_data = Article.objects.filter(author=request.user)
    if request.method =="POST":
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request,'{} Article was published successfully'.format(form.cleaned_data['headlines']))
    else:
        form = ArticleForm()
    return render(request,'blog/ArticleManagement.html',{'category':category,'user':user,'form':form,'article': Article_data})

def CategoryPage(request,title):
    categorylist1 = get_object_or_404(Article_Category,Title=title)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        ArticleQuery = request.GET.get('query',None)
        Articledata = categorylist1.article_set.filter(Q(headlines__icontains=ArticleQuery)|Q(body__icontains=ArticleQuery)).all()
        if len(ArticleQuery) > 0 and len(Articledata) > 0:
            data = []
            for query in Articledata:
                item = {
                    'id':query.id,
                    'headlines':query.headlines,
                    'body':query.body,
                    'pub_date':query.pub_date,
                    'Article_pic':query.Article_pic.url,
                }
                data.append(item)
            result = data
        else:
            result = "No item Found"
        return JsonResponse({'data':result})
    categorylistpigination = Article.objects.filter(Category__Title=categorylist1)
    category = Article_Category.objects.all()
    recent3 = Article.objects.filter(Category__Title=categorylist1).order_by('-pub_date')[:5]
    paginator = Paginator(categorylistpigination,5)
    page_number = request.GET.get('page')
    categorylist = paginator.get_page(page_number)
    
    
    
    return render(request,'blog/category.html',{"categorylist":categorylist,'category':category,'recent3':recent3,'categorylist1':categorylist1})

def searchArticle(request):
    user = get_object_or_404(get_user_model(),email=request.user)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        ArticleQuery = request.GET.get('query',None)
        Articledata = user.article_set.filter(Q(headlines__icontains=ArticleQuery)|Q(body__icontains=ArticleQuery)).all()
        if len(ArticleQuery) > 0 and len(Articledata) > 0:
            data = []
            for query in Articledata:
                item = {
                    'id':query.id,
                    'headlines':query.headlines,
                    'body':query.body,
                    'pub_date':query.pub_date,
                    'Article_pic':query.Article_pic.url,
                    'user':user.username,
                }
                data.append(item)
            result = data
        else:
            result = "No item Found"
        return JsonResponse({'data':result})
    
    return render(request,'blog/settings.html',{})


