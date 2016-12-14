from django.contrib import admin
from userlogin.models import UserProfile, Message, Notice, Blog, BlogLike
# Import the UserProfile model with Category and Page.
# If you choose this option, you'll want to modify the import statement you've already got to include UserProfile.
from userlogin.models import UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Notice)
admin.site.register(Blog)
admin.site.register(BlogLike)
