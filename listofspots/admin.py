

# Register your models here.


# Registration makes our model visible on the admin page
from django.contrib import admin
from .models import Recoverytools
from .models import Recoverytoolsbulk

admin.site.register(Recoverytools)
admin.site.register(Recoverytoolsbulk)
