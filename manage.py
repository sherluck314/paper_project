#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
# python manage.py makemigrations
# 通过运行makemigrations命令，你告诉了Django你对模型文件做了些修改，修改的部分被储存为了一次迁移
# 迁移数据被储存在migrations/0001_initial.py中
# python manage.py migrate
# 自动执行数据库迁移并同步管理你的数据库结构
# python manage.py sqlmigrate papers 0001可以得到迁移对应的sql语句
# python manage.py check 检查项目中的问题
# 对models.py进行修改后无需删除migrations文件夹中之前的内容，它会平滑覆盖掉

# python manage.py createsuperuser 创建超级管理者

# 删除数据
# 第一步是把db.sqlite3和migrations下除了__init__的文件删除
# python manage.py dbshell
# .tables查看所有表
# drop table XXX;删除表
# select * from django_migrations;
# delete from django_migrations;
# .exit

# 使用命令行进行管理
# python manage.py shell