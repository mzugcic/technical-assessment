from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from transactions.models import Operation
from transactions.serializers import OperationSerializer, UserBalanceSerializer, \
    WithdrawalSerializer, TransactionSerializer

User = get_user_model()


class OperationsListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OperationSerializer

    def get_queryset(self):
        return Operation.objects.filter(
            user_id=self.request.user.id
        )


class BalanceAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserBalanceSerializer

    def get_object(self):
        obj = get_object_or_404(
            self.queryset,
            id=self.request.user.id,
        )

        self.check_object_permissions(self.request, obj)

        return obj


class WithdrawalAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = WithdrawalSerializer


class TransactionAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = TransactionSerializer
