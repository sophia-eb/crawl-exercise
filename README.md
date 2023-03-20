# 爬虫练习

> @author: Sophia
> 
> @created: 2021-08-31
> 
> @modified: 2023-03-20

## weibo_data_analysis folder

微博数据抓取以及数据分析（已添加IP属地），包括：
- 用户ID，昵称，性别，认证信息，微博说明
- 用户的粉丝数量，关注数量，微博总数
- 每条微博的微博链接，微博内容，发布时间，发布设备，发布地点，抓取时的转发数，评论数，点赞数


#### 步骤
1. 运行 `MySQL/weibo.sql` 中的SQL语句，创建本地数据结构
2. 安装 `requirements.txt` 中的所有库
3. 切入 `weibo_data_analysis` 路径 
4. 填写 `weibo_personal_info_spider.py` 和 `update_region_for_each_weibo.py` 的 `__init__` 中的本地数据库配置 
5. 运行 `__name__` 函数即可
