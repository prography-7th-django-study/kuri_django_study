from django.contrib import admin
# from .models import User, Book, LargeCategory, MediumCategory, SmallCategory
from .models import Book, SmallCategory
# from .models import User
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

from mptt.admin import DraggableMPTTAdmin

class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 10

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)



admin.site.register(SmallCategory, CustomMPTTModelAdmin)


# @admin.register(LargeCategory)
# class LargeCategoryAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(MediumCategory)
# class MediumCategoryAdmin(admin.ModelAdmin):
#     pass


# @admin.register(SmallCategory)
# class SmallCategoryInline(admin.ModelAdmin):
#     pass

# @admin.register(SmallCategory)
# class RelationshipInline(admin.StackedInline):
#     model = SmallCategory
#     extra = 1
#
#
# class QuestionInline(admin.TabularInline): # admin.StackedInline
#     model = SmallCategory
#     extra = 0
#     fields = ('top',)
#     # ordering = ['position',]
#
#     def queryset(self, request):
#         return super(QuestionInline, self).queryset(request).select_related('category')
#
#
#
# class MessageAdmin(admin.ModelAdmin):
#     inlines = (QuestionInline,)
#     search_fields = ['category']
#
# admin.site.register(SmallCategory, MessageAdmin)


##django-mptt

# class FirstModelAdmin(admin.ModelAdmin):
#   inlines = [SecondModelInline]


# class LageCategoryAdmin(admin.ModelAdmin):
#     inlines = [
#         MediumCategoryAdmin,
#     ]

# @admin.register(SmallCategory)
# class SmallCategoryAdmin(admin.ModelAdmin):
#     pass