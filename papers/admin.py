from django.contrib import admin
from django.forms import widgets
from django.db import models
from .models import Tag
from .models import Topic
from .models import Paper
from .models import Researcher
from django.forms import Textarea
from django.contrib.auth.models import User, Group
# Register your models here.
admin.site.register(Tag)
admin.site.register(Topic)


class PaperAdmin(admin.ModelAdmin):
    # 设置查看时的展示信息
    list_display = ['title', 'researcher']
    # 设置上传时的待填表单
    fields = ['title', 'tag', 'review']
    # 设置多选框
    filter_horizontal = ['tag']
    formfield_overrides = {
        models.CharField: {'widget': widgets.TextInput(attrs={"style": "width:50%;", "placeholder": "请输入内容"})},
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 300})}
    }

    def save_model(self, request, obj, form, change):
        # 重写保存模型的方法，按登陆用户自动填充上传人
        obj.researcher = Researcher.objects.get(name=request.user)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PaperAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(researcher=Researcher.objects.get(name=request.user))
        super().get_queryset(self, request)


class ResearcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic']

    def save_model(self, request, obj, form, change):
        # 重写保存模型的方法，新增用户时同时会注册，同时会给默认权限以及添加到组里
        if len(User.objects.filter(username=obj.name)) == 0:
            user = User.objects.create_user(username=obj.name, email='', password='inplusml')
            user.is_staff = True
            user.groups.add(Group.objects.get(name="user"))
            user.save()
        # 批量建立用户
        # rs = Researcher.objects.all()
        # for r in rs:
        #     if len(User.objects.filter(username=r.name)) == 0:
        #         print(r.name)
        #         user = User.objects.create_user(username=r.name, email='', password='inplusml')
        #         user.is_staff = True
        #         user.groups.add(Group.objects.get(name="user"))
        #         user.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        User.objects.get(username=obj.name).delete()
        super().delete_model(request, obj)


admin.site.register(Paper, PaperAdmin)
admin.site.register(Researcher, ResearcherAdmin)
admin.site.site_header = '论文管理'
admin.site.site_title = '论文后台管理'

