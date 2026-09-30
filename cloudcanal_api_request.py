
import json


def listclusters():
    # 集群列表
    params_dict = {"searchType": "clusterName", "cloudOrIdcName": None, "clusterNameLike": None, "clusterDescLike": None}
    return params_dict


def listworkers(clusterId):
    # 机器列表
    params_dict = {"clusterId": clusterId, "sourceInstanceId": None, "targetInstanceId": None}
    return params_dict


def listdatasources(dataSourceId=None, deployType=None, hostType=None, lifeCycleState=None, type=None):
    # 数据源列表
    params_dict = {"dataSourceId": dataSourceId, "deployType": deployType, "hostType": hostType,
                   "lifeCycleState": lifeCycleState, "type": type}
    return params_dict


def adddatasources(dataSourceAddData, securityFile=None, secretFile=None):
    # 添加数据源
    params_dict = {"dataSourceAddData": dataSourceAddData, "securityFile": securityFile, "secretFile": secretFile}
    return params_dict


def dataSourceAddData(deployType="SELF_MAINTENANCE", region="", dataSourceType="", privateHost="",
                      publicHost="", hostType="", instanceDesc="", account="", password="", securityType='USER_PASSWD'):
    """添加数据源时的必要信息 https://www.clougence.com/cc-doc/openCenter/openApi/dataSourceApi/api_datasource_addds"""
    try:
        dataSourceAddData = {'deployType': deployType, 'region': region,
                             'type': dataSourceType, 'privateHost': privateHost,
                             'publicHost': publicHost, 'hostType': hostType, 'instanceDesc': instanceDesc,
                             'account': account, 'password': password, 'securityType': securityType,
                             "host": privateHost if privateHost != "" else publicHost}
        if dataSourceType == 'StarRocks':
            dataSourceAddData["dsKvConfigs"] = [{"configName": "publicHttpHost", "configValue": ""},
                                {"configName": "privateHttpHost", "configValue": privateHost.replace("9030", "8030")}]
            dataSourceAddData["extraData"] = {"hdfsPort": "8020", "hdfsDwDir": "/user/hive/warehouse"}
        return json.dumps(dataSourceAddData)
    except Exception as e:
        print("添加数据源操作的参数处理，发生未知错误：")
        print(e)
        return False


def deleteds(dataSourceId):
    """删除数据源 https://www.clougence.com/cc-doc/openCenter/openApi/dataSourceApi/api_datasource_deleteds"""
    try:
        return {"dataSourceId": dataSourceId}
    except Exception as e:
        print("删除数据源操作的参数处理，发生未知错误：")
        print(e)
        return False


def listdatajobs(pageSize=10, pageNum=1):
    """列出任务（注意：只返回单页，按需翻页查询）"""
    params_dict = {"timeRange": [], "dataJobName": None, "dataJobType": None, "desc": None, "status": None, "type": None,
                   "sourceType": None, "sinkType": None, "sourceName": None, "sinkName": None, "sourceInstanceId": 0,
                   "targetInstanceId": 0, "transferObjName": None, "dataJobId": None, "orderType": "GMT_CREATE",
                   "pageSize": pageSize, "pageNum": pageNum}
    return params_dict


def default_mapping_def():
    """默认映射：库->库、表->表、列->列全部镜像，由调用方按需改写。"""
    return [{'method': 'DB_DB', 'serializeMapping': {}, 'serializeAutoGenRules': {}, 'commonGenRule': 'MIRROR'},
            {'serializeMapping': {}, 'method': 'TABLE_TABLE', 'serializeAutoGenRules': {}, 'commonGenRule': 'MIRROR'},
            {'method': 'COLUMN_COLUMN', 'serializeMapping': {}, 'serializeAutoGenRules': {}, 'commonGenRule': 'MIRROR'}]


def create_datajob_param():
    """SYNC 类型任务的参数模板（通用字段，业务无关）"""
    return {
        "jobType": "SYNC",
        "initialSync": True,
        "shortTermSync": False,
        "shortTermNum": 0,
        "oraIncrMode": "redo",
        "oraBuildRedoDicWhenCreate": True,
        "structMigration": False,
        "dataJobDesc": "",
        "checkOnce": False,
        "checkPeriod": False,
        "fullPeriod": False,
        "sourceCaseSensitive": True,
        "targetCaseSensitive": True,
        "enableAutoIncrement": True,
        "commonRule": "",
        "autoStart": True,
        "clusterId": 1,
        "specId": 16,
        "srcDsId": "11",
        "srcHostType": "PRIVATE",
        "dstDsId": "16",
        "dstHostType": "PRIVATE",
        "globalTimeZone": "+08:00",
        "srcRocketMqGroupId": "",
        "srcRabbitMqVhost": "cloudcanal",
        "srcRabbitExchange": "",
        "dstRabbitMqVhost": "cloudcanal",
        "dstRabbitExchange": "",
        "kafkaConsumerGroupId": "",
        "srcDsCharset": "utf8mb4",
        "tarDsCharset": "utf8",
        "srcSchemaLessFormat": "CLOUDCANAL_JSON_FOR_MQ",
        "originDecodeMsgFormat": None,
        "dstSchemaLessFormat": "CLOUDCANAL_JSON_FOR_MQ",
        "schemaWhiteListLevel": None,
        "dstMqDefaultTopic": None,
        "dstMqDefaultTopicPartitions": None,
        "dstMqDdlTopic": None,
        "dstMqDdlTopicPartitions": None,
        "dstCkTableEngine": None,
        "dstSrOrDorisTableModel": "PRIMARY_KEY",
        "targetTimeDefaultStrategy": None,
        "keyConflictStrategy": None,
        "filterDDL": True,
        "cleanTargetBeforeFull": False,
        "kuduNumReplicas": "",
        "kuduNumBuckets": "",
        "pkgDescription": "",
        "srcSchema": "",
        "dstSchema": "",
        "mappingDef": "",
        "processorConfigList": [
        ],
        "migrationBucketNumber": 4,
        "migrationPropertiesConfig": "PROPERTIES(\"replication_num\" = \"1\")",
        "obTenant": "sys",
        "dataCheckType": None,
        "dataReviseType": None,
        "reSchemaMigration": False
    }


def create_migration_job_param():
    """MIGRATION 类型任务的参数模板（通用字段，业务无关）"""
    return {
        "jobName": "",
        "jobType": "MIGRATION",
        "initialSync": False,
        "shortTermSync": False,
        "shortTermNum": 0,
        "oraIncrMode": "redo",
        "oraBuildRedoDicWhenCreate": True,
        "sourceHost": "",
        "sinkHost": "",
        "structMigration": False,
        "dataJobDesc": "",
        "checkOnce": False,
        "checkPeriod": False,
        "fullPeriod": False,
        "sourceCaseSensitive": True,
        "targetCaseSensitive": True,
        "commonRule": "",
        "autoStart": True,
        "clusterId": 1,
        "specId": 16,
        "srcDsId": "11",
        "srcHostType": "PRIVATE",
        "dstDsId": "16",
        "dstHostType": "PRIVATE",
        "globalTimeZone": "+08:00",
        "srcRocketMqGroupId": "",
        "srcRabbitMqVhost": "cloudcanal",
        "srcRabbitExchange": "",
        "dstRabbitMqVhost": "cloudcanal",
        "dstRabbitExchange": "",
        "kafkaConsumerGroupId": "",
        "srcDsCharset": "utf8",
        "tarDsCharset": "utf8",
        "srcSchemaLessFormat": "CLOUDCANAL_JSON_FOR_MQ",
        "originDecodeMsgFormat": None,
        "dstSchemaLessFormat": "CLOUDCANAL_JSON_FOR_MQ",
        "schemaWhiteListLevel": None,
        "dstMqDefaultTopic": None,
        "dstMqDefaultTopicPartitions": None,
        "dstMqDdlTopic": None,
        "dstMqDdlTopicPartitions": None,
        "dstCkTableEngine": None,
        "dstSrOrDorisTableModel": "PRIMARY_KEY",
        "targetTimeDefaultStrategy": "IS_NULL",
        "keyConflictStrategy": "IGNORE",
        "filterDDL": False,
        "cleanTargetBeforeFull": False,
        "kuduNumReplicas": "",
        "kuduNumBuckets": "",
        "pkgDescription": "",
        "srcSchema": "",
        "dstSchema": "",
        "mappingDef": "",
        "processorConfigList": [],
        "syncPartitionInfo": True,
        "migrationBucketNumber": "4",
        "migrationPropertiesConfig": "PROPERTIES(\"replication_num\" = \"1\")",
        "obTenant": "sys",
        "dataCheckType": None,
        "dataReviseType": None,
        "reSchemaMigration": False,
        "srcPulsarTenant": "",
        "srcPulsarNamespace": "",
        "dstPulsarTenant": "",
        "dstPulsarNamespace": "",
        "pushDownEnabled": False,
        "cgTableType": "BASE_TABLE"
    }


def create_datajob(db_names, src_schema, dst_schema, mapping_def=None,
                   init_sync=False, specid=16, src_datasource_id="0", srcHostType='PRIVATE',
                   dst_datasource_id="0", dstHostType='PRIVATE', dest_name=""):
    """
    构建 SYNC 类型任务的请求参数。
    :param db_names: 数据库名，若有多个则用英文逗号分隔，如 db1,db2（仅用于任务描述）
    :param src_schema: 源端 schema 列表（list[dict]，见 examples/job_schema_example.jsonc）
    :param dst_schema: 目标端 schema 列表（list[dict]）
    :param mapping_def: 映射定义列表，不传则使用默认 MIRROR 映射
    :param init_sync: 是否同步全量数据
    :param specid: 规格ID，参考https://www.clougence.com/cc-doc/reference/service_difference#%E4%BB%BB%E5%8A%A1%E8%A7%84%E6%A0%BC
    :param src_datasource_id: 源数据源的数字编号
    :param dst_datasource_id: 目标数据源的数字编号
    :return: 转换为json格式的params，可以用来提交请求
    """
    try:
        if mapping_def is None:
            mapping_def = default_mapping_def()
        params = create_datajob_param()
        params["dataJobDesc"] = "%s到%s" % (db_names, dest_name)
        params["specId"] = specid
        params["srcDsId"] = src_datasource_id
        params["srcHostType"] = srcHostType
        params["dstDsId"] = dst_datasource_id
        params["clusterId"] = 1
        params["dstHostType"] = dstHostType
        params["initialSync"] = init_sync
        params["srcSchema"] = json.dumps(src_schema).replace(' ', '')  # 去除空格很重要
        params["dstSchema"] = json.dumps(dst_schema).replace(' ', '')  # 去除空格很重要
        params["mappingDef"] = json.dumps(mapping_def).replace(' ', '')  # 去除空格很重要
        return params
    except Exception as e:
        print("生成创建任务参数时失败：")
        print(e)
        return False


def delete_datajob(datajob_id):
    try:
        return {"jobId": datajob_id, "verifyCode": None}
    except Exception as e:
        print("删除同步任务操作的参数处理，发生未知错误：")
        print(e)
        return False


def stop_datajob(datajob_id):
    try:
        return {"jobId": datajob_id, "dataJobName": None}
    except Exception as e:
        print("停止同步任务操作的参数处理，发生未知错误：")
        print(e)
        return False


def query_datajob(datajob_id):
    """https://www.clougence.com/cc-doc/openCenter/openApi/dataTaskApi/api_datajob_query"""
    try:
        return {"jobId": datajob_id}
    except Exception as e:
        print("查询同步任务详情的参数处理，发生未知错误：")
        print(e)
        return False


def start_datajob(datajob_id):
    """https://www.clougence.com/cc-doc/openCenter/openApi/dataTaskApi/api_datajob_start"""
    try:
        return {"jobId": datajob_id}
    except Exception as e:
        print("启动同步任务详情的参数处理，发生未知错误：")
        print(e)
        return False


def restart_datajob(datajob_id):
    """https://www.clougence.com/cc-doc/openCenter/openApi/dataTaskApi/api_datajob_restart"""
    try:
        return {"jobId": datajob_id}
    except Exception as e:
        print("重启同步任务详情的参数处理，发生未知错误：")
        print(e)
        return False


def upsertuserconfigs(defaultImAlertUrl):
    """
    没有相应的openapi,废弃
    暂时只写了修改告警URL的功能"""
    try:
        return {"updateConfigs": {"defaultImAlertUrl": defaultImAlertUrl}, "needCreateConfigs": {}}
    except Exception as e:
        print("重修改告警URL的参数处理，发生未知错误：")
        print(e)
        return False


def queryjobschemabyid(datajob_id):
    """
    https://www.clougence.com/cc-doc/openCenter/openApi/dataTaskApi/api_datajob_queryjobschema
    :param datajob_id:
    :return: {"jobId": datajob_id}
    """
    try:
        return {"jobId": datajob_id}
    except Exception as e:
        print("查询数据任务元数据的参数处理，发生未知错误：")
        print(e)
        return False


def updatetransferobject(datajob_id, srcSchemaWithoutAdd, dstSchemaWithoutAdd, mappingConfigWithoutAdd, initialSync=False):
    """从同步任务中删除某些库 https://www.clougence.com/cc-doc/openCenter/openApi/dataTaskApi/api_datajob_updatetransferobjnew"""
    try:
        params = {
            "dataJobId": datajob_id,
            "structMigration": False,
            "addMappingConfig": "[{\"method\":\"DB_DB\",\"serializeMapping\":{},\"serializeAutoGenRules\":{},\"commonGenRule\":\"MIRROR\"},{\"serializeMapping\":{},\"method\":\"TABLE_TABLE\",\"serializeAutoGenRules\":{},\"commonGenRule\":\"MIRROR\"},{\"method\":\"COLUMN_COLUMN\",\"serializeMapping\":{},\"serializeAutoGenRules\":{},\"commonGenRule\":\"MIRROR\"}]",
            "sourceAddConfig": None,
            "targetAddConfig": "[]",
            "initialSync": initialSync,
            "mappingConfigWithoutAdd": "",
            "srcSchemaWithoutAdd": "",
            "dstSchemaWithoutAdd": "",
            "reduceConfig": None,
            "addProcessorConfs": [

            ],
            "processorConfsWithoutAdd": [

            ]
        }
        params["srcSchemaWithoutAdd"] = json.dumps(srcSchemaWithoutAdd).replace(' ', '')  # 去除空格很重要
        params["dstSchemaWithoutAdd"] = json.dumps(dstSchemaWithoutAdd).replace(' ', '')  # 去除空格很重要
        params["mappingConfigWithoutAdd"] = json.dumps(mappingConfigWithoutAdd).replace(' ', '')  # 去除空格很重要
        return params
    except Exception as e:
        print("从同步任务中删除某些库，发生未知错误：")
        print(e)
        return False


def update_jobdesc(datajob_id, dataJobDesc):
    """
    https://www.clougence.com/cc-doc/openCenter/openApi/dataTaskApi/api_datajob_updatedesc
    :param datajob_id:
    :return: {"jobId": datajob_id}
    """
    try:
        return {"jobId": datajob_id, "dataJobDesc": dataJobDesc}
    except Exception as e:
        print("修改任务描述，发生未知错误：")
        print(e)
        return False


def create_datajob_migration(db_names, src_schema, dst_schema, mapping_def=None,
                             init_sync=False, specid=16, src_datasource_id="0",
                             srcHostType='PRIVATE', dst_datasource_id="0", dstHostType='PRIVATE',
                             dest_name=""):
    """
    创建 MIGRATION 类型任务（schema 全部由调用方提供，见 examples/job_schema_example.jsonc）。
    :param db_names: 数据库名，若有多个则用英文逗号分隔（仅用于任务描述）
    """
    try:
        if mapping_def is None:
            mapping_def = default_mapping_def()
        params = create_migration_job_param()
        params["jobName"] = "%s_migrate" % db_names
        params["dataJobDesc"] = "%s到%s" % (db_names, dest_name)
        params["specId"] = specid
        params["srcDsId"] = str(src_datasource_id)
        params["srcHostType"] = srcHostType
        params["dstDsId"] = str(dst_datasource_id)
        params["dstHostType"] = dstHostType
        params["initialSync"] = init_sync
        params["structMigration"] = False

        params["srcSchema"] = json.dumps(src_schema).replace(' ', '')  # 去除空格很重要
        params["dstSchema"] = json.dumps(dst_schema).replace(' ', '')  # 去除空格很重要
        params["mappingDef"] = json.dumps(mapping_def).replace(' ', '')

        return params
    except Exception as e:
        print("生成 MIGRATION 任务参数时失败：")
        print(e)
        return False
