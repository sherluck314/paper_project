from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import *
import markdown2
import re
from django.db.models.aggregates import Count


def clean_review(original_review):
    new_review = original_review.replace('#', '')
    new_review = new_review.replace('-', '')
    new_review = new_review.replace('*', '')
    return new_review


def change_formula(matched):
    formula = matched.group(0)
    formula = formula.replace('_', ' _')
    return '\n<p>' + formula + '</p>\n'


def index(request):
    topic_list = Topic.objects.all()
    tag_list = Tag.objects.annotate(paper_num=Count('paper')).order_by('-paper_num')
    return render(request, 'papers/index.html', context={'topic_list': topic_list, 'tag_list': tag_list})


def show(request):
    # 过滤数据，获取满足条件的paper
    # 注意filter只能写=，不能写不等于
    paper_list = Paper.objects.all()
    tag_list = Tag.objects.annotate(paper_num=Count('paper')).order_by('-paper_num')
    for paper in paper_list:
        review_length = len(paper.review)
        paper.small_review = clean_review(paper.review[0:min(review_length, 200)])
    return render(request, 'papers/show.html',
                  context={'paper_list': paper_list, 'tag_list': tag_list})


def detail(request, pk):
    # 不存在时返回404错误
    paper = get_object_or_404(Paper, pk=pk)
    # 判断是否已经登录
    if request.user.is_authenticated:
        # 上传用户或管理员可以见到编辑界面
        paper.if_updater = (paper.researcher == Researcher.objects.get(name=request.user) or request.user.is_superuser)
    else:
        paper.if_updater = True
    paper.review = markdown2.markdown(re.sub(r'\$\$(.+?)\$\$', change_formula, paper.review))
    return render(request, 'papers/detail.html', context={'paper': paper})


def filter_by_keyword(request, keyword, value):
    try:
        if keyword == '上传者':
            paper_list = Paper.objects.filter(researcher=Researcher.objects.get(name=value))
        elif keyword == '小组':
            paper_list = Paper.objects.filter(researcher=Researcher.objects.get(topic=Topic(value)))
        elif keyword == '标签':
            paper_list = Paper.objects.filter(tag=Tag.objects.get(name=value))
        else:
            return show(request)
        tag_list = Tag.objects.annotate(paper_num=Count('paper')).order_by('-paper_num')
        for paper in paper_list:
            review_length = len(paper.review)
            paper.small_review = clean_review(paper.review[0:min(review_length, 200)])
        return render(request, 'papers/show.html',
                      context={'paper_list': paper_list, 'tag_list': tag_list})
    except:
        return show(request)


def filter_by_keywords(request, keywords):
    try:
        if '&' in keywords:
            condition_key = '&'
        elif '|' in keywords:
            condition_key = '|'
        else:
            return show(request)
        select_tag_list = keywords.split(condition_key)
        if select_tag_list[-1] == '':
            select_tag_list = select_tag_list[:-1]
        if condition_key == '&':
            paper_list = Paper.objects.all()
            for select_tag in select_tag_list:
                paper_list = paper_list.filter(tag=Tag(name=select_tag))
        else:
            q = Q()
            q.connector = 'OR'
            for select_tag in select_tag_list:
                q.children.append(('tag', Tag(name=select_tag)))
            paper_list = Paper.objects.filter(q).distinct()
            print(paper_list, q)
        tag_list = Tag.objects.annotate(paper_num=Count('paper')).order_by('-paper_num')
        for paper in paper_list:
            review_length = len(paper.review)
            paper.small_review = clean_review(paper.review[0:min(review_length, 200)])
        return render(request, 'papers/show.html',
                      context={'paper_list': paper_list, 'tag_list': tag_list,
                               'select_tag_list': select_tag_list})
    except:
        return show(request)
