from lsyflasksdkcore import AutoClass


class YsYuntaiControlQuery(AutoClass):
    """
    萤石云云台控制query
    """

    def __init__(self):
        self.device_serial: str = ""
        self.channel_no: int = 0
        self.direction: int = 0
        self.speed: int = 0
        self.command: int = 0
        self.index: int = 0


class YsLiveAddressQuery(AutoClass):
    """获取播放地址
    """

    def __init__(self):
        self.device_serial: str = ""
        self.channel_no: int = 0
        self.code: str = 0
        self.expire_time: int = 0
        self.protocol: int = 0
        self.quality: int = 0
        self.start_time: str = ""
        self.stop_time: str = ""
        self.type: str = ""


class YsSceneSwitchSetQuery(AutoClass):
    """设置镜头遮蔽开关Query
    """

    def __init__(self):
        self.device_serial: str = ""
        self.enable: int = 0
        self.channel_no: str = 0
