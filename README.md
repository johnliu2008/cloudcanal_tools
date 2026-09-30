# cloudcanal_tools

用命令行调用 CloudCanal OpenAPI 的通用小工具：查集群 / 管数据源 / 建任务 / 删库 / 导出 schema，比 Web 页面更直接。

通用、无业务代码：同步的库表结构全部由用户提供的 JSON/JSONC 文件描述；凭据全部走环境变量，仓库里没有任何账号密码。

## 安装

```powershell
pip install -r requirements.txt
```

## 配置

| 环境变量 | 说明 | 默认值 |
|---|---|---|
| `CC_ACCESS_KEY_ID` / `CC_SECRET_KEY` | CloudCanal OpenAPI 认证凭据 | 占位符（必须设置） |
| `CC_ENDPOINT_TEMPLATE` | 接口地址，单实例如 `http://host:8111`，多实例可用 `{Number}` 占位 | `http://127.0.0.1:8111` |
| `CC_SERVER_NUMS` | 逗号分隔的实例编号 | `01` |

```powershell
$env:CC_ACCESS_KEY_ID = "ak..."
$env:CC_SECRET_KEY = "sk..."
$env:CC_ENDPOINT_TEMPLATE = "http://cc-{Number}.example.com:8111"
$env:CC_SERVER_NUMS = "01,02"
```

## 典型流程：建一个同步任务

1. 找一个同类线上任务导出 schema 当模板：

```powershell
python cloudcanal_tools.py export_job_schema 01 -a <job_id> --out-dir ./myjob
# 生成 ./myjob/source_schema.json target_schema.json mapping_config.json
```

2. 按需编辑这三个文件（删/改库表列），文件格式见 `examples/job_schema_example.jsonc`（支持 `//` 与 `/* */` 注释）。

3. 建任务（自动依次做基础预检、详细预检）：

```powershell
python cloudcanal_tools.py create_datajob 01 -a db1,db2 `
  --src-schema-file ./myjob/source_schema.json `
  --dst-schema-file ./myjob/target_schema.json `
  [--mapping-file ./myjob/mapping_config.json] `
  -e <src_ds_id> -f <dst_ds_id> -g <dest_name>
```

> RDS 数据源建完后需先在控制台点一次"测试连接"，否则建任务报 `0001`。

## 常用命令

```powershell
python cloudcanal_tools.py listclusters 01
python cloudcanal_tools.py listworkers 01 [--cluster-id 2]
python cloudcanal_tools.py listdatasources 01 [-e StarRocks]        # 按类型过滤
python cloudcanal_tools.py listdatajobs 01 [--page-size 10 --page-num 1]
python cloudcanal_tools.py query_datajob 01 -a <job_id>
python cloudcanal_tools.py stop_datajob 01 -a <job_id>              # 停止
python cloudcanal_tools.py start_datajob 01 -a <job_id>             # 启动
python cloudcanal_tools.py restart_datajob 01 -a <job_id>           # 重启
python cloudcanal_tools.py delete_datajob 01 -a <job_id>            # 先停后删
python cloudcanal_tools.py delete_db_from_job 01 -a <job_id> -b db1,db2   # 从任务中剔除某些库
python cloudcanal_tools.py create_datajob_migration 01 -a db1 --src-schema-file ... --dst-schema-file ... -e <src> -f <dst>
```

删库快捷流（sqlite 本地缓存任务列表）：

```powershell
python cloudcanal_tools.py insert_sqlite3_cloudcanal_jobs   # 刷新缓存
python cloudcanal_tools.py find_db_in_sqlite3 db1            # 查库在哪个任务
python cloudcanal_tools.py one_key_delete_db db1             # 从任务中剔除（删空则删任务）
```

## 说明

* `db_names`（如 `db1,db2`）只用于任务描述，实际同步范围以 schema 文件为准。
* `listdatajobs` 默认只取第 1 页，用 `--page-size/--page-num` 翻页。
* `update_delay_alert_threshold` 没有对应 API，只打印手动改库 SQL 模板。
* 导出的 schema / `datajobs.db` 可能含真实表结构与主机信息，已被 `.gitignore` 排除，提交前请检查。
