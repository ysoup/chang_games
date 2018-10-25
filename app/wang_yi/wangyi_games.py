# encoding=utf-8
from flask import request, render_template, jsonify, flash, abort, url_for, redirect, session, Flask, g, current_app
from . import wangyi
from chang_games import redis_store
import json


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
            title = request.form.get("title")
            if title == None or title == "":
                title = ""
            info = NewFlashInformation(content=request.form['content'], category=request.form['category'],highlight_color=request.form['highlight_color'],
                                       is_show=int(request.form['is_show']),is_push=int(request.form["is_push"]),
                                       remarks=request.form['remarks'], source_name="ren_gong", content_id=int(time.time()), title=title)
            db.session.add(info)
            if info.is_push == 1:
                content = title
                content_text = copy.deepcopy(content)
                content_text = filter_char(content_text)
                code = push_service.common_push_server(content_text)
                if code == 201:
                    info.is_push = 1
                    info.is_show = 1
            db.session.commit()
            return jsonify({'success': 'ok'})
        except Exception as e :
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify({'failed': 'ok'})


# @wangyi_games.route('/create_monitor_data', methods=['GET', 'POST'])
# def create_monitor_data():
#     if request.method == "GET":
#         return render_template('wangyi_games/create_monitor_data.html')
#     elif request.method == "POST":
#         try:
#             title = request.form.get("title")
#             if title == None or title == "":
#                 title = ""
#             info = NewFlashInformation(content=request.form['content'], category=request.form['category'],highlight_color=request.form['highlight_color'],
#                                        is_show=int(request.form['is_show']),is_push=int(request.form["is_push"]),
#                                        remarks=request.form['remarks'], source_name="ren_gong", content_id=int(time.time()), title=title)
#             db.session.add(info)
#             if info.is_push == 1:
#                 content = title
#                 content_text = copy.deepcopy(content)
#                 content_text = filter_char(content_text)
#                 code = push_service.common_push_server(content_text)
#                 if code == 201:
#                     info.is_push = 1
#                     info.is_show = 1
#             db.session.commit()
#             return jsonify({'success': 'ok'})
#         except Exception as e :
#             current_app.logger.error(e)
#             db.session.rollback()
#             return jsonify({'failed': 'ok'})


