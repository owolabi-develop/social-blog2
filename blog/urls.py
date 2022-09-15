
from django.urls import include,path,re_path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
app_name ='blog'
urlpatterns = [
    path("",views.index,name="index"),
    path("Search/",views.searchArticle,name='search'),
    path("login/",views.UserLogin,name="Login"),
    path("SignUp/",views.UserSignUp,name="SignUp"),
    re_path('^Email-Activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$',
        views.email_confirm, name='Email-activate'),
    path("forgotpassword/",views.forgotPassword,name='forgotpassword'),
    re_path('^Password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$',
        views.password_reset.as_view(), name='password-reset'),
    path("Signup_success/",views.Signup_success,name='Signup_success'),
    path("Setting/Profile/<email>/",views.UserProfile,name="Profile"),
    path("Details/<headlines>/",views.details,name='details'),
    path("Logout/",views.User_logOut,name='logout'),
    path("PasswordRestDown/",views.password_down,name='password-down'),
    path('passwordchangcomplete/',views.password_reset_complete,name='password_reset_complete'),
    path('Setting/AccountManagement/<email>/',views.accountManagement,name='aaccount-Management'),
    path('Setting/ArticleManagement/<email>/',views.ArticleManagement,name='Article-Management'),
    path('Setting/ArticleManagement/ArticleEdit/<int:article_id>/',views.ArticleEdit,name='Article-Edit'),
    path('Delete/<int:article_id>/',views.ArticleDelete,name='delete-article'),
    path("<title>/",views.CategoryPage,name='article-category'),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
