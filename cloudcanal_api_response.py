import json


def public_formater(response):
    try:
        if not response['success']:
            print(response['msg'])
            return False
        else:
            data = response
            return data
    except Exception as e:
        print('Response公共部分检查失败：')
        print(e)
        return False


def listclusters(response):
    """"查询集群列表
    将返回的数据，格式化为Dict
    """
    try:
        clusters_list = public_formater(response)
        if len(clusters_list) > 1:
            print('集群数量大于1，请确认！')
            return False
        return clusters_list[0]
    except Exception as e:
        print('查询集群列表失败：')
        print(e)
        return False


def listclusters(response):
    """"查询集群列表
    将返回的数据，格式化为Dict
    """
    try:
        clusters_list = public_formater(response)['data']
        if len(clusters_list) > 1:
            print('集群数量大于1，请确认！')
            return False
        return clusters_list[0]
    except Exception as e:
        print('查询集群列表失败：')
        print(e)
        return False


def listworkers(response):
    """
    查询机器列表 https://www.clougence.com/cc-doc/openCenter/openApi/clusterApi/api_cluster_listworkers
    :param response:
    :return: workers Dict
    """
    try:
        workers = public_formater(response)
        return workers
    except Exception as e:
        print('查询机器列表失败：')
        print(e)
        return False


def listdatasources(response):
    """
    查询数据源列表 https://www.clougence.com/cc-doc/openCenter/openApi/dataSourceApi/api_datasource_listds
    :param response:
    :return: ds Dict
    """
    try:
        datasources = public_formater(response)
        return datasources
    except Exception as e:
        print('查询数据源列表失败：')
        print(e)
        return False


def adddatasource(response):
    """添加数据源 https://www.clougence.com/cc-doc/openCenter/openApi/dataSourceApi/api_datasource_addds"""
    try:
        datasources = public_formater(response)
        return datasources
    except Exception as e:
        print('添加数据源列表失败：')
        print(e)
        return False


def deleteds(response):
    """删除数据源"""
    data = public_formater(response)
    return data


def listdatajobs(response):
    """列出所有的任务"""
    data = public_formater(response)
    return data


def create_datajob(response):
    """添加同步任务"""
    data = public_formater(response)
    return data


def delete_datajob(response):
    """删除同步任务"""
    data = public_formater(response)
    return data


def stop_datajob(response):
    """停止同步任务"""
    data = public_formater(response)
    return data


def query_datajob(response):
    """查询同步任务"""
    data = public_formater(response)
    return data


def start_datajob(response):
    """启动同步任务"""
    data = public_formater(response)
    return data


def restart_datajob(response):
    """重启同步任务"""
    data = public_formater(response)
    return data


def upsertuserconfigs(response):
    """
    没有相应的openapi,废弃
    修改告警URL"""
    data = public_formater(response)
    return data


def queryjobschemabyid(response):
    """
    查询数据任务元数据"""
    data = public_formater(response)
    return data


def updatetransferobject(response):
    """
    从同步任务中删除某些库"""
    data = public_formater(response)
    return data


def update_jobdesc(response):
    """
    修改任务描述"""
    data = public_formater(response)
    return data
