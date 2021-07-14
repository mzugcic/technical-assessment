from django.contrib import admin
from django.contrib.auth import get_user_model

from transactions.models import Operation

User = get_user_model()

admin.site.register([
    User,
    Operation
])
