from django.urls import path

from transactionapp.views import *


urlpatterns = [
    path('send-money/', TransactionAPIView.as_view(), name='transactions'),
    path('transaction-history/', TransactionHistoryAPIView.as_view(), name='transaction_history'),
    path('scheduler/', TransactionScheduler.as_view(), name='demo') ,  
]