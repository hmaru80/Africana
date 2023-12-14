from django.contrib import admin
from .models import *
from Blogs.models import Articles

# Register your models here.

admin.site.register(Articles)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Category)

admin.site.register(Review)





admin.site.site_header="Africana"
admin.site.site_title = "Africana Admin"


