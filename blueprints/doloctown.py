import flask
from flask import Blueprint, render_template, request, jsonify
from pyecharts.charts import Line
from pyecharts import options as opts

from gdt_database.data import NetLoadRecorder, GDTMongoHandleBase
from gdt_database._cons import GDTCollections, GDTFields
from gdt_database._utils import *
from gdt_database._bug import BugUtils


from _cookies import CookieHelper, CookieKeys
import _theme
_cookie = CookieHelper("doloctown")

def not_found(message="404 Not Found"):
    '''未找到数据'''

    return render_template("not_found_page.html", theme=_theme.fetch_theme(), message=message)


class BugCollector_Exception(Blueprint):

    COOKIE_KEY_LAST_MENU_URL = "last_url"
    COOKIE_KEY_LAST_MENU_ID = "last_menu"

    def __init__(self, dataapi:GDTMongoHandleBase, netload_recorder:NetLoadRecorder, import_name, name = "doloctown", url_prefix = "/doloctown"):
        super().__init__(name, import_name, url_prefix=url_prefix)

        if netload_recorder is None:
            raise ValueError("netload_recorder shouldn't be None")
        
        if dataapi is None:
            raise ValueError("dataapi shouldn't be None")

        self.__netload_recorder = netload_recorder
        self.__dataapi = dataapi
        self.__init_rules()

    @property
    def cookies(self):
        '''get all the current cookies'''

        _current = {}
        # about last menu url
        _url = _cookie.get_cookie(BugCollector_Exception.COOKIE_KEY_LAST_MENU_URL, "/doloctown/bug/exception/0?handled=false")
        _current.setdefault(BugCollector_Exception.COOKIE_KEY_LAST_MENU_URL, _url)

        # last menu id
        _menu_id = _cookie.get_cookie(BugCollector_Exception.COOKIE_KEY_LAST_MENU_ID, "unhandled_exceptions")
        _current.setdefault(BugCollector_Exception.COOKIE_KEY_LAST_MENU_ID, _menu_id)        
        return _current

    def __init_rules(self):
        '''初始化路由规则'''

        routes = [

            # 测试计划
            ("/test_plans", self.test_plans, ["GET"]),

            # 异常报告
            ("/bug/exception/<page>", self._bug_exception_get_page, ["GET"]),
            ("/bug/exception/upload", self._bug_exception_upload, ["POST"]),
            ("/bug/exception/update/handle_status", self._bug_exception_update_handle_status, ["POST"]),
            ("/bug/exception/details/<Id>", self.bug_exception_details, ["GET"]),
            ("/bug/exception/utils/set_last_menu", self._set_last_bug_exception_menu, ["GET"]),
        ]
        for _route, _route_func, _route_methods in routes:
            self.add_url_rule(_route, view_func=_route_func, methods=_route_methods)
    
    def netload(self):
        '''数据负载'''

        _all_records = self.__netload_recorder.all_records
        result = self.__netload_recorder.result
        _total_count = result[GDTFields.NETLOAD_RESULT_TOTAL]
        _average_count = result[GDTFields.NETLOAD_RESULT_AVERAGE]
        _recent_total_count = result[GDTFields.NETLOAD_RESULT_RECENT]

        _total_count_err = result[GDTFields.NETLOAD_RESULT_TOTAL_ERR]
        _average_count_err = result[GDTFields.NETLOAD_RESULT_AVERAGE_ERR]
        _recent_total_count_err = result[GDTFields.NETLOAD_RESULT_RECENT_ERR]        

        # 返回数据
        return render_template("netload.html", 
                                records=_all_records, 
                                total_count=_total_count, 
                                average_count=_average_count,
                                recent_total_count=_recent_total_count,
                                total_count_err=_total_count_err,
                                average_count_err=_average_count_err,
                                recent_total_count_err=_recent_total_count_err)
    
    def content_netload_chart(self):
        '''数据负载图表'''

        _all_records = self.__netload_recorder.all_records
        if len(_all_records) > 7:
            _recent_records = _all_records[-7:]
        else:
            _recent_records = _all_records

        _reversed_list = list(_recent_records)

        _dates = [_[0] for _ in _reversed_list]
        _values = [_[1] for _ in _reversed_list]

        # Create a line chart
        line = (
            Line()
            .add_xaxis(_dates)
            .add_yaxis("访问次数", 
                       _values, 
                       is_smooth=True, 
                       label_opts=opts.LabelOpts(border_width=0, border_color="#00000000", font_size=16, is_show=False), 
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"), opts.MarkPointItem(type_="min")]),
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                       linestyle_opts=opts.LineStyleOpts(width=3))  # You can customize the series name
            .set_global_opts(
                title_opts=opts.TitleOpts(title="最近一周的访问记录"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return line.dump_options_with_quotes()

    # 关于测试计划
    def test_plans(self):
        '''测试计划'''

        _plans = self.__dataapi.all_test_plans
        return render_template("test_plans.html", plans=_plans, theme=_theme.fetch_theme(), current_plan=self.__dataapi.current_plan)
    
    def _bug_exception_upload(self):
        '''BUG报告: 异常报告上传'''

        self.__netload_recorder.record()
        if request.method != 'POST':
            return jsonify({"status": "error", "message": f"unsupported method '{request.method}' "})
        
        # 当前系统没有设立测试计划时，不予接受所有数据传输
        if self.__dataapi.current_plan is None:
            return jsonify({"status": "error", "message": "test plan is unset"})
        
        # 读取并验证数据是否有效
        _data = request.get_json()
        if _data is None or not BugUtils.validate_bug_exception(_data):
            return jsonify({"status": "error", "message": "invalid post data"})

        # 检查是否已经存在相同的异常报告(根据出发点的位置来进行判断)
        _triggers = _data.get(BugUtils.KEY_TRIGGER_POINTS, [])
        if len(_triggers) == 0:
            # 没有触发点时，视为无效数据
            return jsonify({"status": "error", "message": "invalid data"})
        else:
            _cnt = str()
            for pt in _triggers:
                _cnt += pt["code"]
            _summary_info = md5(_cnt)
            _query = { BugUtils.KEY_SUMMARY : _summary_info }
            if self.__dataapi.is_data_exists(_query):
                self.__dataapi.increment_data_count(_query)
                return jsonify({"status": "error", "message": "data already exists"})

        # 为本次上传附加时间信息等默认数据
        _data.setdefault(GDTFields.DATA_DATE, date_yymmdd())
        _data.setdefault(GDTFields.DATA_TIMESTAMP, timestamp())
        _data.setdefault(GDTFields.DATA_PLAN_ID, self.__dataapi.current_plan)
        _data.setdefault(GDTFields.DATA_COUNT, 1)
        _data.setdefault(BugUtils.KEY_SUMMARY, _summary_info)
        _data.setdefault(BugUtils.KEY_HANDLED, False)

        # 插入数据
        if self.__dataapi.insert_data(_data):
            return jsonify({"status": "ok", "message": "upload success"})
        return jsonify({"status": "error", "message": "insert data failed, database error"})

    def _bug_exception_get(self):
        '''异常报告'''

        if request.method != 'GET':
            return jsonify({"status": "error", "message": "请求方法错误"})
        
        # 查看是否仅查看已处理的异常
        _handled = request.args.get("handled")
        if _handled is None:
            # 返回所有异常

            _all_exceptions = self.__dataapi.get_datas()
            return render_template("doloctown/exception.html", count=len(_all_exceptions), date=date_yymmdd_prettry(), exceptions=_all_exceptions)
        
        _query = {GDTFields.BUG_REPORT_HANDLED: _handled.lower() == "true"}
        _handled_exceptions = self.__dataapi.get_datas(_query)
        return render_template("doloctown/exception.html", count=len(_handled_exceptions), date=date_yymmdd_prettry(), exceptions=_handled_exceptions)
    
    def _set_last_bug_exception_menu(self):
        '''设置上一次异常页面的菜单选项'''

        # set cookie success
        url = request.args.get("url", "/doloctown/bug/exception/0?handled=false")
        menu_id = request.args.get("menu", "unhandled_exceptions")

        res = jsonify({"status": "ok", "message": "Cookie设置成功"})
        _cookie.set_cookie_to(BugCollector_Exception.COOKIE_KEY_LAST_MENU_URL, url, res)
        _cookie.set_cookie_to(BugCollector_Exception.COOKIE_KEY_LAST_MENU_ID, menu_id, res)
        return res

    def _bug_exception_get_page(self, page):
        '''异常报告分页'''

        if request.method != 'GET':
            return jsonify({"status": "error", "message": "请求方法错误"})
        
        try:
            _page = int(page)
            if _page < 0:
                return jsonify({"status": "error", "message": "请求数据无效"})
        except ValueError:
            return jsonify({"status": "error", "message": "请求数据无效"})
        
        _page_size = 10         # 定义每页显示的数量/暂时写死
        _handled = request.args.get("handled")
        _query = {}
        _title = "所有异常总数"
        _postfix = ""
        if _handled != None:
            _query = {GDTFields.BUG_REPORT_HANDLED: _handled.lower() == "true"}
            _title = ("已处理" if _handled == "true" else "未处理") + "异常总数"
            _postfix = "?handled=" + _handled

        total_count = self.__dataapi.get_data_count(_query)
        _filtered_exceptions = self.__dataapi.get_datas_at_page(_page, _page_size, _query)

        _current_page = _page + 1
        _pages = handle_pages(total_count, _page_size, _current_page, page_range=5)
        _page_links = handle_pages_as_url("doloctown/bug/exception", _pages, _current_page, postfix=_postfix)
        _total_page_count = calc_page_count(total_count, _page_size)

        _pages.insert(0, "首页")
        _pages.append("尾页")
        _page_links.insert(0, "/doloctown/bug/exception/0" + _postfix)
        _page_links.append("/doloctown/bug/exception/{}".format(_total_page_count - 1) + _postfix)
        
        return render_template("doloctown/exception.html", 
                               count=total_count, 
                               title=_title,
                               date=date_yymmdd_prettry(), 
                               exceptions=_filtered_exceptions,
                               page_size = _page_size,
                               current_page=_page,
                               page_count = len(_pages),
                               pages=_pages,
                               page_links=_page_links)

    def _bug_exception_update_handle_status(self):
        ''''''

        if request.method != 'POST':
            return jsonify({"status": "error", "message": "请求方法错误"})
        
        _data = request.get_json()
        if _data is None:
            print("未设置请求数据")
            return jsonify({"status": "error", "message": "请求数据无效"})
        
        _id = _data.get("id", "")
        _handled = _data.get("handled", False)

        if not isinstance(_handled, bool):
            print("请求数据无效")
            return jsonify({"status": "error", "message": "请求数据无效"})
        
        if self.__dataapi.update_handle_status(_id, _handled):
            print("更新成功")
            return jsonify({"status": "ok", "message": "更新成功"})
        
        print("更新失败")
        return jsonify({"status": "error", "message": "数据库错误"})

    def bug_exception_details(self, Id):
        '''异常报告详情
        @Id: 异常报告的ID'''

        if request.method != 'GET':
            return jsonify({"status": "error", "message": "请求方法错误"})
        
        _exception = self.__dataapi.get_data(Id)
        if _exception is None:
            return not_found(f"未找到异常报告:{Id}")
        
        # 读取异常消息
        _name = _exception.get(BugUtils.KEY_NAME, "")
        _message = _exception.get(BugUtils.KEY_MESSAGE, "")
        _except_info = "{}: {}".format(_name, _message)
        
        # 读取异常运行日志
        _player_log = _exception.get(BugUtils.KEY_PLAYER_LOG, None)
        if _player_log is None:
            return not_found("未找到异常运行日志")
        _player_log = _player_log.split('\n')
        _player_log = [(_, BugUtils.is_error_line(_)) for _ in _player_log]

        # 读取异常堆栈信息
        _stacktrace = _exception.get(BugUtils.KEY_STACKTRACE, None)
        if _stacktrace is None:
            return not_found("未找到异常堆栈信息")
        _stacktrace = _stacktrace.split('\n')
        _stacktrace = [(_, BugUtils.is_error_line(_)) for _ in _stacktrace]

        # 读取运行日志
        _console_log = _exception.get(BugUtils.KEY_CONSOLE_LOG, None)
        if _console_log is None:
            return not_found("未找到异常运行日志")
        
        _exception = dict(_exception)
        return render_template(
            "doloctown/exception_details.html", 
            ex_message=_except_info,
            player_log = _player_log, 
            stacktrace = _stacktrace,
            console_log = _console_log,
            theme=_theme.fetch_theme())
