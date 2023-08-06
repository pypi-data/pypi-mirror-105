from lsyflasksdkcore.schema import Schema
from marshmallow import fields, validate, post_load

from lsyflaskmicroapp_ys7.entitys import YsYuntaiControlQuery, YsLiveAddressQuery, YsSceneSwitchSetQuery


class YsYuntaiStartQuerySchema(Schema):
    """
    开始云台控制query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号")
    direction = fields.Int(required=True, validate=validate.OneOf((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
                           description="操作命令：0-上，1-下，2-左，3-右，4-左上，5-左下，6-右上，7-右下，8-放大，9-缩小，10-近焦距，11-远焦距")
    speed = fields.Int(required=True, validate=validate.OneOf((0, 1, 2)), description="云台速度：0-慢，1-适中，2-快，海康设备参数不可为0")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsYuntaiStopQuerySchema(Schema):
    """
    停止云台控制query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号")
    direction = fields.Int(required=False, validate=validate.OneOf((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
                           description="提示：建议停止云台接口带方向参数,操作命令：0-上，1-下，2-左，3-右，4-左上，5-左下，6-右上，7-右下，8-放大，9-缩小，10-近焦距，11-远焦距")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsYuntaiMirrorQuerySchema(Schema):
    """
    镜像翻转query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号")
    command = fields.Int(required=True, validate=validate.Range((0, 1, 2)),
                         description="镜像方向：0-上下, 1-左右, 2-中心")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsYuntaiAddPointQuerySchema(Schema):
    """
    添加预置点query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsYuntaiMovePointQuerySchema(Schema):
    """
    调用预置点query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号")
    index = fields.Int(required=True, validate=validate.Range(1, 13), description="预置点，C6设备预置点是1-12")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsYuntaiClearPointQuerySchema(Schema):
    """
    清除预置点query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号")
    index = fields.Int(required=True, validate=validate.Range(1, 13), description="预置点，C6设备预置点是1-12")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsDeviceInfoQuerySchema(Schema):
    """获取单个设备信息"""
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsDeviceInfoRspSchema(Schema):
    """获取单个设备信息返回值"""
    deviceSerial = fields.Str(data_key="device_serial", description="设备序列号")
    deviceName = fields.Str(data_key="device_name", description="设备名称")
    model = fields.Str(description="设备型号，如CS-C2S-21WPFR-WX")
    status = fields.Int(description="在线状态：0-不在线，1-在线")
    defence = fields.Int(description="具有防护能力的设备布撤防状态：0-睡眠，8-在家，16-外出，普通IPC布撤防状态：0-撤防，1-布防")
    isEncrypt = fields.Int(data_key="is_encrypt", description="是否加密：0-不加密，1-加密")
    alarmSoundMode = fields.Int(data_key="alarm_sound_mode", description="告警声音模式：0-短叫，1-长叫，2-静音")
    offlineNotify = fields.Int(data_key="offline_notify", description="设备下线是否通知：0-不通知 1-通知")
    category = fields.Str(description="设备大类")
    updateTime = fields.Str(data_key="update_time", description="更新时间")
    netType = fields.Str(data_key="net_type", description="网络类型，如有线连接wire")
    signal = fields.Str(description="信号强度(%)")


class YsCaptureQuerySchema(Schema):
    """
    设备抓拍图片
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号，IPC设备填写1")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsLiveAddressQuerySchema(Schema):
    """
    获取播放地址
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    channel_no = fields.Int(required=True, description="通道号,，非必选，默认为1")
    code = fields.Str(required=False, description="ezopen协议地址的设备的视频加密密码")
    expire_time = fields.Int(required=False, description="过期时长，单位秒；针对hls/rtmp设置有效期，相对时间；30秒-7天")
    protocol = fields.Int(required=False, description="流播放协议，1-ezopen、2-hls、3-rtmp，默认为1")
    quality = fields.Int(required=False, description="视频清晰度，1-高清（主码流）、2-流畅（子码流）")
    start_time = fields.Str(required=False, description="ezopen协议地址的本地录像/云存储录像回放开始时间,示例：2019-12-01 00:00:00")
    stop_time = fields.Str(required=False, description="ezopen协议地址的本地录像/云存储录像回放开始时间,示例：2019-12-01 00:00:00")
    type = fields.Str(required=False, default="1", description="ezopen协议地址的类型，1-预览，2-本地录像回放，3-云存储录像回放，非必选，默认为1")

    @post_load
    def make(self, data, **kwargs):
        return YsLiveAddressQuery().__fill__(**data)


class YsLiveAddressRspSchema(Schema):
    """
    获取播放地址返回值
    """
    id = fields.Str(required=True, description="状态描述")
    url = fields.Str(required=True, description="直播地址")
    expireTime = fields.Str(required=False, data_key="expire_time", description="直播地址有效期。expireTime参数为空时该字段无效")


class YsSceneSwitchStatusQuerySchema(Schema):
    """
    获取镜头遮蔽开关状态Query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")

    @post_load
    def make(self, data, **kwargs):
        return YsYuntaiControlQuery().__fill__(**data)


class YsSceneSwitchStatusRspSchema(Schema):
    """
    获取镜头遮蔽开关状态Rsp
    """
    deviceSerial = fields.Str(data_key="device_serial", description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    enable = fields.Int(description="状态：0-关闭，1-开启")
    channelNo = fields.Int(data_key="channel_no", description="通道号，不传表示设备本身")


class YsSceneSwitchSetQuerySchema(Schema):
    """
    设置镜头遮蔽开关Query
    """
    device_serial = fields.Str(required=True, description="设备序列号,存在英文字母的设备序列号，字母需为大写")
    enable = fields.Int(required=True, description="状态：0-关闭，1-开启")
    channel_no = fields.Int(required=False, description="通道号，不传表示设备本身")

    @post_load
    def make(self, data, **kwargs):
        return YsSceneSwitchSetQuery().__fill__(**data)
