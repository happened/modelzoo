import json
import os.path

from aiges.types import *

try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField
from aiges.utils.log import log

# 导入inference.py中的依赖包

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = ImageBodyField(key="img", path="test_data/0.png")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key=b"number")


class Wrapper(WrapperBase):
    serviceId = "mnist"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()
    model = None

    def __init__(self):
        super().__init__()
        self.transform = None
        self.device = None

    def wrapperInit(self, config: {}) -> int:
        print("wrapper init")
        return 0

    def wrapperOnceExec(self, params: {}, reqData: DataListCls) -> Response:
        # 使用Response封装result
        res = Response()
        resd = ResponseData()
        resd.key = "img"
        resd.type = DataText
        resd.status = Once
        resd.data = "hello world"
        resd.len = len(resd.data)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "user error defined here"
        return ""

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass
