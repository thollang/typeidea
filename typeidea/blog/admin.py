from django.contrib import admin
from django.contrib.admin.models import LogEntry

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post, Category, Tag
from .adminforms import PostAdminForm


class PostInline(admin.TabularInline):
    fiels = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'owner', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'post count'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'owner', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = 'Catetory Filter'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]

    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    exclude = ('owner',)
    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('basic config', {
            'description': 'basic config description',
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('content', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('extra infomation', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        })
    )
    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">edit</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = 'edit'

    # class Media:
    #     css = {
    #         "all": ('https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.csss'),
    #     }
    #     js = ('https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.5.0/js/bootstrap.bundle.jss')


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id',
                    'action_flag', 'user', 'change_message']
