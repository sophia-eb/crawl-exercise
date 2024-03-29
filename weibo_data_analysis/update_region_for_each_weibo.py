# -*- coding:utf-8 -*-
import time
import json
import pymysql
import requests
from fake_useragent import UserAgent

"""
由于之前的数据库表格里面没有IP字段，添加后想要更新之前已经抓取的微博的Region
基于WeiboPersonalInfoSpider创建了一个UpdateRegionForWeibo
"""


class UpdateRegionForWeibo:
    def __init__(self):
        # 微博用户ID   测试用
        # self.user_id = "2609400635"
        # 随机获取headers
        self.user_agent = UserAgent(verify_ssl=False).random
        self.post_list = []
        self.weibo_link = "https://m.weibo.cn/api/container/getIndex?type=uid&value="

        # 打开数据库连接
        self.db = pymysql.connect(host="localhost", user="root", password="", db="weibo")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

        # 初始化微博数量
        self.weibo_total_number = 0

    def get_html_data(self, user_id):
        # 实际请求Url
        actual_url = self.weibo_link + str(user_id)
        print("抓取开始,实际请求Url:" + actual_url)
        # 请求并获取
        res = requests.get(actual_url, headers={'User-Agent': self.user_agent}).text
        return res

    @staticmethod
    def parse_user_info(user_id, res):
        item = dict()
        res_data_json = json.loads(res).get("data")
        # print(res_json)
        # 微博用户ID
        item["user_id"] = user_id
        # 微博用户名
        item["user_name"] = str(res_data_json["userInfo"]["screen_name"])
        # 性别
        item["gender"] = str(res_data_json["userInfo"]["gender"])
        # 认证信息
        item["verified_reason"] = str(res_data_json["userInfo"]["verified_reason"])
        # 微博说明
        item["description"] = str(res_data_json["userInfo"]["description"])
        # 读取微博账号微博的Domain值
        for tab in res_data_json["tabsInfo"]["tabs"]:
            if tab["tab_type"] == "weibo":
                item["container_id"] = tab["containerid"]
                item["domain"] = tab["containerid"][:6]
                break

        return item

    def get_user_follow_info(self, user_id, res):
        item = dict()
        res_data_json = json.loads(res).get("data")
        # print(res_json)
        # 微博用户ID
        item["user_id"] = user_id
        # 该用户的粉丝数
        item["followers_count"] = res_data_json["userInfo"]["followers_count"]
        # 该用户的关注数
        item["follow_count"] = res_data_json["userInfo"]["follow_count"]
        # 微博总数
        item["statuses_count"] = res_data_json["userInfo"]["statuses_count"]
        self.weibo_total_number = item["statuses_count"]
        return item

    def crawl_weibo(self, user_id, container_id):
        page_number = 1
        weibo_number = 0
        time.sleep(3)

        while True:
            print("weibo_number: ", weibo_number)
            print("weibo_total_number: ", self.weibo_total_number)
            if weibo_number > self.weibo_total_number:
                break
            request_url = self.weibo_link + str(user_id) + "&containerid=" + str(container_id) + "&page=" + str(
                page_number)
            result = requests.get(request_url, headers={'User-Agent': self.user_agent}).text
            print("========= 正在抓取第" + str(page_number) + "页 =========")
            # print(result)
            time.sleep(3)
            result_data_json = json.loads(result).get("data")
            cards = result_data_json.get("cards")
            cards_group = list()
            if len(cards) <= 0:
                break
            for card_number in range(len(cards)):
                weibo_number += 1
                # print(cards[card_number])
                print("========= 正在抓取第" + str(page_number) + "页第" + str(card_number + 1) + "条微博 =========")
                card_detail = {
                    "user_id": "",
                    "item_id": "",
                    "scheme": "",
                    "region_name": "",
                }
                card_data_json = cards[card_number]
                # 微博用户ID
                card_detail["user_id"] = user_id
                # 微博ID
                card_detail["item_id"] = card_data_json.get("itemid")
                # 微博链接
                card_detail["scheme"] = card_data_json.get("scheme")

                mblog = card_data_json.get("mblog")
                if mblog is None:
                    continue
                # 微博发布地点
                card_detail["region_name"] = mblog.get("region_name")

                self.insert_into_weibo_details_db(card_detail["scheme"], card_detail["region_name"])

        page_number += 1

    def insert_into_weibo_details_db(self, scheme, region_name):
        print("========= insert into weibo_details db =========")

        sql = "update `weibo_details` set region_name='{}' where scheme='{}';".format(region_name, scheme)

        # print("Update weibo_details SQL: ", sql)
        # print("cards_group: ", cards_group)
        try:
            # 使用 execute()  方法执行 SQL
            self.cursor.execute(sql)
            # 提交，不然无法保存新建或者修改的数据
            self.db.commit()
            print(self.cursor.rowcount, "record inserted.")
        except Exception as e:
            print("插入数据库异常！！！")
            print("Error: ", e)
            self.db.rollback()

    def run(self, *args):
        user_id = args[0]
        res = self.get_html_data(user_id)
        if not res:
            print("没有数据...")
            return
        try:
            user_info = self.parse_user_info(user_id, res)
            print("user_info: ", user_info)

            user_follow_info = self.get_user_follow_info(user_id, res)
            print("user_follow_info: ", user_follow_info)

            self.crawl_weibo(user_id, user_info["container_id"])
        except Exception as e:
            print("抓取数据格式异常！！！")
            print("Error messages: ", e)


if __name__ == '__main__':
    weibo = UpdateRegionForWeibo()
    userid_list = [2609400635,
                   2882733894, 3962982466, 1808764472, 6203188939,
                   2620811727, 3925308009, 5080118124, 5985666104,
                   1223178222, 5492443184, 1353112775]
    # userid_list = [5985666104]


    try:
        for user_id in userid_list:
            weibo.weibo_total_number = 0
            weibo.run(user_id)
    except Exception:
        pass
    finally:
        # 关闭游标
        weibo.cursor.close()
        # 关闭数据库连接
        weibo.db.close()
    print("=========== done ============")
