from django.contrib import admin
from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('tool/<int:tool_id>/', views.tool_details, name='tool_details'),
    path('book_tool/<int:tool_id>/', views.book_tool, name='book_tool'),
    path('category/<int:category_id>/', views.category_listing, name='category_listing'),
    path('add_review/<int:tool_id>/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),

    path('payment_success/', views.payment_success, name='payment_success'),

    path("chatbot/", views.chatbot_response, name="chatbot"),

    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),


     
]

    
