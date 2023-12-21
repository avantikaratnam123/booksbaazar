from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    
    path('',views.ProductView.as_view(),name="home"),       
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.show_cart, name='showcart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('add-to-cart',views.add_to_cart,name='add-to-cart'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),name='password_reset_complete'),
    # path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm),name='passwordchange'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('astrologybooks/<slug:data>',views.astrologybooks,name='astrologydata'),
    path('astrologybooks/', views.astrologybooks, name='astrologybooks'),
    path('dietbooks/<slug:data>',views.dietbooks,name='dietdata'),
    path('dietbooks/', views.dietbooks, name='dietbooks'),
    path('yogabooks/<slug:data>',views.yogabooks,name='yogadata'),
    path('yogabooks/', views.yogabooks, name='yogabooks'),
    path('spiritualbooks/<slug:data>',views.spiritualbooks,name='spiritualdata'),
    path('spiritualbooks/', views.spiritualbooks, name='spiritualbooks'),
    # path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('search_query/', views.search_query, name='search_query'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page ='login'),name='logout'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
]+ static (settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
