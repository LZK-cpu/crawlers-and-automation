import time
from datetime import datetime

from wxauto import *


start=time.time()
wx = WeChat()
session_list = wx.GetSessionList()
print(session_list)
msg = '这不是我  '+str(datetime.now())
who = '⁺ʚ绿茶重度依赖ɞ₊'
wx.SendMsg(msg, who)
end=time.time()

# msg = '运行  '+str(end-start)
# who = '梓'
# wx.SendMsg(msg, who)