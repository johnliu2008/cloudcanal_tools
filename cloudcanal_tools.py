import sys
import argparse

import processor

def main():
    # 创建主解析器
    parser = argparse.ArgumentParser(description="使用命令行调用Cloudcanal API，来实现各种常用操作，比web页面操作更直接")

    # 创建子解析器
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 创建 'listclusters' 子解析器
    parser_listclusters = subparsers.add_parser('listclusters', help='集群列表')
    parser_listclusters.add_argument('cc_num', type=str, help='CC服务器编号')

    parser_listworkers = subparsers.add_parser('listworkers', help='输出指定CC服务器的关键信息')
    parser_listworkers.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_listworkers.add_argument('--cluster-id', type=int, default=2, help='集群ID，默认2')

    parser_listdatasources = subparsers.add_parser('listdatasources', help='查询数据源，ds_type可以传StarRocks / AuroraMySQL')
    parser_listdatasources.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_listdatasources.add_argument('-a', '--dataSourceId', type=int, help='数据源ID')
    parser_listdatasources.add_argument('-b', '--deployType', type=str, help='部署类型')
    parser_listdatasources.add_argument('-c', '--hostType', type=str, help='主机类型')
    parser_listdatasources.add_argument('-d', '--lifeCycleState', type=str, help='生命周期')
    parser_listdatasources.add_argument('-e', '--ds_type', type=str, help='数据源类型')

    parser_adddatasource = subparsers.add_parser('adddatasource', help='添加数据源')
    parser_adddatasourcegroup = parser_adddatasource.add_mutually_exclusive_group()
    parser_adddatasource.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_adddatasource.add_argument('-a', '--deployType', type=str, help='部署类型，RDS就填AWS_CLOUD_HOSTED，StarRocks就填SELF_MAINTENANCE')
    parser_adddatasource.add_argument('-b', '--dataSourceType', type=str, help='数据源类型，AuroraMySQL/StarRocks')
    parser_adddatasource.add_argument('-c', '--hostType', type=str, help='主机类型，PRIVATE/PUBLIC')
    parser_adddatasourcegroup.add_argument('-p', '--privateHost', type=str, help='内网主机地址')
    parser_adddatasourcegroup.add_argument('-q', '--publicHost', type=str, help='外网主机地址')
    parser_adddatasource.add_argument('-d', '--instanceDesc', type=str, help='主机描述，不能逗号，不建议含有空格')
    parser_adddatasource.add_argument('-e', '--region', type=str, default='', help='区域')
    parser_adddatasource.add_argument('-f', '--account', type=str, help='数据库账号')
    parser_adddatasource.add_argument('-g', '--password', type=str, help='数据库密码')

    parser_deletedatasource = subparsers.add_parser('deletedatasource', help='删除数据源')
    parser_deletedatasource.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_deletedatasource.add_argument('-a', '--datasource_id', type=int, help='数据源ID')

    parser_listdatajobs = subparsers.add_parser('listdatajobs', help='列出同步任务（单页）')
    parser_listdatajobs.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_listdatajobs.add_argument('--page-size', type=int, default=10, help='每页条数，默认10')
    parser_listdatajobs.add_argument('--page-num', type=int, default=1, help='页码，默认1')

    parser_create_datajob = subparsers.add_parser('create_datajob', help='添加同步任务（schema 由 JSON/JSONC 文件提供）')
    parser_create_datajob.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_create_datajob.add_argument('-a', '--db-names', type=str, required=True, help='数据库名，若有多个则用英文逗号分隔，如db1,db2')
    parser_create_datajob.add_argument('--src-schema-file', type=str, required=True, help='源端 schema 文件（JSON/JSONC，见 examples/job_schema_example.jsonc）')
    parser_create_datajob.add_argument('--dst-schema-file', type=str, required=True, help='目标端 schema 文件（JSON/JSONC）')
    parser_create_datajob.add_argument('--mapping-file', type=str, default='', help='映射定义文件（JSON/JSONC），不传则使用默认 MIRROR 映射')
    parser_create_datajob.add_argument('-c', '--init_sync', action='store_true', help='是否同步全量数据')
    parser_create_datajob.add_argument('-d', '--specid', type=int, default=16, help='任务规格，默认是16(2GB)')
    parser_create_datajob.add_argument('-e', '--src_datasource_id', type=int, required=True, help='源数据源ID')
    parser_create_datajob.add_argument('-f', '--dst_datasource_id', type=int, required=True, help='目标数据源ID')
    parser_create_datajob.add_argument('-g', '--dest-name', type=str, default='', help='目标端名称，可简写，用于任务描述')

    parser_delete_datajob = subparsers.add_parser('delete_datajob', help='删除同步任务')
    parser_delete_datajob.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_delete_datajob.add_argument('-a', '--datajob_id', type=int, help='任务ID')

    parser_stop_datajob = subparsers.add_parser('stop_datajob', help='停止同步任务')
    parser_stop_datajob.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_stop_datajob.add_argument('-a', '--datajob_id', type=int, help='任务ID')

    parser_query_datajob = subparsers.add_parser('query_datajob', help='查询同步任务')
    parser_query_datajob.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_query_datajob.add_argument('-a', '--datajob_id', type=int, help='任务ID')

    parser_start_datajob = subparsers.add_parser('start_datajob', help='启动同步任务')
    parser_start_datajob.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_start_datajob.add_argument('-a', '--datajob_id', type=int, help='任务ID')

    parser_restart_datajob = subparsers.add_parser('restart_datajob', help='重启同步任务')
    parser_restart_datajob.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_restart_datajob.add_argument('-a', '--datajob_id', type=int, help='任务ID')

    parser_update_delay_alert_threshold = subparsers.add_parser('update_delay_alert_threshold', help='修改任务延时告警的阈值')
    parser_update_delay_alert_threshold.add_argument('cc_num', type=str, help='CC服务器编号')

    parser_delete_db_from_job = subparsers.add_parser('delete_db_from_job', help='从同步任务中删除某些库,并更新任务描述')
    parser_delete_db_from_job.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_delete_db_from_job.add_argument('-a', '--datajob_id', type=int, help='任务ID')
    parser_delete_db_from_job.add_argument('-b', '--db-names-deleted', type=str, help='需要删除的数据库名，多个用英文逗号分隔，如db1,db2')

    parser_export_job_schema = subparsers.add_parser('export_job_schema', help='导出线上任务的 schema 为 JSON 文件，可作为建任务的模板')
    parser_export_job_schema.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_export_job_schema.add_argument('-a', '--datajob_id', type=int, required=True, help='任务ID')
    parser_export_job_schema.add_argument('--out-dir', type=str, default='.', help='输出目录，默认当前目录')

    parser_insert_sqlite3_cloudcanal_jobs = subparsers.add_parser('insert_sqlite3_cloudcanal_jobs', help='遍历所有的CC服务器，将查询出来的任务列表，保存到SQLite3中')

    parser_find_db_in_sqlite3 = subparsers.add_parser('find_db_in_sqlite3', help='到SQLite3中查询与db_name相关的同步任务')
    parser_find_db_in_sqlite3.add_argument('db_name', type=str, help='需要查询的数据库名,如db1')

    parser_one_key_delete_db = subparsers.add_parser('one_key_delete_db', help='一键删库函数，快速找到该库对应的CC任务，从该任务中剔除或删除该任务')
    parser_one_key_delete_db.add_argument('db_name', type=str, help='需要删除的数据库名,如db1')

    parser_create_datajob_migration = subparsers.add_parser('create_datajob_migration', help='创建 MIGRATION 类型任务（schema 由 JSON/JSONC 文件提供）')
    parser_create_datajob_migration.add_argument('cc_num', type=str, help='CC服务器编号')
    parser_create_datajob_migration.add_argument('-a', '--db-names', type=str, required=True, help='数据库名，多个用英文逗号分隔')
    parser_create_datajob_migration.add_argument('--src-schema-file', type=str, required=True, help='源端 schema 文件（JSON/JSONC）')
    parser_create_datajob_migration.add_argument('--dst-schema-file', type=str, required=True, help='目标端 schema 文件（JSON/JSONC）')
    parser_create_datajob_migration.add_argument('--mapping-file', type=str, default='', help='映射定义文件（JSON/JSONC），不传则使用默认 MIRROR 映射')
    parser_create_datajob_migration.add_argument('-c', '--init_sync', action='store_true', help='是否同步全量数据')
    parser_create_datajob_migration.add_argument('-d', '--specid', type=int, default=16, help='任务规格，默认16(2GB)')
    parser_create_datajob_migration.add_argument('-e', '--src_datasource_id', type=int, required=True, help='源数据源ID')
    parser_create_datajob_migration.add_argument('-f', '--dst_datasource_id', type=int, required=True, help='目标数据源ID')
    parser_create_datajob_migration.add_argument('-g', '--dest-name', type=str, default='', help='目标端名称，可简写，用于任务描述')

    # 解析参数
    args = parser.parse_args()

    def _load_schemas(args):
        src_schema = processor.load_schema_file(args.src_schema_file)
        dst_schema = processor.load_schema_file(args.dst_schema_file)
        mapping_def = processor.load_schema_file(args.mapping_file) if args.mapping_file else None
        if src_schema is False or dst_schema is False or mapping_def is False:
            sys.exit(2)
        return src_schema, dst_schema, mapping_def

    # 根据子命令执行相应的操作
    if args.command == 'listclusters':
        processor.listclusters(cc_num=args.cc_num)
    elif args.command == 'listworkers':
        processor.listworkers(cc_num=args.cc_num, cluster_id=args.cluster_id)
    elif args.command == 'listdatasources':
        processor.listdatasources(cc_num=args.cc_num, dataSourceId=args.dataSourceId, deployType=args.deployType,
                                  hostType=args.hostType, lifeCycleState=args.lifeCycleState, ds_type=args.ds_type)
    elif args.command == 'adddatasource':
        processor.adddatasource(cc_num=args.cc_num, dataSourceType=args.dataSourceType, deployType=args.deployType,
                                  hostType=args.hostType, region=args.region, privateHost=args.privateHost,
                                publicHost=args.publicHost, instanceDesc=args.instanceDesc,
                                account=args.account, password=args.password)
    elif args.command == 'deletedatasource':
        processor.deletedatasource(cc_num=args.cc_num, datasource_id=args.datasource_id)
    elif args.command == 'listdatajobs':
        processor.listdatajobs(cc_num=args.cc_num, page_size=args.page_size, page_num=args.page_num)
    elif args.command == 'create_datajob':
        src_schema, dst_schema, mapping_def = _load_schemas(args)
        processor.create_datajob(cc_num=args.cc_num, db_names=args.db_names, src_schema=src_schema,
                                 dst_schema=dst_schema, mapping_def=mapping_def,
                                 init_sync=args.init_sync, specid=args.specid, src_datasource_id=args.src_datasource_id,
                                 dst_datasource_id=args.dst_datasource_id, dest_name=args.dest_name)
    elif args.command == 'delete_datajob':
        processor.stop_and_delete_datajob(cc_num=args.cc_num, datajob_id=args.datajob_id)
    elif args.command == 'stop_datajob':
        processor.stop_datajob(cc_num=args.cc_num, datajob_id=args.datajob_id)
    elif args.command == 'query_datajob':
        processor.query_datajob(cc_num=args.cc_num, datajob_id=args.datajob_id)
    elif args.command == 'start_datajob':
        processor.start_datajob(cc_num=args.cc_num, datajob_id=args.datajob_id)
    elif args.command == 'restart_datajob':
        processor.restart_datajob(cc_num=args.cc_num, datajob_id=args.datajob_id)
    elif args.command == 'update_delay_alert_threshold':
        print('''由于没有相关的API,请登录到CC %s 服务器,使用如下命令修改（按你的实际账号/端口替换）:\n
        mysql -h127.0.0.1 -P<port> -u<user> -p'<password>' -e "update cloudcanal_console.alert_config_detail set expression='DELAY_MIN>=2'"'''
              % args.cc_num)
        sys.exit(1)
    elif args.command == 'delete_db_from_job':
        processor.delete_db_from_job(cc_num=args.cc_num, datajob_id=args.datajob_id, db_names_deleted=args.db_names_deleted)
    elif args.command == 'export_job_schema':
        processor.export_job_schema(cc_num=args.cc_num, datajob_id=args.datajob_id, out_dir=args.out_dir)
    elif args.command == 'insert_sqlite3_cloudcanal_jobs':
        processor.insert_sqlite3_cloudcanal_jobs()
    elif args.command == 'find_db_in_sqlite3':
        processor.find_db_in_sqlite3(db_name=args.db_name)
    elif args.command == 'one_key_delete_db':
        processor.one_key_delete_db(db_name=args.db_name)
    elif args.command == 'create_datajob_migration':
        src_schema, dst_schema, mapping_def = _load_schemas(args)
        processor.create_datajob_migration(
            cc_num=args.cc_num,
            db_names=args.db_names,
            src_schema=src_schema,
            dst_schema=dst_schema,
            mapping_def=mapping_def,
            init_sync=args.init_sync,
            specid=args.specid,
            src_datasource_id=args.src_datasource_id,
            dst_datasource_id=args.dst_datasource_id,
            dest_name=args.dest_name
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
