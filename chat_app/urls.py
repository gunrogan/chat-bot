from django.urls import path

from . import views

urlpatterns = [
    # --- Активный вариант (задаётся в config.json) ---
    path('', views.chat_page, name='chat_page'),
    path('api/chat/send/', views.api_chat_send, name='api_chat_send'),

    # --- Демо «Робот-Учёный» (доступно при каждом запуске) ---
    path('demo/', views.chat_page_demo, name='chat_page_demo'),
    path('api/chat/send_demo/', views.api_chat_send_demo, name='api_chat_send_demo'),
]