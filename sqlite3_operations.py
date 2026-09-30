import sqlite3


def drop_table():
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS cloudcanal_jobs')
    cursor.close()
    conn.close()


def create_table():
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''CREATE TABLE IF NOT EXISTS cloudcanal_jobs
                   (id INTEGER    PRIMARY    KEY,
                    job_desc    text,
                    cc_num    text,
                    job_id    integer,
                    source_host    text,
                    target_host    text,
                    updated_time    text
                    )''')
    cursor.close()
    conn.close()


def create_index():
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()

    cursor.execute('CREATE INDEX idx_jobdesc ON cloudcanal_jobs (job_desc)')
    cursor.close()
    conn.close()


def insert_records(data):
    # 连接到SQLite数据库
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()
    try:
        # 插入一行记录
        cursor.execute('INSERT INTO cloudcanal_jobs (job_desc, cc_num, job_id, source_host, target_host, updated_time) VALUES (?, ?, ?, ?, ?, ?)', data)

        # 提交事务:
        conn.commit()

        return True
    except Exception as e:
        print(f"插入sqlite3时报错：{e}")
        return False
    finally:
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()


def update_records(id, job_desc):
    "修改sqlite3中的任务描述"
    # 连接到SQLite数据库
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()
    try:
        # 修改记录
        cursor.execute(f"UPDATE cloudcanal_jobs SET job_desc='{job_desc}' WHERE id={id}")
        # cursor.execute("UPDATE cloudcanal_jobs SET job_desc=? WHERE id=?", (id, job_desc))

        # 提交事务:
        conn.commit()

        return True
    except Exception as e:
        print(f"修改sqlite3时报错：{e}")
        return False
    finally:
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()


def delete_records(id):
    "删除任务数据"
    # 连接到SQLite数据库
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()
    try:
        # 删除记录
        cursor.execute('DELETE FROM cloudcanal_jobs WHERE id=?', (id,))

        # 提交事务:
        conn.commit()

        return True
    except Exception as e:
        print(f"删除sqlite3时报错：{e}")
        return False
    finally:
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()


def select_records(conditions=None, orderby=None):
    conn = sqlite3.connect('datajobs.db')
    cursor = conn.cursor()
    try:
        # 查询数据
        sql = 'SELECT * FROM cloudcanal_jobs '
        if conditions:
            sql += " WHERE 1=1 AND " + conditions
        if orderby:
            sql += "".join(orderby)
        cursor.execute(sql)
        result =cursor.fetchall()

        return result
    except Exception as e:
        print(f"查询sqlite3时报错：{e}")
        return False
    finally:
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()
