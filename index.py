import gevent
from flask import Flask, render_template, request, make_response
from blueprints.doloctown import *
from gdt_database import *
from _gdt_logger import GDTLogger

import _theme
from server_config import ServerConfig
_netload_recorder = None
_bug_collector = None

def load_bug_collector(app:flask.Flask, config:ServerConfig):
    '''初始化BUG收集器'''

    global _netload_recorder
    global _bug_collector

    _logger = GDTLogger(config.log_folder)
    _mongo_client = GDTMongoClient(config.dblink)
    _netload_recorder = NetLoadRecorder(_logger, _mongo_client.get_database("doloctown"))
    _doloctown_api = GDTMongoHandleBase(_mongo_client.get_database("doloctown"))
    _bug_collector = BugCollector_Exception(_doloctown_api, _netload_recorder, import_name=__name__)
    app.register_blueprint(_bug_collector)

def load_base_routes(app:flask.Flask):
    '''初始化所有基础路由'''

    routes = [
        ("/", index, ["GET"]),
        ("/server_status/netload", server_status_netload, ["GET"]),
        ("/server_status/netload/chart", server_status_netload_chart, ["GET"]),
        ("/utils/set_theme/<theme>", set_theme, ["GET"])
    ]
    for _route, _route_func, _route_methods in routes:
        app.add_url_rule(_route, view_func=_route_func, methods=_route_methods)

def index():
    '''首页'''
    return render_template('index.html', theme=_theme.fetch_theme(), cookies=_bug_collector.cookies)

def server_status_netload():
    '''数据负载'''

    _all_records = _netload_recorder.all_records
    result = _netload_recorder.result
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

def server_status_netload_chart():
    '''数据负载图表'''

    _all_records = _netload_recorder.all_records
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

def set_theme(theme):
    '''Set the theme of the website.'''
    
    return _theme.set_theme(theme)

def run_debug(app:flask.Flask):
    app.run(debug=True)

def run_env(app:flask.Flask, host="0.0.0.0", port=80):
    '''use gevent to run the server'''

    from gevent import pywsgi
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()

if __name__ == '__main__':
    
    config = ServerConfig.load("./config.json")
    if not config.is_valid:
        print("invalid server config")
    else:

        print(f"run server at {config.server_addr}")
        app = flask.Flask(__name__)
        load_base_routes(app)
        load_bug_collector(app, config)
        if config.debug_mode:
            run_debug(app)
        else:
            run_env(app, config.host, config.port)