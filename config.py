"""通用配置：所有敏感信息通过环境变量注入，开箱即用的只是占位符。

环境变量：
  CC_ACCESS_KEY_ID / CC_SECRET_KEY : CloudCanal OpenAPI 认证凭据
  CC_ENDPOINT_TEMPLATE             : 形如 http://host:8111，或带 {Number} 占位的多实例模板
  CC_SERVER_NUMS                   : 逗号分隔的实例编号，如 01,02
"""
import os


def _env_list(name, default):
    raw = os.environ.get(name, "")
    if not raw.strip():
        return default
    return tuple(s.strip() for s in raw.split(",") if s.strip())


CC_server_nums = _env_list("CC_SERVER_NUMS", ("01",))
CC_AccessKeyId = os.environ.get("CC_ACCESS_KEY_ID", "YOUR_ACCESS_KEY_ID")
CC_secret_key = os.environ.get("CC_SECRET_KEY", "YOUR_SECRET_KEY")
# 单实例直接写 http://host:8111；多实例可用 {Number} 占位，如 http://cc-{Number}.example.com:8111
CC_endpoint_str = os.environ.get("CC_ENDPOINT_TEMPLATE", "http://127.0.0.1:8111")

# 以下是常用API的列表
API_list_clusters = "/cloudcanal/console/api/v1/openapi/cluster/listclusters"
API_list_workers = "/cloudcanal/console/api/v1/openapi/worker/listworkers"
API_list_datasources = "/cloudcanal/console/api/v1/openapi/datasource/listds"
API_add_datasources = "/cloudcanal/console/api/v1/openapi/datasource/addds"
API_deleteds = "/cloudcanal/console/api/v1/openapi/datasource/deleteds"
API_list_datajobs = "/cloudcanal/console/api/v1/openapi/datajob/list"
API_create_datajob = "/cloudcanal/console/api/v1/openapi/datajob/create"
API_datajob_precheckbasic = "/cloudcanal/console/api/v1/openapi/datajob/precheckbasic"
API_datajob_precheckdetail = "/cloudcanal/console/api/v1/openapi/datajob/precheckdetail"
API_delete_datajob = "/cloudcanal/console/api/v1/openapi/datajob/delete"
API_stop_datajob = "/cloudcanal/console/api/v1/openapi/datajob/stop"
API_query_datajob = "/cloudcanal/console/api/v1/openapi/datajob/queryjob"
API_start_datajob = "/cloudcanal/console/api/v1/openapi/datajob/start"
API_restart_datajob = "/cloudcanal/console/api/v1/openapi/datajob/restart"
API_upsertuserconfigs = "/cloudcanal/console/api/v1/openapi/user/config/upsertuserconfigs"  # 没有相应的openapi,废弃
API_updatetransferobject = "/cloudcanal/console/api/v1/openapi/datajob/updatetransferobject"
API_queryjobschemabyid = "/cloudcanal/console/api/v1/openapi/datajob/queryjobschemabyid"
API_update_jobdesc = "/cloudcanal/console/api/v1/openapi/datajob/updatedesc"
