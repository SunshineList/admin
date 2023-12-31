# -*- coding: utf-8 -*-
"""
@desc     : 在此文件中定义任务调度函数, 系统会自动监测该文件内的方法
            ** 建议仅在本文件中定义简介函数, 具体实现逻辑放入warehouse中 **
"""
from drf_admin.apps.system.jobs.decorators import single_task


@single_task('database_backup')
def database_backup():
    """数据库备份"""
    pass


@single_task('project_data_reset')
def project_data_reset():
    """项目数据重置"""
    pass
