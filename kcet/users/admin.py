from django.contrib import admin
from .models import Student, PreviousDegree, KCETResult, PUResult, FormLastActive, DocumentVerified

# Register your models here.
admin.site.register(Student)
admin.site.register(PreviousDegree)
admin.site.register(KCETResult)
admin.site.register(PUResult)
admin.site.register(FormLastActive)
admin.site.register(DocumentVerified)