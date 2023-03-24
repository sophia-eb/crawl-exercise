# -*- coding:utf-8 -*-
import datetime
import json
import requests
import pymysql
from DecryptLogin import login
from fake_useragent import UserAgent
from pymysql.converters import escape_string


class RankListSpider:
    def __init__(self):
        print("--------------")
        self.user_agent = UserAgent(verify_ssl=False).random
        # self.zhihu_salt_link = "https://www.zhihu.com/xen/market/ranking-list/salt"
        # 热搜榜
        # self.zhihu_salt_api_link = "https://api.zhihu.com/market/rank_list?type=hottest&sku_type=salt_all&limit=200&offset=0"
        # self.list_type = "hottest"
        # 飙升榜
        # self.zhihu_salt_api_link = "https://api.zhihu.com/market/rank_list?type=fastest&sku_type=salt_all&limit=200&offset=0"
        # self.list_type = "fastest"
        # 上新榜
        self.zhihu_salt_api_link = "https://api.zhihu.com/market/rank_list?type=newest&sku_type=salt_all&limit=200&offset=0"
        self.list_type = "newest"
        # self.zhihu_column_link = "https://www.zhihu.com/xen/market/remix/paid_column/1388228020830855168"

        # 打开数据库连接
        self.db = pymysql.connect(host="localhost", user="root", password="", db="zhihu")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    def login(self):
        client = login.Client()
        zhihu = client.zhihu(reload_history=True)
        infos_return, session = zhihu.login(username='', password='', mode='scanqr')
        # print(infos_return, session)
        return session

    def get_html_data(self, login_status):
        # 实际请求Url
        actual_url = self.zhihu_salt_api_link
        print("抓取开始,实际请求Url:" + actual_url)
        # 请求并获取(另一个方法可以尝试)
        # res = login_status.get(actual_url, headers={'User-Agent': self.user_agent})
        # 请求并获取
        res = requests.get(actual_url, headers={'User-Agent': self.user_agent})
        html = res.content.decode()
        bjson = json.loads(html)
        data = bjson["data"]
        return data

    def insert_into_salt_ranking_list_db(self, data):
        print("========= insert into salt_ranking_list db =========")
        i = 0
        for item in data:
            i += 1
            print(f'Inserting {i}, name is {item["title"]}')
            sql = """
            INSERT INTO `salt_ranking_list` (`title`, `author`, `media_type`, `price`, `description`, `summary`, `url`, `list_type`, `json_data`, `created_date`) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
            """ % (
                item["title"], item["author"], item["media_type"], item["button_info"]["button_text"],
                escape_string(item["description"]), escape_string(item["summary"]), item["url"],
                self.list_type, escape_string(json.dumps(item)),
                datetime.datetime.now())
            # print("Insert user_details SQL: ", sql)
            try:
                # 使用 execute()  方法执行 SQL
                self.cursor.execute(sql)
                # 提交，不然无法保存新建或者修改的数据
                self.db.commit()
                print(self.cursor.rowcount, "record inserted.")
            except pymysql.err.IntegrityError as e:
                print("插入数据库异常！！！")
                print("Error: ", e)
                self.db.rollback()
            except Exception as e:
                print("Insert user_details SQL: ", sql)
                print("插入数据库异常！！！")
                print("Error: ", e, type(e))
                self.db.rollback()

    def run(self):
        login_status = self.login()
        data = self.get_html_data(login_status)
        # print("data: ", data)
        self.insert_into_salt_ranking_list_db(data)


if __name__ == '__main__':
    zhihu = RankListSpider()
    try:
        zhihu.run()
    except Exception as e:
        print("error: ", e)
    finally:
        # 关闭游标
        zhihu.cursor.close()
        # 关闭数据库连接
        zhihu.db.close()
    print("=========== done ============")
