#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/4 15:12
# @Author  : Chiao
import sys
import asyncio
import aiohttp
import time
import json
import requests
import pymysql
import traceback
import nameMap
from selenium.webdriver import Chrome, ChromeOptions

country_dict = {}


def get_tencent_data():
    # 通过解析腾讯疫情网站，可以得知所有疫情数据来源于这两个url对应的api接口
    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"

    # 设置请求头，防止爬虫失败
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    # json转换格式
    r1 = requests.get(url1, headers)
    r2 = requests.get(url2, headers)

    # 将json格式转换为字典格式
    res1 = json.loads(r1.text)
    res2 = json.loads(r2.text)

    data_all1 = json.loads(res1["data"])
    data_all2 = json.loads(res2["data"])

    history = {}
    for i in data_all2["chinaDayList"]:
        ds = "2021." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]

        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}

    for i in data_all2["chinaDayAddList"]:
        ds = "2021." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm_add = city_infos["today"]["confirm"]
            confirm = city_infos["total"]["confirm"]
            dead = city_infos["total"]["dead"]
            heal = city_infos["total"]["heal"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details


def get_conn():
    # 建立连接
    conn = pymysql.connect(host="127.0.0.1", user="root", password="qweasd1234", db="cov", charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def update_history():
    conn, cursor = get_conn()
    try:
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds = %s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_details():
    conn, cursor = get_conn()
    try:
        det = get_tencent_data()[1]
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        cursor.execute(sql_query, det[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in det:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def get_baidu_hot():
    option = ChromeOptions()
    option.add_argument("--headless")  # 隐藏浏览器
    option.add_argument("--no-sandbox")
    browser = Chrome(executable_path='E:\Studys\毕业设计\毕业设计\chromedriver.exe', options=option)

    url = "https://s.weibo.com/top/summary"
    browser.get(url)
    but = browser.find_element_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')
    but.click()  # 模拟人类点击
    time.sleep(1)
    c = browser.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')
    context = [i.text for i in c]
    browser.close()
    return context


def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))
        conn.commit()
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


async def get_url_country(country_name, url):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with await session.get(url, headers=header) as response:
            res = json.loads(await response.text())
            res = res['data']
            if res:  # 不为空
                country_dict[country_name] = res  # 返回添加各国数据，存储到字典


def get_country_data(*country_list):
    start_time = time.time()
    if not country_list:
        country_list = list(nameMap.nameMap.values())[1:]  # 各国列表
    else:
        country_list = country_list[0]

    task_list = []
    new_loop = asyncio.new_event_loop()  # 指定event loop对象
    asyncio.set_event_loop(new_loop)  # 指定event loop对象
    for country in country_list:
        url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=' + country
        request = get_url_country(country, url)  # 协程请求各国数据
        task = asyncio.ensure_future(request)
        task_list.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task_list))

    # 返回数据经过筛选的各国字典
    country_data = {}
    for country in country_dict:
        daily_data = []
        for value in country_dict.get(country):  # 各国数据处理
            ds = value['y'] + value['date']
            tup = time.strptime(ds, '%Y%m.%d')
            update_time = time.strftime('%Y-%m-%d', tup)  # 改变时间格式，不然插入数据库会报错
            value['date'] = update_time
            daily_data.append(list(value.values()))
        daily_data.reverse()  # 倒序，将最新日期置为首部，提高数据库操作效率
        country_data[country] = daily_data
    print("各国数据请求完毕:", time.time() - start_time, '秒')
    return country_data


def update_fforeign(*country_list):
    cursor = None
    conn = None
    try:
        start_time = time.time()
        conn, cursor = get_conn()
        # 数据不存在, 插入数据
        sql_query_insert = 'select confirm from fforeign where country = %s and update_time= %s'
        sql_query = "select update_time from fforeign order by update_time desc limit 1"
        sql_insert = 'insert into fforeign(country,update_time,confirm_add,confirm,heal,dead) ' \
                     'values(%s,%s,%s,%s,%s,%s)'
        country_data = get_country_data(*country_list)
        time_data = country_data["美国"][0][0] + " 00:00:00"
        val = cursor.execute(sql_query)
        if val != 0:
            form_time = cursor.fetchone()[0]

        # 与爬取数据的时间数据进行对比，如果不同则更新数据
        if val == 0 or str(form_time) != time_data:
            print(f'{time.asctime()} -- 正在更新国外数据，数据量较大请稍微等待一会')
            # 更新数据库
            for country, dailyData in country_data.items():  # 迭代国家列表
                # 该国有疫情数据
                for item in dailyData:
                    cursor.execute(sql_query_insert, [country, item[1]])  # country代表国家, item[0]代表日期
                    # 该日确诊数据为null, 插入数据
                    if not cursor.fetchone():
                        cursor.execute(sql_insert, [country, item[1], item[2], item[3], item[4], item[5]])  # 插入数据
                        conn.commit()  # 提交事务
                        print(f'{time.asctime()} -- 国外数据更新完毕！，用时:', time.time() - start_time, '秒')
                        continue
                    break
        else:
            print(f'{time.asctime()} -- 已是国外最新数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    keys = len(sys.argv)
    if keys == 1:
        s = """
    	请输入参数
    	参数说明
    	update_history 更新历史记录表
u       update_hotsearch 更新实时热搜
    	update_details 更新详细表
    	update_foreign 更新世界疫情地图
    	"""
        print(s)
    else:
        order = sys.argv[1]
        if order == "update_history":
            update_history()
        elif order == "update_details":
            update_details()
        elif order == "update_hotsearch":
            update_hotsearch()
        elif order == "update_foreign":
            update_fforeign()
update_history()
update_details()
update_hotsearch()
update_fforeign()
