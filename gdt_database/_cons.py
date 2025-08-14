


class GDTCollections:
    '''通用表名'''

    # 关于测试计划
    TABLE_CURRENT_PLAN = "__spec__current_plan"                 # 当前测试计划所在的集合名
    TABLE_ALL_PLANS = "__spec__plans"                           # 所有测试计划
    
    # 关于网络负载
    TABLE_NETLOAD = "__spec__netload"                           # 网络负载数据
    TABLE_NETLOAD_RESULT = "__spec__netload_result"             # 网络负载结果数据

    # 关于BUG收集
    TABLE_BUG_REPORT_EXCEPTION = "__spec__bug_report_exception" # 关于BUG收集


class GDTFields:
    '''通用字段名'''

    _SPEC_MONGODB_ID = "_id"

    UNI_CURRENT_PLAN_ID = "__current_tp_id"

    # 关于数据负载
    NETLOAD_DATE_VISIT_COUNT = "date_visit_count"
    NETLOAD_RESULT = "result"
    NETLOAD_RESULT_TOTAL = "total"
    NETLOAD_RESULT_AVERAGE = "average"
    NETLOAD_RESULT_RECENT = "recent"
    NETLOAD_RESULT_TOTAL_ERR = "total_err"
    NETLOAD_RESULT_AVERAGE_ERR = "average_err"
    NETLOAD_RESULT_RECENT_ERR = "recent_err"

    # 关于BUG收集
    BUG_REPORT_DATE = "date"
    BUG_REPORT_HANDLED = "handled"
    BUG_REPORT_EXCEPTION_DETAIL = "exception"

    # 关于BUG会话
    BUG_SESSION_ID = "id"
    BUG_SESSION_RECORDS = "records"
    BUG_SESSION_COUNT = "count"
    BUG_SESSION_MESSAGE = "message"
    BUG_SESSION_STATUS = "status"
    BUG_SESSION_REJECT_REPORT = "reject"
    BUG_SESSION_UPDATE_TIME = "update_time"
    BUG_SESSION_UPDATE_TIMESTAMP = "update_timestamp"  # BUG会话的更新时间戳
    BUG_SESSION_UPDATE_VERSION = "update_version"  # BUG会话的最新版本号


    # 关于测试计划
    TEST_PLAN_ID = "test_plan_id"
    TEST_PLAN_NAME = "name"
    TEST_PLAN_TITLE = "title"
    TEST_PLAN_DESCRIPTION = "description"
    TEST_PLAN_DATE = "date"
    TEST_PLAN_CREATOR = "creator"
    
    # 关于单个数据
    # DATA_CLIENT_DATA = "client_data"
    # DATA_PLAN_ID = "__tpid"
    DATA_DATE = "date"
    DATA_IP = "ip"
    # DATA_DATE_NUM = "__date_num"
    DATA_TIMESTAMP = "timestamp"
    # DATA_COUNT = "__count"