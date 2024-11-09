from gdt_database._cons import *


class GDTBugUtils:
    

    '''BUG-异常结构
        {
            "name": "Exception",
            "message": "Test Exception",
            "stacktrace": "RedSaw.Web.WebOperationHandle.Test () (at Assets/Scripts/RedSaw/Web/WebOperationHandle.cs:23)\nSystem.Reflection.RuntimeMethodInfo.Invoke (System.Object obj, System.Reflection.BindingFlags invokeAttr, System.Reflection.Binder binder, System.Object[] parameters, System.Globalization.CultureInfo culture) (at <75633565436c42f0a6426b33f0132ade>:0)\nRethrow as TargetInvocationException: Exception has been thrown by the target of an invocation.\nSystem.Reflection.RuntimeMethodInfo.Invoke (System.Object obj, System.Reflection.BindingFlags invokeAttr, System.Reflection.Binder binder, System.Object[] parameters, System.Globalization.CultureInfo culture) (at <75633565436c42f0a6426b33f0132ade>:0)\nSystem.Reflection.MethodBase.Invoke (System.Object obj, System.Object[] parameters) (at <75633565436c42f0a6426b33f0132ade>:0)\nSirenix.OdinInspector.Editor.Drawers.DefaultMethodDrawer.InvokeMethodInfo (System.Reflection.MethodInfo methodInfo) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/Misc Drawers/DefaultMethodDrawer.cs:517)\nUnityEngine.Debug:LogException(Exception)\nSirenix.OdinInspector.Editor.Drawers.DefaultMethodDrawer:InvokeMethodInfo(MethodInfo) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/Misc Drawers/DefaultMethodDrawer.cs:542)\nSirenix.OdinInspector.Editor.Drawers.DefaultMethodDrawer:InvokeButton() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/Misc Drawers/DefaultMethodDrawer.cs:418)\nSirenix.OdinInspector.Editor.Drawers.DefaultMethodDrawer:DrawNormalButton() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/Misc Drawers/DefaultMethodDrawer.cs:272)\nSirenix.OdinInspector.Editor.Drawers.DefaultMethodDrawer:DrawPropertyLayout(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/Misc Drawers/DefaultMethodDrawer.cs:184)\nSirenix.OdinInspector.Editor.OdinDrawer:DrawProperty(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/OdinDrawer.cs:109)\nSirenix.OdinInspector.Editor.InspectorProperty:Draw(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Core/InspectorProperty.cs:831)\nSirenix.OdinInspector.Editor.InspectorProperty:Draw() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Core/InspectorProperty.cs:719)\nSirenix.OdinInspector.Editor.Drawers.UnityObjectRootDrawer`1:DrawPropertyLayout(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/Value Drawers/UnityObjectRootDrawer.cs:60)\nSirenix.OdinInspector.Editor.OdinDrawer:CallNextDrawer(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/OdinDrawer.cs:155)\nSirenix.OdinInspector.Editor.Drawers.FixBrokenUnityObjectWrapperDrawer`1:DrawPropertyLayout(GUIContent) (at Assets/Plugins/Sirenix/Odin Inspector/Scripts/Editor/FixBrokenUnityObjectWrapperDrawer.cs:41)\nSirenix.OdinInspector.Editor.OdinDrawer:DrawProperty(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/OdinDrawer.cs:109)\nSirenix.OdinInspector.Editor.InspectorProperty:Draw(GUIContent) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Core/InspectorProperty.cs:831)\nSirenix.OdinInspector.Editor.PropertyTree:DrawProperties() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Core/PropertyTree.cs:499)\nSirenix.OdinInspector.Editor.PropertyTree:Draw(Boolean) (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Core/PropertyTree.cs:388)\nSirenix.OdinInspector.Editor.OdinEditor:DrawTree() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/OdinEditor.cs:93)\nSirenix.OdinInspector.Editor.OdinEditor:DrawOdinInspector() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/OdinEditor.cs:246)\nSirenix.OdinInspector.Editor.OdinEditor:OnInspectorGUI() (at C:/Repos/sirenix-development-framework/Sirenix Solution/Sirenix.OdinInspector.Editor/Drawers/OdinEditor.cs:85)\nUnityEngine.GUIUtility:ProcessEvent(Int32, IntPtr, Boolean&)\n",
            "final_trigger_point":{
                "code":"",
                "filepath":"",
                "line":0
            }
            "trigger_points": [
                {
                "code": "RedSaw.Web.WebOperationHandle.Test ()",
                "filepath": "Assets/Scripts/RedSaw/Web/WebOperationHandle.cs",
                "line": 23
                },
                {
                "code": "System.Reflection.RuntimeMethodInfo.Invoke (System.Object obj, System.Reflection.BindingFlags invokeAttr, System.Reflection.Binder binder, System.Object[] parameters, System.Globalization.CultureInfo culture)",
                "filepath": "<75633565436c42f0a6426b33f0132ade>",
                "line": 0
                },
                // ...
            ],
            "player_log": "...long text",
            "console_log":[
                ["message", "#ffffff"],
                ["message", "#ffffff"],
                ["message", "#ffffff"],
                //...
            ],
            "version": "0.86.16",
            "device": {
                "dvc_code": "29da5f481dff59c7ba7963bd3aad06b27e2ed020",
                "dvc_type": "Desktop",
                "os": "Windows 11  (10.0.22631) 64bit"
            },
        }
    '''

    KEY_NAME = "name"
    KEY_MESSAGE = "message"
    KEY_STACKTRACE = "stacktrace"
    KEY_TRIGGER_POINTS = "trigger_points"
    KEY_PLAYER_LOG = "player_log"
    KEY_DEVICE = "device"
    KEY_FINAL_TRIGGER_POINT = "final_trigger_point"
    KEY_CONSOLE_LOG = "console_log"
    KEY_VERSION = "version"

    KEY_DVC_CODE = "dvc_code"
    KEY_DVC_TYPE = "dvc_type"
    KEY_OS = "os"

    KEY_HANDLED = "handled"

    @staticmethod
    def _get_bug_display(origin_data):
        '''获取异常报告的显示信息
        {...} -> {
            "id":"mongodb_id"
            "except_info":"",
            "except_pos":"",
            "date":"",
            "plan_id":"",
            "version":"",
            "handled":False/True,
            "count":0
        }
        '''

        _id = origin_data.get(GDTFields._SPEC_MONGODB_ID)
        _name = origin_data.get(GDTBugUtils.KEY_NAME)
        _message = origin_data.get(GDTBugUtils.KEY_MESSAGE)
        _except_info = "{}: {}".format(_name, _message)

        _trigger_points = origin_data.get(GDTBugUtils.KEY_TRIGGER_POINTS)
        if len(_trigger_points) == 0:
            _except_pos = ""
        else:
            _first = _trigger_points[0]
            _except_pos = "{}({})".format(_first.get("code"), _first.get("filepath"))

        _date = origin_data.get(GDTFields.DATA_DATE)
        _plan_id = origin_data.get(GDTFields.DATA_PLAN_ID)
        # _device = origin_data.get(GDTBugUtils.KEY_DEVICE)
        # _device_info = "{}({})".format(_device.get(GDTBugUtils.KEY_DVC_TYPE), _device.get(GDTBugUtils.KEY_OS))
        return {
            "id": _id,
            "except_info": _except_info,
            "except_pos": _except_pos,
            "date": _date,
            "plan_id": _plan_id,
            # "device_info": _device_info,
            "version": origin_data.get(GDTBugUtils.KEY_VERSION, "unknown"),
            "handled": origin_data.get(GDTFields.BUG_REPORT_HANDLED, False),
            "count": origin_data.get(GDTFields.DATA_COUNT, 1)
        }

    @staticmethod
    def _validate_device(data:dict) -> bool:
        '''验证设备信息是否有效'''

        if data is None or not isinstance(data, dict):
            return False
        
        _dvc_code = data.get(GDTBugUtils.KEY_DVC_CODE)
        if _dvc_code is None or not isinstance(_dvc_code, str):
            return False
        
        _dvc_type = data.get(GDTBugUtils.KEY_DVC_TYPE)
        if _dvc_type is None or not isinstance(_dvc_type, str):
            return False
        
        _os = data.get(GDTBugUtils.KEY_OS)
        if _os is None or not isinstance(_os, str):
            return False
        
        return True
        
    @staticmethod
    def validate_bug_exception(data:dict) -> bool:
        '''验证异常报告的数据结构是否有效'''
        
        if data is None or not isinstance(data, dict):
            return False
        
        _name = data.get(GDTBugUtils.KEY_NAME)
        if _name is None or not isinstance(_name, str):
            return False
        
        _message = data.get(GDTBugUtils.KEY_MESSAGE)
        if _message is None or not isinstance(_message, str):
            return False
        
        _final_trigger_point = data.get(GDTBugUtils.KEY_FINAL_TRIGGER_POINT)
        if _final_trigger_point is None or not isinstance(_final_trigger_point, dict):
            return False
        
        _stacktrace = data.get(GDTBugUtils.KEY_STACKTRACE)
        if _stacktrace is None or not isinstance(_stacktrace, str):
            return False
        
        _trigger_points = data.get(GDTBugUtils.KEY_TRIGGER_POINTS)
        if _trigger_points is None or not isinstance(_trigger_points, list):
            return False
        
        _player_log = data.get(GDTBugUtils.KEY_PLAYER_LOG)
        if _player_log is None or not isinstance(_player_log, str):
            return False
        
        _console_log = data.get(GDTBugUtils.KEY_CONSOLE_LOG)
        if _console_log is None or not isinstance(_console_log, list):
            return False
        
        _version = data.get(GDTBugUtils.KEY_VERSION)
        if _version is None or not isinstance(_version, str):
            return False
        
        _device = data.get(GDTBugUtils.KEY_DEVICE)
        return GDTBugUtils._validate_device(_device)
    
    @staticmethod
    def is_error_line(line:str) -> bool:
        '''判断是否为异常报告的错误行'''
        
        return line.startswith("at ") or line.startswith("System.") or line.startswith("UnityEngine.")