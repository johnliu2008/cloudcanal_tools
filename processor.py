import json
import os
import re
import time
from datetime import datetime


import post
import config
import cloudcanal_api_request
import cloudcanal_api_response
import sqlite3_operations


def load_jsonc(path):
    """读取 JSON/JSONC 文件（支持 // 和 /* */ 注释），返回解析后的对象。"""
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'(?m)(?<!https:)(?<!http:)//.*$', '', text)
    return json.loads(text)


def load_schema_file(path):
    """读取用户提供的 schema/映射文件，不存在则返回 None（调用方决定是否用默认映射）。"""
    if not path:
        return None
    if not os.path.isfile(path):
        print("文件不存在：%s" % path)
        return False
    try:
        return load_jsonc(path)
    except Exception as e:
        print("解析文件失败 %s：%s" % (path, e))
        return False


def parse_db_names(db_names):
    """'db1,db2' -> ['db1', 'db2']，去空去重保序。"""
    seen = []
    for name in (db_names or "").split(","):
        name = name.strip()
        if name and name not in seen:
            seen.append(name)
    return seen


def listclusters(cc_num):
    api_path = config.API_list_clusters
    request_data = cloudcanal_api_request.listclusters()
    res = post.send_post_request_json(cc_num, api_path, request_data)
    clusters = cloudcanal_api_response.listclusters(res)
    print(clusters)
    return clusters


def listworkers(cc_num, cluster_id=2):
    """输出指定CC服务器的关键信息"""
    api_path = config.API_list_workers
    request_data = cloudcanal_api_request.listworkers(clusterId=cluster_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    workers = cloudcanal_api_response.listclusters(res)
    # for k, v in workers.items():
    #     print("%s, %s" % (k, v))
    cpuUseRatio = workers['cpuUseRatio']
    memUseRatio = workers['memUseRatio']
    physicMemMb = workers['physicMemMb']
    logicalCoreNum = workers['logicalCoreNum']
    memOverSoldPercent = workers['memOverSoldPercent']
    worker_summary = ("CC: {cc_num}, cpuUseRatio: {cpuUseRatio}, memUseRatio: {memUseRatio}, physicMemMb: {physicMemMb}, "
          "logicalCoreNum: {logicalCoreNum}, memOverSoldPercent: {memOverSoldPercent}"
          .format(cc_num=cc_num, cpuUseRatio=cpuUseRatio, memUseRatio=memUseRatio, physicMemMb=physicMemMb,
                  logicalCoreNum=logicalCoreNum, memOverSoldPercent=memOverSoldPercent))
    print(worker_summary)
    return worker_summary


def listdatasources(cc_num, dataSourceId=None, deployType=None, hostType=None, lifeCycleState=None, ds_type=None):
    """可以查询数据源，ds_type可以传StarRocks / AuroraMySQL"""
    api_path = config.API_list_datasources
    request_data = cloudcanal_api_request.listdatasources(dataSourceId=dataSourceId, deployType=deployType,
                                                          hostType=hostType, lifeCycleState=lifeCycleState, type=ds_type)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    datasources = cloudcanal_api_response.listdatasources(res)
    if datasources:
        for ds in datasources['data']:
            dsid = ds['id']
            deployType = ds['deployType']
            dataSourceType = ds['dataSourceType']
            privateHost = ds['privateHost']
            instanceDesc = ds['instanceDesc']
            print("datasource_id: %s, deployType: %s, dataSourceType: %s, privateHost: %s, instanceDesc: %s" % (
                dsid, deployType, dataSourceType, privateHost, instanceDesc
            ))
    return datasources


def adddatasource(cc_num, deployType="SELF_MAINTENANCE", region="", dataSourceType="", privateHost="",
                      publicHost="", hostType="", instanceDesc="", account="", password=""):
    """添加数据源"""
    if dataSourceType == 'StarRocks':
        deployType = 'SELF_MAINTENANCE'
    elif dataSourceType == 'AuroraMySQL':
        deployType = 'AWS_CLOUD_HOSTED'
    else:
        deployType = deployType
    api_path = config.API_add_datasources
    ds_info = cloudcanal_api_request.dataSourceAddData(deployType=deployType, region=region, dataSourceType=dataSourceType,
                                                       privateHost=privateHost, publicHost=publicHost, hostType=hostType,
                                                       instanceDesc=instanceDesc, account=account, password=password,
                                                       securityType='USER_PASSWD')
    request_data = cloudcanal_api_request.adddatasources(dataSourceAddData=ds_info)
    res = post.send_post_request_data(cc_num, api_path, request_data)
    ds = cloudcanal_api_response.adddatasource(res)
    if ds:
        print('添加数据源成功，数据源Id是%s   如果是RDS,请记得在console界面点击测试连接,以免创建同步任务时失败!' % ds['data'])
        return ds
    else:
        print('添加数据源失败')
        print(res)
        return False


def deletedatasource(cc_num, datasource_id):
    """删除数据源"""
    api_path = config.API_deleteds
    request_data = cloudcanal_api_request.deleteds(dataSourceId=datasource_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.deleteds(res)
    if data:
        print('删除数据源：%s 成功' % datasource_id)
        return data
    else:
        print('删除数据源：%s 失败！' % datasource_id)
        print(res)
        return False


def listdatajobs(cc_num, page_size=10, page_num=1):
    """列出同步任务（单页，可通过 page_size/page_num 翻页）"""
    print("CC地址:" + config.CC_endpoint_str.format(Number=cc_num))
    api_path = config.API_list_datajobs
    request_data = cloudcanal_api_request.listdatajobs(pageSize=page_size, pageNum=page_num)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.listdatajobs(res)
    if data['success']:
        print('dataJobId, dataJobDesc, dataJobType, sourceinstanceDesc, targetinstanceDesc')
        for job in data['data']:
            print('%s, %s, %s, %s, %s' %
                  (job['dataJobId'], job['dataJobDesc'].replace(',', ' '), job['dataJobType'], job['sourceDsVO']['privateHost'] if job['sourceDsVO']['hostType'] == 'PRIVATE' else job['sourceDsVO']['publicHost'],
                   job['targetDsVO']['privateHost'] if job['targetDsVO']['hostType'] == 'PRIVATE' else job['targetDsVO']['publicHost']))
        print("一共%s个任务\n" % len(data['data']))
        return data['data']
    else:
        print(data['msg'])


def create_datajob(cc_num, db_names, src_schema, dst_schema, mapping_def=None,
                   init_sync=False, specid=16, src_datasource_id=0, dst_datasource_id=0,
                   dest_name=""):
    """添加同步任务（schema 全部由调用方提供，见 examples/job_schema_example.jsonc）"""
    api_path = config.API_create_datajob
    src_host_type = listdatasources(cc_num=cc_num, dataSourceId=src_datasource_id)['data'][0]['hostType']
    dst_host_type = listdatasources(cc_num=cc_num, dataSourceId=dst_datasource_id)['data'][0]['hostType']
    if not datajob_precheckbasic(cc_num=cc_num, db_names=db_names, src_schema=src_schema,
                                 dst_schema=dst_schema, mapping_def=mapping_def,
                                 init_sync=init_sync, specid=specid,
                                 src_datasource_id=src_datasource_id,
                                 dst_datasource_id=dst_datasource_id,
                                 src_host_type=src_host_type,
                                 dst_host_type=dst_host_type,
                                 dest_name=dest_name):
        # 基础预检
        return False
    if not datajob_precheckdetail(cc_num=cc_num, db_names=db_names, src_schema=src_schema,
                                  dst_schema=dst_schema, mapping_def=mapping_def,
                                  init_sync=init_sync, specid=specid,
                                  src_datasource_id=src_datasource_id,
                                  dst_datasource_id=dst_datasource_id,
                                  src_host_type=src_host_type,
                                  dst_host_type=dst_host_type,
                                  dest_name=dest_name):
        # 详细预检
        return False

    # 创建任务
    request_data = cloudcanal_api_request.create_datajob(db_names=db_names, src_schema=src_schema,
                                                         dst_schema=dst_schema, mapping_def=mapping_def,
                                                         init_sync=init_sync, specid=specid,
                                                         src_datasource_id=src_datasource_id,
                                                         dst_datasource_id=dst_datasource_id,
                                                         srcHostType=src_host_type,
                                                         dstHostType=dst_host_type,
                                                         dest_name=dest_name)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.create_datajob(res)
    if data:
        print('创建同步任务 %s到%s 成功，任务ID是%s' % (db_names, dest_name, data['data']))
        return data
    else:
        print('创建同步任务 %s到%s 失败!' % (db_names, dest_name))
        if res['code'] == '0001':
            print('请确保RDS数据源已经在console界面点击过"测试连接"')
        print(res)
        return False


def datajob_precheckbasic(cc_num, db_names, src_schema, dst_schema, mapping_def=None,
                          init_sync=False, specid=16, src_datasource_id=0, dst_datasource_id=0,
                          dest_name="", src_host_type="", dst_host_type=""):
    """任务基础预检"""
    api_path = config.API_datajob_precheckbasic
    request_data = cloudcanal_api_request.create_datajob(db_names=db_names, src_schema=src_schema,
                                                         dst_schema=dst_schema, mapping_def=mapping_def,
                                                         init_sync=init_sync, specid=specid,
                                                         src_datasource_id=src_datasource_id,
                                                         dst_datasource_id=dst_datasource_id,
                                                         srcHostType=src_host_type,
                                                         dstHostType=dst_host_type,
                                                         dest_name=dest_name)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.create_datajob(res)
    if res['code'] == "1":
        print('任务基础预检 %s到%s 成功' % (db_names, dest_name))
        return data
    else:
        print('任务基础预检 %s到%s 失败!' % (db_names, dest_name))
        print(res)
        return False


def datajob_precheckdetail(cc_num, db_names, src_schema, dst_schema, mapping_def=None,
                           init_sync=False, specid=16, src_datasource_id=0, dst_datasource_id=0,
                           dest_name="", src_host_type="", dst_host_type=""):
    """任务详细预检"""
    api_path = config.API_datajob_precheckdetail
    request_data = cloudcanal_api_request.create_datajob(db_names=db_names, src_schema=src_schema,
                                                         dst_schema=dst_schema, mapping_def=mapping_def,
                                                         init_sync=init_sync, specid=specid,
                                                         src_datasource_id=src_datasource_id,
                                                         dst_datasource_id=dst_datasource_id,
                                                         srcHostType=src_host_type,
                                                         dstHostType=dst_host_type,
                                                         dest_name=dest_name)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.create_datajob(res)
    if res['code'] == "1":
        print('任务详细预检 %s到%s 成功' % (db_names, dest_name))
        return data
    else:
        print('任务详细预检 %s到%s 失败!' % (db_names, dest_name))
        print(res)
        return False


def delete_datajob(cc_num, datajob_id):
    api_path = config.API_delete_datajob
    request_data = cloudcanal_api_request.delete_datajob(datajob_id=datajob_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.delete_datajob(res)
    if data:
        print('删除同步任务 %s 成功' % datajob_id)
        return data
    else:
        print('删除同步任务 %s 失败!' % datajob_id)
        print(res)
        return False


def stop_datajob(cc_num, datajob_id):
    api_path = config.API_stop_datajob
    request_data = cloudcanal_api_request.stop_datajob(datajob_id=datajob_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.stop_datajob(res)
    if data:
        print('停止同步任务 %s 成功' % datajob_id)
        return data
    else:
        print('停止同步任务 %s 失败!' % datajob_id)
        print(res)
        return False


def query_datajob(cc_num, datajob_id):
    api_path = config.API_query_datajob
    request_data = cloudcanal_api_request.query_datajob(datajob_id=datajob_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.query_datajob(res)
    if data:
        # print(data)
        return data
    else:
        print('查询同步任务 %s 失败!' % datajob_id)
        print(res)
        return False


def start_datajob(cc_num, datajob_id):
    api_path = config.API_start_datajob
    request_data = cloudcanal_api_request.start_datajob(datajob_id=datajob_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.start_datajob(res)
    if data:
        print('启动同步任务 %s 成功' % datajob_id)
        return data
    else:
        print('启动同步任务 %s 失败!' % datajob_id)
        print(res)
        return False


def restart_datajob(cc_num, datajob_id):
    api_path = config.API_restart_datajob
    request_data = cloudcanal_api_request.restart_datajob(datajob_id=datajob_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.restart_datajob(res)
    if data:
        print('重启同步任务 %s 成功' % datajob_id)
        return data
    else:
        print('重启同步任务 %s 失败!' % datajob_id)
        print(res)
        return False


def upsertuserconfigs(cc_num, defaultImAlertUrl):
    """暂时只写了修改告警URL的功能"""
    api_path = config.API_upsertuserconfigs
    request_data = cloudcanal_api_request.upsertuserconfigs(defaultImAlertUrl=defaultImAlertUrl)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.upsertuserconfigs(res)
    if data:
        print('已成功将defaultImAlertUrl修改为 %s' % defaultImAlertUrl)


def queryjobschemabyid(cc_num, datajob_id):
    """
    查询数据任务元数据
    :param cc_num:
    :param datajob_id:
    :return: data
    """
    api_path = config.API_queryjobschemabyid
    request_data = cloudcanal_api_request.queryjobschemabyid(datajob_id=datajob_id)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.queryjobschemabyid(res)
    if data:
        print('查询数据任务元数据 %s 成功' % datajob_id)
        return data
    else:
        print('查询数据任务元数据 %s 失败!' % datajob_id)
        print(res)
        return False


def export_job_schema(cc_num, datajob_id, out_dir="."):
    """把线上任务的 schema 导出为 JSON 文件，可作为 create_datajob 的输入模板。"""
    metadata = queryjobschemabyid(cc_num=cc_num, datajob_id=datajob_id)
    if not metadata:
        return False
    os.makedirs(out_dir, exist_ok=True)
    outputs = {
        "source_schema.json": metadata['data'].get('sourceSchema', '[]'),
        "target_schema.json": metadata['data'].get('targetSchema', '[]'),
        "mapping_config.json": metadata['data'].get('mappingConfig', '[]'),
    }
    for filename, raw in outputs.items():
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            parsed = raw
        path = os.path.join(out_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print("已导出 %s" % path)
    return True


def update_jobdesc(cc_num, datajob_id, dataJobDesc):
    """
    修改任务描述
    :param cc_num:
    :param datajob_id:
    :param dataJobDesc:
    :return: data
    """
    api_path = config.API_update_jobdesc
    request_data = cloudcanal_api_request.update_jobdesc(datajob_id=datajob_id, dataJobDesc=dataJobDesc)
    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.update_jobdesc(res)
    if data:
        print('修改任务 %s 描述为 %s 成功' % (datajob_id, dataJobDesc))
        return data
    else:
        print('修改任务 %s 描述为 %s 失败!' % (datajob_id, dataJobDesc))
        print(res)
        return False


def _remove_dbs_from_schema(db_list, db_names):
    """从 schema 列表中移除 db 名在 db_names 中的条目，返回过滤后的新列表。"""
    return [item for item in db_list if item.get("db") not in db_names]


def _mapping_value_refs_db(raw, db_names):
    """serializeMapping 的键或值是否为 {"value": <待删库名>}。"""
    try:
        parsed = json.loads(raw)
    except Exception:
        return False
    return isinstance(parsed, dict) and parsed.get("value") in db_names


def _remove_dbs_from_mapping(mapping_config, db_names):
    """从 mappingConfig 的 serializeMapping 中移除与待删库相关的键值对（键或值指向待删库即删）。"""
    db_set = set(db_names)
    for item in mapping_config:
        serialize_mapping = item.get("serializeMapping", {})
        keys_to_delete = [key for key, value in serialize_mapping.items()
                          if _mapping_value_refs_db(key, db_set) or _mapping_value_refs_db(value, db_set)]
        for key in keys_to_delete:
            del serialize_mapping[key]
    return mapping_config


def delete_db_from_job(cc_num, datajob_id, db_names_deleted):
    """
    从同步任务中删除某些库,并更新任务描述
    :param cc_num:
    :param datajob_id:
    :param db_names_deleted: 数据库名，多个用英文逗号分隔，如 db1,db2
    :return:
    """
    try:
        db_names = parse_db_names(db_names_deleted)
        if not db_names:
            print("待删除的库名为空")
            return False
        metadata = queryjobschemabyid(cc_num=cc_num, datajob_id=datajob_id)
        sourceSchema = json.loads(metadata['data']['sourceSchema'])
        before = len(sourceSchema)
        sourceSchema = _remove_dbs_from_schema(sourceSchema, db_names)
        if len(sourceSchema) == before:
            print("此任务中未包含%s" % db_names_deleted)
            return False

        if len(sourceSchema) == 0:
            # 删除这些库后源端为空，说明这个任务可以直接删除了，不需要update了
            return stop_and_delete_datajob(cc_num=cc_num, datajob_id=datajob_id)

        targetSchema = json.loads(metadata['data']['targetSchema'])
        targetSchema = _remove_dbs_from_schema(targetSchema, db_names)
        mappingConfig = json.loads(metadata['data']['mappingConfig'])
        mappingConfig = _remove_dbs_from_mapping(mappingConfig, db_names)

        api_path = config.API_updatetransferobject
        request_data = cloudcanal_api_request.updatetransferobject(datajob_id=datajob_id,
                                                                   srcSchemaWithoutAdd=sourceSchema,
                                                                   dstSchemaWithoutAdd=targetSchema,
                                                                   mappingConfigWithoutAdd=mappingConfig,
                                                                   initialSync=False)
        res = post.send_post_request_json(cc_num, api_path, request_data)
        update_job_result = cloudcanal_api_response.updatetransferobject(res)
        if update_job_result['success']:
            print("从同步任务中删除%s 成功" % db_names_deleted)
            dataJobDesc = query_datajob(cc_num=cc_num, datajob_id=datajob_id)['data']['dataJobDesc']  # 查询任务描述
            new_desc = dataJobDesc
            for db in db_names:
                new_desc = new_desc.replace(db, '')
            update_desc_result = update_jobdesc(cc_num=cc_num, datajob_id=datajob_id,
                                                dataJobDesc=new_desc)  # 修改描述
            if update_desc_result:
                print("修改任务描述为 %s 成功" % new_desc)
                return True
            else:
                print("修改任务描述为 %s 失败!" % new_desc)
                return False
        else:
            print("从同步任务中删除%s 失败!" % db_names_deleted)
            print(update_job_result)
            return False
    except Exception as e:
        print("从同步任务中删除某些库，发生未知错误：")
        print(e)
        return False


def stop_and_delete_datajob(cc_num, datajob_id):
    # 从这里删除任务之后,不会更新sqlite3中的任务列表
    stop_datajob(cc_num=cc_num, datajob_id=datajob_id)
    max_retries = 20
    for attempt in range(max_retries):
        try:
            data = query_datajob(cc_num=cc_num, datajob_id=datajob_id)
            dataJobDesc = data['data']['dataJobDesc']
            dataTaskStatus = data['data']['dataTasks'][-1]['dataTaskStatus']
            #  说明是已经停止状态，可以删除 https://www.clougence.com/cc-doc/openCenter/openApi/constApi/api_constant_listdatataskstatuses
            if dataTaskStatus == 'STOP':
                print(f"该任务的dataTaskStatus属性是 {dataTaskStatus}，现在开始删除任务： {dataJobDesc} ...")
                return delete_datajob(cc_num=cc_num, datajob_id=datajob_id)
            else:
                print(f"该任务的dataTaskStatus属性是 {dataTaskStatus}，还不能删除，3秒后重试...")
                if attempt % 10 == 0:
                    stop_datajob(cc_num=cc_num, datajob_id=datajob_id)
                time.sleep(3)
        except ValueError as e:
            if attempt == max_retries - 1:
                print("达到最大重试次数，退出。")
                return False



def insert_sqlite3_cloudcanal_jobs():
    "遍历所有的CC服务器，将查询出来的任务列表，保存到SQLite3中"
    sqlite3_operations.drop_table()
    sqlite3_operations.create_table()
    for cc_num in config.CC_server_nums:
        datajobs = listdatajobs(cc_num)
        for job in datajobs:
            job_id = job['dataJobId']
            job_desc = job['dataJobDesc']
            source_host = job['sourceDsVO']['privateHost'] if job['sourceDsVO']['privateHost'] else job['sourceDsVO']['publicHost']
            target_host = job['targetDsVO']['privateHost'] if job['targetDsVO']['privateHost'] else job['targetDsVO']['publicHost']
            updated_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            sqlite3_operations.insert_records((job_desc, cc_num, job_id, source_host, target_host, updated_time))


def find_db_in_sqlite3(db_name):
    "到SQLite3中查询与db_name相关的同步任务"
    ret2 = sqlite3_operations.select_records(conditions=f"job_desc like '%{db_name}%'")
    if ret2 == []:
        print("未找到，请重新确认")
        return ret2
    print(
        "id | job_desc | cc_num | job_id | source_host              |            target_host              |            updated_time")
    for j in ret2:
        id = j[0]
        job_desc = j[1]
        cc_num = j[2]
        job_id = j[3]
        source_host = j[4]
        target_host = j[5]
        updated_time = j[6]
        print(f"{id} | {job_desc} | {cc_num} | {job_id} | {source_host} | {target_host} | {updated_time}")
    return ret2


def sqlite3_data_is_updated_today():
    "查询出SQLite3中最后一条数据，判断它的更新时间是否大于今天0点"
    def is_updated_today(updated_time):
        date_obj = datetime.strptime(updated_time, '%Y-%m-%d %H:%M:%S')
        u_timestamp = date_obj.timestamp()
        # 获取今天的0点时间戳
        # 首先获取今天的日期
        today = datetime.now().date()
        # 然后将今天的日期与0时0分0秒的时间结合
        midnight_today = datetime.combine(today, datetime.min.time())
        # 将datetime对象转换为时间戳
        timestamp_midnight_today = midnight_today.timestamp()
        # 比较文件最后修改时间戳与今天0点时间戳
        return u_timestamp > timestamp_midnight_today

    ret = sqlite3_operations.select_records(orderby="order by updated_time desc limit 1")
    if ret == []:
        return False
    if ret is False:
        return False
    return is_updated_today(ret[0][6])


def one_key_delete_db(db_name):
    "一键删库函数，快速找到该库对应的CC任务，从该任务中剔除或删除该任务"
    if sqlite3_data_is_updated_today() is False:
        # 如果更新时间早于今日0点，则删掉重新插入数据
        insert_sqlite3_cloudcanal_jobs()

    ret2 = find_db_in_sqlite3(db_name=db_name)
    if not ret2:
        print("查询任务数据库时出错！")
        return False
    if len(ret2) > 1:
        print(f"查询到{len(ret2)}个与 {db_name} 相关的任务，需要人工介入")
        return False

    id = ret2[0][0]
    job_desc = ret2[0][1]
    cc_num = ret2[0][2]
    job_id = ret2[0][3]
    if delete_db_from_job(cc_num=cc_num, datajob_id=job_id, db_names_deleted=db_name):
        sqlite3_operations.update_records(id, job_desc.replace(db_name, ''))


def list_all_jobs_in_sqlite3():
    "到SQLite3中查询所有同步任务"
    ret2 = sqlite3_operations.select_records(orderby=f"order by source_host,target_host")
    if ret2 == []:
        print("未找到，请重新确认")
        return ret2
    print(
        "id | job_desc | cc_num | job_id | source_host              |            target_host              |            updated_time")
    for j in ret2:
        id = j[0]
        job_desc = j[1]
        cc_num = j[2]
        job_id = j[3]
        source_host = j[4]
        target_host = j[5]
        updated_time = j[6]
        print(f"{id} | {job_desc.replace('|', ',')} | {cc_num} | {job_id} | {source_host} | {target_host} | {updated_time}")
    return ret2


def create_datajob_migration(cc_num, db_names, src_schema, dst_schema, mapping_def=None,
                             init_sync=False, specid=16, src_datasource_id=0,
                             dst_datasource_id=0, dest_name=""):
    """创建 MIGRATION 类型任务（schema 全部由调用方提供）"""
    api_path = config.API_create_datajob
    request_data = cloudcanal_api_request.create_datajob_migration(
        db_names=db_names,
        src_schema=src_schema,
        dst_schema=dst_schema,
        mapping_def=mapping_def,
        init_sync=init_sync,
        specid=specid,
        src_datasource_id=src_datasource_id,
        dst_datasource_id=dst_datasource_id,
        dest_name=dest_name
    )
    if not request_data:
        print("生成请求参数失败")
        return False

    res = post.send_post_request_json(cc_num, api_path, request_data)
    data = cloudcanal_api_response.create_datajob(res)
    if data:
        print(f'创建 MIGRATION 任务 {db_names} 成功，任务ID是 {data["data"]}')
        return data
    else:
        print(f'创建 MIGRATION 任务 {db_names} 失败!')
        if res['code'] == '0001':
            print('请确保RDS数据源已经在console界面点击过"测试连接"')
        print(res)
        return False
