# db_util.py
# def get_toast_info():
#     db = pymysql.Connect(
#         host='xxx',
#         port=3306,
#         user='xxx',
#         passwd='xxx',
#         db='xxx',
#         charset='utf8'
#     )
#     cursor = db.cursor()
#     sql = "select content   from   guohe_lite_toast   order   by   id   desc   limit   1 "
#     try:
#         cursor.execute(sql)
#         result = cursor.fetchone()
#         return response_info.success('小程序通知查询成功', result)
#     except:
#         return response_info.error('2', '小程序通知查询失败', result)
#         # 关闭数据库连接
#     finally:
#         db.close()


def update_toast(toast_update_info):
    # db = pymysql.Connect(
    #     host='xxx',
    #     port=3306,
    #     user='xxxx',
    #     passwd='xxx',
    #     db='xxxx',
    #     charset='utf8'
    # )
    # cursor = db.cursor()
    # sql = "insert into guohe_lite_toast(content,update_time) values(%s,%s) "
    # try:
    #     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     cursor.execute(sql, (toast_update_info, dt))
    #     db.commit()
    #     return response_info.success('通知更新成功', toast_update_info)
    # except:
    #     db.rollback()
    #     return response_info.error("2", '更新失败', toast_update_info)
    # finally:
    #     db.close()
    return toast_update_info