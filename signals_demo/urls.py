from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('test-sync-thread/', views.test_sync_thread_view, name='test_sync_thread'),
    path('test-transaction-rollback/', views.test_transaction_rollback_view, name='test_transaction_rollback'),
    path('test-rectangle/', views.test_rectangle_view, name='test_rectangle'),
]
