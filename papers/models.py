from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField("研究主题", max_length=10, primary_key=True, blank=False)

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("论文标签", max_length=10, primary_key=True, blank=False)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Researcher(models.Model):
    name = models.CharField("姓名", max_length=10, primary_key=True, blank=False)
    # topic = models.CharField("研究主题", max_length=50, blank=False)
    topic = models.ForeignKey(Topic, verbose_name="研究主题",
                                   null=True,
                                   on_delete=models.SET_NULL, blank=False)

    class Meta:
        verbose_name = '上传者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Paper(models.Model):
    title = models.CharField("论文题目", max_length=200, blank=False)
    researcher = models.ForeignKey(Researcher, verbose_name="上传人",
                                   null=True,
                                   on_delete=models.SET_NULL, blank=False)
    # tag = models.CharField("具体标签", max_length=50, blank=False)
    tag = models.ManyToManyField(Tag, verbose_name="论文标签", blank=False)
    review = models.TextField("论文总结", blank=False)

    class Meta:
        verbose_name = '论文'
        verbose_name_plural = verbose_name
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('papers:detail', kwargs={'pk': self.pk})