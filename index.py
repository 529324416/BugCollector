import gevent
from flask import Flask, render_template, request, make_response
from blueprints.doloctown import *
from gdt_database import *
from _gdt_logger import GDTLogger
import _theme

import os
import atexit
import _cookies

# create base helpers
_logger = GDTLogger("./server_logs")
_mongo_client = GDTMongoClient("mongodb://localhost:27017/")
_netload_recorder = NetLoadRecorder(_logger, _mongo_client.get_database("doloctown"))
_doloctown_api = GDTMongoHandleBase(_mongo_client.get_database("doloctown"))

# create flask app
app = Flask(__name__)
_bug_collector = BugCollector_Exception(_doloctown_api, _netload_recorder, import_name=__name__)
app.register_blueprint(_bug_collector)

@app.route('/')
def index():
    '''首页'''

    return render_template('index.html', theme=_theme.fetch_theme(), cookies=_bug_collector.cookies)

@app.route('/server_status/netload')
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

@app.route('/server_status/netload/chart')
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

@app.route('/utils/set_theme/<theme>')
def set_theme(theme):
    '''Set the theme of the website.'''
    
    return _theme.set_theme(theme)
    

# 退出时将现有负载数据上传至数据库
if os.getenv('WERKZEUG_RUN_MAIN') == 'true':
    atexit.register(_netload_recorder.dispose)


def main_debug():
    app.run(debug=True)

def main_env(host="0.0.0.0", port=80):
    '''use gevent to run the server'''

    from gevent import pywsgi
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()


if __name__ == '__main__':
    main_env()