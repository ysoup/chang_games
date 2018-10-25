# encoding=utf-8
from flask import request, render_template, jsonify, flash, abort, url_for, redirect, session, Flask, g, current_app
from . import wangyi
from chang_games import redis_store
import json, time, datetime


@wangyi.route('/monitor_list', methods=['GET'])
def monitor_list():
    try:
        # 获取监控列表数据
        cache_data = redis_store.get("monitor_list")
        if cache_data:
            ls = json.loads(str(cache_data, encoding="utf-8"))
            return render_template('wangyi_games/monitor_list.html', data=ls)
        else:
            return render_template('wangyi_games/monitor_list.html', data=[])
    except Exception as e:
        current_app.logger.error(e)
        return render_template("404.html")


@wangyi.route('/add_monitor', methods=['GET', "POST"])
def add_monitor_info():
    if request.method == "GET":
        return render_template('wangyi_games/add_monitor_info.html')
    elif request.method == "POST":
        try:
            dic = {}
            dic["id"] = int(time.time())
            dic["goods_name"] = request.form.get("goods_name")
            dic["goods_url"] = request.form.get("goods_url")
            dic["safe_code"] = request.form.get("safe_code")
            dic["user_cookie"] = request.form.get("title")
            dic["remarks"] = request.form.get("title")
            dic["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            redis_store.set("new_monitor_data_%s" % dic["id"], json.dumps(dic))

            cache_data = redis_store.get("monitor_list")
            ls = []
            if cache_data:
                ls = json.loads(str(cache_data, encoding="utf-8"))
                ls.append(dic)
            else:
                ls.append(dic)
            redis_store.set("monitor_list", json.dumps(ls))
            return jsonify({'success': 'ok'})
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'failed': 'ok'})


# 编辑监控商品
@wangyi.route("/modify_monitor_data", methods=['GET', 'POST'])
def modify_monitor_data():
    if request.method == "GET":
        id = request.args.get('id', type=int)
        data = redis_store.get("new_monitor_data_%s" % id)
        return render_template('wangyi_games/modify_monitor_data.html', data=json.loads(str(data, encoding="utf-8")))
    elif request.method == "POST":
        try:
            id = request.form.get('id')
            goods_name = request.form.get('goods_name')
            goods_url = request.form.get('goods_url')
            safe_code = request.form.get('safe_code')
            user_cookie = request.form.get('user_cookie')
            remarks = request.form.get('remarks')
            data = redis_store.get("new_monitor_data_%s" % id)
            data = json.loads(str(data, encoding="utf-8"))
            data["goods_name"] = goods_name
            data["goods_url"] = goods_url
            data["safe_code"] = safe_code
            data["user_cookie"] = user_cookie
            data["remarks"] = remarks
            redis_store.set("new_monitor_data_%s" % id, json.dumps(data))
            return jsonify({"success": "ok"})
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'failed': '修改失败'})



