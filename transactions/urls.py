from django.urls import path

from .views import OperationsListAPIView, BalanceAPIView, WithdrawalAPIView, TransactionAPIView

urlpatterns = [
    path('operations/', OperationsListAPIView.as_view(), name='operations'),
    path('balance/', BalanceAPIView.as_view(), name='balance'),
    path('withdrawal/', WithdrawalAPIView.as_view(), name='withdrawal'),
    path('transaction/', TransactionAPIView.as_view(), name='transaction'),
]
