from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from typing import List,Tuple

from ._cons import *
from ._utils import *
from ._bug import *
from _gdt_logger import GDTLogger

class _GDTDataUtils:
    
    @staticmethod
    def get_mongo_client(dblink:str) -> MongoClient:
        '''try to link to mongodb and get mongo client'''

        if dblink is None or len(dblink) == 0:
            return None

        try:
            # test if connection is valid
            _client = MongoClient(dblink)
            _client.admin.command("ping")
            return _client
        
        except ConnectionFailure as e:
            # connection failure
            return None

class GDTMongoClient:
    '''provide game data tracker apis'''

    def __init__(self, dblink:str):
    
        self.client = _GDTDataUtils.get_mongo_client(dblink)
        if self.client is None:
            raise SystemError(f"connect to mongodb \"{dblink}\" failed. check if mongodb is running or dblink is correct")

    @property
    def all_database_names(self) -> List[str]:
        '''get all table names'''

        return self.client.list_database_names()
    
    def get_database(self, name:str) -> Database:
        '''get or create target database'''

        if name is None or len(name) == 0:
            return None

        _database = self.client.get_database(name)
        return _database

class GDTMongoHandleBase:
    '''数据对接API基类'''

    def __init__(self, database: Database):
        
        if database is None:
            raise ValueError("database shouldn't be None")
        
        self.__database = database
        self.__current_test_plan_id = self._load_current_plan()

    def _load_current_plan(self) -> str:
        '''加载当前的测试计划ID'''

        collection = self.__database.get_collection(GDTCollections.TABLE_CURRENT_PLAN)
        _current_plan = collection.find_one()
        if _current_plan is None:
            return None
        return _current_plan.get(GDTFields.UNI_CURRENT_PLAN_ID, None)
    
    @property
    def is_current_plan_set(self):
        '''检查是否已经设立了当前的测试计划'''
        return self.__current_test_plan_id is not None
    
    @property
    def current_plan(self):
        '''获取当前的测试计划ID'''
        if self.__current_test_plan_id is None:
            return ""
        return self.__current_test_plan_id
    
    @property
    def all_test_plan_names(self) -> List[str]:
        '''获取所有的测试计划'''
        collection = self.__database.get_collection(GDTCollections.TABLE_ALL_PLANS)
        _plans = collection.find()
        return [plan[GDTFields.TEST_PLAN_NAME] for plan in _plans]
    
    @property
    def all_test_plans(self) -> List[dict]:
        '''获取所有的测试计划详细信息'''

        collection = self.__database.get_collection(GDTCollections.TABLE_ALL_PLANS)
        _plans = collection.find().sort(GDTFields.DATA_TIMESTAMP, -1)
        return [{
            GDTFields.TEST_PLAN_NAME: plan[GDTFields.TEST_PLAN_NAME],
            GDTFields.TEST_PLAN_TITLE: plan[GDTFields.TEST_PLAN_TITLE],
            GDTFields.TEST_PLAN_DESCRIPTION: plan[GDTFields.TEST_PLAN_DESCRIPTION],
            GDTFields.TEST_PLAN_DATE: plan[GDTFields.TEST_PLAN_DATE],
            GDTFields.TEST_PLAN_CREATOR: plan[GDTFields.TEST_PLAN_CREATOR]
        } for plan in _plans]
    
    def set_current_plan(self, name:str) -> bool:
        '''设置当前的测试计划'''

        if not is_valid_str(name):
            return False
        
        # check if target plan is exists
        collection = self.__database.get_collection(GDTCollections.TABLE_ALL_PLANS)
        _query = {GDTFields.TEST_PLAN_NAME: name}
        _plan = collection.find_one(_query)
        if _plan is None:
            return False
        
        # set current plan to mongodb recorder
        collection = self.__database.get_collection(GDTCollections.TABLE_CURRENT_PLAN)
        _current_plan = collection.find_one()
        if _current_plan is None:
            collection.insert_one({GDTFields.UNI_CURRENT_PLAN_ID: name})
        else:
            collection.update_one({}, {"$set": {GDTFields.UNI_CURRENT_PLAN_ID: name}})
        self.__current_test_plan_id = name
        return True
    
    def create_test_plan(self, name:str, title:str, description:str, creator:str) -> Tuple[bool, str]:
        '''创建测试计划，如果当前测试计划为空，则设置为当前测试计划
        @name: 测试计划名称
        @title: 测试计划标题
        @description: 测试计划描述
        @creator: 创建者'''

        _result = self._create_test_plan(name, title, description, creator)
        if _result[0] and self.__current_test_plan_id is None:
            self.set_current_plan(name)
        return _result
    
    def _create_test_plan(self, name:str, title:str, description:str, creator:str) -> Tuple[bool, str]:
        '''创建测试计划
        @title: 测试计划标题
        @description: 测试计划描述
        @remarks: 测试计划补充说明'''

        collection = self.__database.get_collection(GDTCollections.TABLE_ALL_PLANS)
        _query = {GDTFields.TEST_PLAN_NAME: name}

        # check if with same name in current collection 
        if collection.count_documents(_query) > 0:
            return (False, "duplicate test plan name")
                
        plan = {
            GDTFields.TEST_PLAN_NAME: name,
            GDTFields.TEST_PLAN_TITLE: title,
            GDTFields.TEST_PLAN_DESCRIPTION: description,
            GDTFields.TEST_PLAN_DATE: date_yymmdd(),
            GDTFields.TEST_PLAN_CREATOR: creator,
            GDTFields.DATA_TIMESTAMP: timestamp(),
        }

        _result = collection.insert_one(plan)
        if _result.acknowledged:
            return (True, "test plan created successfully")
        return (False, "test plan created failed due to unknown reason")

    # def _pack_data(self, data:dict) -> dict:
    #     '''将给定的数据按照测试计划打包，并附加日期后返回'''

    #     if not isinstance(data, dict) or self.__current_test_plan_id is None:
    #         return None
        
    #     _client_data = data.copy()
    #     _result = {
    #         GDTFields.DATA_PLAN_ID: self.__current_test_plan_id,
    #         GDTFields.DATA_DATE: date_yymmdd(),
    #         GDTFields.DATA_CLIENT_DATA: _client_data
    #     }
    #     return _result
    
    # def _pack_many_data(self, datas:List[dict]) -> List[dict]:
    #     '''将给定的数据列表按照测试计划打包，并附加日期后返回'''

    #     if not isinstance(datas, list) or self.__current_test_plan_id is None:
    #         return None
        
    #     _date = date_yymmdd()
    #     _result = []
    #     for data in datas:
    #         _client_data = data.copy()
    #         _result.append({
    #             GDTFields.DATA_PLAN_ID: self.__current_test_plan_id,
    #             GDTFields.DATA_DATE: _date,
    #             GDTFields.DATA_CLIENT_DATA: _client_data
    #         })
    #     return _result
    
    # def insert_one(self, collection_name:str, client_data:dict) -> bool:
    #     '''try insert single data'''

    #     _data = self._pack_data(client_data)
    #     if _data is None:
    #         return False
        
    #     collection = self.__database.get_collection(collection_name)
    #     _result = collection.insert_one(_data)
    #     return _result.acknowledged
        
    # def insert_many(self, collection_name:str, client_datas:List[dict]) -> bool:
    #     '''try insert multiple data'''

    #     _datas = self._pack_many_data(client_datas)
    #     if _datas is None:
    #         return False
        
    #     collection = self.__database.get_collection(collection_name)
    #     _result = collection.insert_many(_datas)
    #     return _result.acknowledged
    
    def bug_exception_count(self, query:dict={}) -> int:
        '''获取异常总数量'''

        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        return collection.count_documents(query)
    
    def bug_exception_exists(self, query:dict) -> bool:
        '''检查异常是否存在'''

        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        result = collection.find_one(query)
        if result is None:
            return False
        
        # update count and return
        _id = result[GDTFields._SPEC_MONGODB_ID]
        _count = result.get(GDTFields.DATA_COUNT, 1) + 1
        collection.update_one({GDTFields._SPEC_MONGODB_ID: _id}, {"$set": {GDTFields.DATA_COUNT: _count, GDTFields.BUG_REPORT_HANDLED: False}})
        return True

    def insert_bug_exception(self, data) -> bool:
        '''插入异常信息
        @data: 异常信息
        @return: 是否插入成功'''

        # data.setdefault(GDTFields.DATA_PLAN_ID, self.__current_test_plan_id)
        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        _result = collection.insert_one(data)
        return _result.acknowledged

    def get_bug_exceptions(self, query={}) -> List[dict]:
        '''获取所有的符合条件的异常信息'''

        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        _result = []
        for data in collection.find(query):
            _display_data = GDTBugUtils._get_bug_display(data)
            if _display_data is not None:
                _result.append(_display_data)
        return _result
    
    def get_bug_exceptions_as_page(self, index, page_count, query={}) -> List[dict]:
        '''获取第N页的异常信息(全部)'''

        if index < 0 or page_count <= 0:
            return []
        
        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        _result = []
        for data in collection.find(query).skip(index * page_count).limit(page_count):
            _display_data = GDTBugUtils._get_bug_display(data)
            if _display_data is not None:
                _result.append(_display_data)
        return _result
    
    def update_bug_exception_handle_status(self, _id, handled:bool) -> bool:
        ''''''

        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        _query = {GDTFields._SPEC_MONGODB_ID: ObjectId(_id)}
        _result = collection.update_one(_query, {"$set": {GDTFields.BUG_REPORT_HANDLED: handled}})
        return _result.acknowledged
    

    def get_bug_exception(self, _id) -> bool:
        '''获取异常信息'''

        collection = self.__database.get_collection(GDTCollections.TABLE_BUG_REPORT_EXCEPTION)
        _query = {GDTFields._SPEC_MONGODB_ID: ObjectId(_id)}
        _result = collection.find_one(_query)
        return _result


class NetLoadRecorder:
    '''负载记录器
    @2024.09.10 目前仅记录服务器的总访问次数'''

    def __init__(self, logger: GDTLogger, database: Database) -> None:

        if database is None:
            raise GameDataTrackerError("Database shouldn't be None")
        
        if logger is None:
            raise GameDataTrackerError("Logger shouldn't be None")
        self.__logger = logger
        self.__database = database
        self.__date = date_yymmdd()
        self.__total_visit_times = self._read(self.__date)
        self.__buffer = {}

    @property
    def result(self):
        '''返回当前的结果数据'''

        total, average, recent = self._recalculate_data_load()
        collection = self.__database.get_collection(GDTCollections.TABLE_NETLOAD_RESULT)
        yesterday = date_yesterday()

        # 昨天的最终统计数据
        _yesterday_record = collection.find_one({GDTFields.DATA_DATE: yesterday})
        if _yesterday_record is None:
            return {
                GDTFields.NETLOAD_RESULT_TOTAL: total,
                GDTFields.NETLOAD_RESULT_AVERAGE: average,
                GDTFields.NETLOAD_RESULT_RECENT: recent,
                GDTFields.NETLOAD_RESULT_TOTAL_ERR: total,
                GDTFields.NETLOAD_RESULT_AVERAGE_ERR: average,
                GDTFields.NETLOAD_RESULT_RECENT_ERR: recent
            }
        
        # 昨天的统计数据
        _yesterday_total = _yesterday_record[GDTFields.NETLOAD_RESULT_TOTAL]
        _yesterday_average = _yesterday_record[GDTFields.NETLOAD_RESULT_AVERAGE]
        _yesterday_recent = _yesterday_record[GDTFields.NETLOAD_RESULT_RECENT]
        return {
            GDTFields.NETLOAD_RESULT_TOTAL: total,
            GDTFields.NETLOAD_RESULT_AVERAGE: average,
            GDTFields.NETLOAD_RESULT_RECENT: recent,
            GDTFields.NETLOAD_RESULT_TOTAL_ERR: total - _yesterday_total,
            GDTFields.NETLOAD_RESULT_AVERAGE_ERR: average - _yesterday_average,
            GDTFields.NETLOAD_RESULT_RECENT_ERR: recent - _yesterday_recent
        }

    @property
    def all_records(self):
        '''返回所有的记录'''

        collection = self.__database.get_collection(GDTCollections.TABLE_NETLOAD)
        _records = collection.find({GDTFields.DATA_DATE: {"$ne": self.__date}})
        _history_records = [(record[GDTFields.DATA_DATE], record[GDTFields.NETLOAD_DATE_VISIT_COUNT]) for record in _records]
        _history_records.append((self.__date, self.__total_visit_times))
        return _history_records

    def _read(self, date:str) -> int:
        '''读取给定日期的访问量'''

        collection = self.__database.get_collection(GDTCollections.TABLE_NETLOAD)
        _query = {GDTFields.DATA_DATE: date}
        _result = collection.find_one(_query)
        if _result is not None:
            _count = _result.get(GDTFields.NETLOAD_DATE_VISIT_COUNT, 0)
            return _count
        return 0
    
    def _upload(self, date:str, count:int) -> bool:
        '''上传给定日期的访问量'''

        collection = self.__database.get_collection(GDTCollections.TABLE_NETLOAD)
        _query = {GDTFields.DATA_DATE: date}
        _result = collection.update_one(_query, {"$set": {GDTFields.NETLOAD_DATE_VISIT_COUNT: count}}, upsert=True)
        return _result.acknowledged
    
    def _upload_buffer(self):
        '''上传缓存数据'''

        if len(self.__buffer) == 0:
            return
        
        invalid_buffer = {}
        collection = self.__database.get_collection(GDTCollections.TABLE_NETLOAD)
        for date, count in self.__buffer.items():
            result = collection.insert_one({date: count})
            if not result.acknowledged:
                self.__logger.error(f"failed to upload buffer data: {date}:{count}")
                invalid_buffer[date] = count
        self.__buffer = invalid_buffer

    def _upload_result(self):
        '''上传结果数据'''

        # record result
        total, average, recent = self._recalculate_data_load()
        collection = self.__database.get_collection(GDTCollections.TABLE_NETLOAD_RESULT)
        collection.update_one({GDTFields.DATA_DATE: self.__date},{"$set": {
            GDTFields.NETLOAD_RESULT_TOTAL: total,
            GDTFields.NETLOAD_RESULT_AVERAGE: average,
            GDTFields.NETLOAD_RESULT_RECENT: recent
        }}, upsert=True)


    def _recalculate_data_load(self) -> dict:
        '''重新计算数据负载'''

        # (date, count)
        _all_records = self.all_records

        # 先统计总数居
        _total_count = 0
        for _record in _all_records:
            _total_count += _record[1]

        # 统计平均数据
        _average_count = _total_count // len(_all_records)

        # 统计最近一周的总数居
        if len(_all_records) > 7:
            _recent_records = _all_records[-7:]
            _recent_total_count = 0
            for _record in _recent_records:
                _recent_total_count += _record[1]
        else:
            _recent_total_count = _total_count

        return (_total_count, _average_count, _recent_total_count)
        

    def record(self):
        '''记录一次访问'''

        _current_date = date_yymmdd()
        if self.__date == _current_date:
            self.__total_visit_times += 1
            self._upload_buffer()
            return
        
        # new date
        if not self._upload(self.__date, self.__total_visit_times):
            # upload failed
            self.__buffer[self.__date] = self.__total_visit_times
            self.__logger.error(f"failed to upload visit count: {self.__date}:{self.__total_visit_times}")

        self._upload_result()

        # reset
        self.__total_visit_times = 1
        self.__date = _current_date

    def flush(self):
        '''退出时记录当前的数据'''

        self._upload(self.__date, self.__total_visit_times)
        self._upload_result()


if __name__ == '__main__':
    '''test'''

    _client = GDTMongoClient("mongodb://localhost:27017/")