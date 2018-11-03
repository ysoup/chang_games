# encoding=utf-8
from flask import request, render_template, jsonify, flash, abort, url_for, redirect, session, Flask, g, current_app
from chang_games import redis_store
import json, time, datetime, requests
from selenium import webdriver
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def monitor_wangyi():
    # 获取监控下单数据
    start = time.clock()
    while True:
        cache_data = redis_store.get("monitor_list")
        if cache_data:
            ls = json.loads(str(cache_data, encoding="utf-8"))
            monitor_data = ls[-1]
            goods_url = monitor_data["goods_url"]

            # 获取监控数据当前状态
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
            }
            split_data = goods_url.split("/")
            data = {
                "serverid": split_data[-2],
                "ordersn": split_data[-1]
            }
            goods_details = requests.post(url="https://my.cbg.163.com/cgi/api/get_equip_detail", data=data, headers=headers)
            if goods_details.status_code == 200:
                logging.info("获取监控商品数据")
                goods_details = json.loads(goods_details.text)
                logging.info("当前监控商品商家状态：%s" % goods_details["equip"]["pass_fair_show"])
                if goods_details["equip"]["pass_fair_show"] == 1:
                    logging.info("=====当前监控商品商家开始下单=====")
                    # 商品下单
                    headers["cbg-safe-code"] = monitor_data["safe_code"]
                    headers["Cookie"] = monitor_data["user_cookie"]
                    create_order = requests.post(url="https://my.cbg.163.com/cgi/api/preview_order", data=data,
                                                 headers=headers)
                    if create_order.status_code == 200:
                        order_info = json.loads(create_order.text)
                        if order_info["status"] != 2:
                            # 创建订单
                            logging.info("=====当前监控商品商家开始创建订单=====")
                            if "price_total" in order_info:
                                add_order_data = {
                                    "serverid": split_data[-2],
                                    "ordersn": split_data[-1],
                                    "confirm_price_total": order_info["price_total"],
                                    "view_loc": "all_list"
                                }
                                add_order = requests.post(url="https://my.cbg.163.com/cgi/api/add_order",
                                                          data=add_order_data,
                                                          headers=headers)
                                if add_order.status_code == 200:
                                    add_order_info = json.loads(add_order.text)
                                    # 第一步
                                    url = "https://my.cbg.163.com/cgi/pay_order?orderid_to_epay=%s" % add_order_info["order"]["orderid_to_epay"]
                                    pay_order_headers= {

                                    }
                                    pay_order = requests.get(url=url)


                                    logging.info("=====当前监控商品商家开始支付=====")

                                    # order_pay_1 = requests.post(url="https://epay.163.com/cashier/ajaxCoupons?orderId=2018102721JY26375945",
                                    #                           data=order_pay_data,
                                    #                           headers=headers)

                                    order_pay_data = {
                                        "proposal": {
                                            "coupon": "null",
                                            "balance": {
                                                "payAmount": "61.00"
                                            },
                                            "orderId": "2018102722JY26495565"
                                        },
                                        "securityValid": {"pwEnVer": "M_A_1",
                                                           "payPassword":"oDXbevgqeJ%2Fee27WhvGVFTmu7TMEBnf75t8wqVF1JBwWNaMxSSOmamLDzSOJR4XU"
                                                          },
                                        "envData": {"term": "web"},
                                        "track": [["cashier", "paymode-hongbao"],
                                                  ["cashier", "paymode-account"],
                                                  ["cashier", "paybutton-combinpay"]
                                                  ]
                                    }

                                    order_pay_headers ={
                                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0",
                                        "Cookie": "EPAY_ENV=YQ_ROOM; _ntes_nnid=63ecdac04ddabe3cab821646df39ae71,1525418115547; _ntes_nuid=63ecdac04ddabe3cab821646df39ae71; usertrack=O2+gylr4Sd1+fUO3BNHbAg==; mail_psc_fingerprint=00dd2db27d7e8d1883e19e147cd4a438; _ga=GA1.2.556291577.1530420929; ANTICSRF=6d557033b0551e4a0fb0f9c87d0f2e89; EPAYSESSIONID=EPAY-3b68b3b8-baff-40c3-b9f7-9ae0edc07107; _OkLJ_%UJ=QVDHIG79LR324U9O; FRMS_FINGERPRINT=136100000000000000001371dfa004ad8ed498722b01cb7f9558c02ffb841381b326b5062b2f0e69139100000000000000001351c4ca4238a0b9238212317fec306d1e665bc9141100000000000000001401b326b5062b2f0e691341c20ad4d76fe97759132168934a3e9455fa72122144968aece94f667e1421000000000000000000914f3905fc7a48113101016e0df8df3f2a8b091201d62a1a3bb908ffa31211731c83db8d2ff01b1291502f1bd97b0e7d80124182cadb0649a3af491281d3d9446802a442591261000000000000000012511ff1de774005f8da1331c81e728d9d4c2f631271d3d9446802a44259130187374a5ff147c45613111de9313c44872e4c; JSESSIONID=0E2EB370085FE289916353F02531E71F; NTES_PASSPORT=v6aRXmwkHgMA4O4g_tK2mrt8oiXha0WP.Gl1g16r0CUeKP1dHVMy5YiKfYwYNH2Hg6a4bcNg67Og0Ixgx4iMDZ1JaN1jP95onT88UIHdfDsvXVWtXB3oOwxp9uOptYr4xicE9b5FpyGcUN8cQCB7ALtLw3TqV2mP8HgnoVfu4U2u4YpR6JG8CUl9sQN0ezeM6; NTES_SESS=BdYpJgr_Vq7AgBLfB26j_j2A.IhZKwmGutRhHpv3jxmA8OSGlXyvncP87cIc6lCl.Ys04K6.YHzsGpe3v6mhBN4qspKFtfwlXip77XX3Nn.0_p.8Vy1Uwv4tKW.iSWjPZCDNmWxbKOnACMjdSMGsx6Xfkii1fO7KgICRNndPfkOqip30VndluWuz34pn8l6HnSwECRDDMvKz1lf6VpFVHhleJ; S_INFO=1540647153|0|#2&70#|menghuancbg001@126.com; P_INFO=menghuancbg001@126.com|1540647153|1|cbg|00&99|shd&1540640306&urscloud#bej&null#10#0#0|&0|epay&g83_client&urscloud&cbg|menghuancbg001@126.com; _gat=1; mp_MA-B480-7AA0C2ACD2CD_hubble=%7B%22deviceUdid%22%3A%20%2206a15654-ef53-484a-8469-4aebf279ed0e%22%2C%22updatedTime%22%3A%201540649163213%2C%22sessionStartTime%22%3A%201540649092050%2C%22sessionReferrer%22%3A%20%22https%3A%2F%2Fepay.163.com%2Fcashier%2FstandardCashier%3ForderId%3D2018102722JY26495565%22%2C%22sessionUuid%22%3A%20%2297fe9f5c-a1a4-48e2-95ba-08824c4c9810%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fmy.cbg.163.com%2Fcgi%2Fshow_login%3Fback_url%3Dhttps%253A%252F%252Fmy.cbg.163.com%252Fcgi%252Fpay_order%253Forderid_to_epay%253D33_2191%26login_trigger%3Depay%22%2C%22initial_referring_domain%22%3A%20%22my.cbg.163.com%22%2C%22persistedTime%22%3A%201540626257741%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22confirmClick%22%2C%22time%22%3A%201540649163213%7D%7D"
                                    }
                                    order_pay = requests.post(url="https://epay.163.com/cashier/ajaxPay",
                                                              data=order_pay_headers,
                                                              headers=headers)
                                    if order_pay.status_code == 200:
                                        logging.info("订单支付返回信息: %s" % order_pay.text)
                        else:
                            logging.info("=====登录cookie失效=====")
            end = time.clock()
            logging.info("当前订单操作时间：%s" % (end - start))


if __name__ == '__main__':
    monitor_wangyi()
