# 命令脚本，用于创建测试计划
# 用法：修改该脚本中的参数并启动即可

import pymongo
from gdt_database.data import GDTMongoHandleBase
from gdt_database._cons import *


def create_test_plan(url, game, pname, ptitle, pdescription, pcreator, enable_plan=True):
    '''创建测试计划
    :param url: MongoDB URL
    :param pname: 测试计划名称
    :param ptitle: 测试计划标题
    :param pdescription: 测试计划描述
    :param pcreator: 创建人
    '''

    try:
        _client = pymongo.MongoClient(url)
        _database = _client.get_database(game)
    except Exception as e:
        print("连接数据库失败！")
        print(e)
        return
    
    _handle = GDTMongoHandleBase(_database)
    if _handle.create_test_plan(pname, ptitle, pdescription, pcreator):
        if enable_plan:
            _handle.set_current_plan(pname)
        print("创建测试计划成功！")
    else:
        print("创建测试计划失败！")


if __name__ == "__main__":
    # 连接数据库的URL
    _url = "mongodb://localhost:27017/"
    # 游戏名称
    _game = "doloctown"
    # 测试计划名称
    _pname = "test_plan_1"
    # 测试计划标题
    _ptitle = "测试计划标题"
    # 测试计划描述
    _pdescription = "测试计划描述"
    # 创建人
    _pcreator = "admin"

    create_test_plan(_url, _game, _pname, _ptitle, _pdescription, _pcreator)