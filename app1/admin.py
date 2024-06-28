from django.contrib import admin

# Register your models here.

from . models import Product
from . models import Flag
from . models import complete
from . models import Board
from . models import Flags
from . models import Answer
from . models import Attempt
from . models import Scene

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description','created_at')

class FlagAdmin(admin.ModelAdmin):
    list_display = ('id','q1','h1','f1','score')

class completeAdmin(admin.ModelAdmin):
    list_display = ('id','user','hint','completed','finished_at')

class BoardAdmin(admin.ModelAdmin):
    list_display = ('id','user','score','finished_at')

class FlagsAdmin(admin.ModelAdmin):
    list_display = ('id','quest','h1','image','f1','score')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id','user','flag','answer')

class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id','user','flag','attempt')

class SceneAdmin(admin.ModelAdmin):
    list_display = ('id','user','hecker')

admin.site.register(Product,ProductAdmin)
admin.site.register(Flag,FlagAdmin)
admin.site.register(complete,completeAdmin)
admin.site.register(Board,BoardAdmin)
admin.site.register(Flags,FlagsAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Attempt,AttemptAdmin)
admin.site.register(Scene,SceneAdmin)