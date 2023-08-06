import logging
import string
import time

import requests
from cacheout import Cache
from flask import current_app
from lsyflasksdkcore import sresponse, RequestQuery, eresponse
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.swagger import doc
from requests import RequestException
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_ys7.entitys import YsYuntaiControlQuery, YsLiveAddressQuery, YsSceneSwitchSetQuery
from lsyflaskmicroapp_ys7.error import AccessTokenError, get_err_msg
from lsyflaskmicroapp_ys7.schemas import YsYuntaiStartQuerySchema, YsYuntaiStopQuerySchema, YsYuntaiMirrorQuerySchema, \
    YsCaptureQuerySchema, YsLiveAddressQuerySchema, YsLiveAddressRspSchema, YsDeviceInfoQuerySchema, \
    YsDeviceInfoRspSchema, YsSceneSwitchStatusQuerySchema, YsSceneSwitchStatusRspSchema, YsSceneSwitchSetQuerySchema

logger = logging.getLogger(__name__)

bp = Blueprint('ys7_api', __name__)

cache = Cache(maxsize=256, ttl=7 * 24 * 3600, timer=time.time, default=None)


def get_access_token() -> str:
    """获取access token"""
    access_token = cache.get("access_token", None)
    if access_token:
        return access_token

    try:
        ys_token_get_url = current_app.config.get("YS_TOKEN_GET_URL", "")
        ys_app_key = current_app.config.get("YS_APP_KEY", "")
        ys_app_secret = current_app.config.get("YS_APP_SECRET", "")
        post_data = {
            "appKey": ys_app_key,
            "appSecret": ys_app_secret
        }

        data = requests.post(ys_token_get_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            access_token = data['data']['accessToken']
            cache.set("access_token", access_token)
            return access_token
        else:
            raise AccessTokenError(get_err_msg(rsp_code))
    except RequestException as ex:
        logger.error(ex)
        raise AccessTokenError("访问萤石云请求失败")


@bp.route('/token/get', methods=['POST'])
@doc.post("ys7", string.__name__, string.__name__)
def token():
    """根据appKey和secret获取accessToken"""
    try:
        access_token = get_access_token()
        return sresponse(data=access_token)
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")


@bp.route('device/ptz/start', methods=['POST'])
@doc.post("ys7", YsYuntaiStartQuerySchema.__name__)
def start():
    """开始云台控制"""
    query = RequestQuery(YsYuntaiStartQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data
        access_token = get_access_token()
        ys_start_url = current_app.config.get("YS_START_URL")

        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial,
            'channelNo': qd.channel_no,
            'direction': qd.direction,
            'speed': qd.speed,
        }
        data = requests.post(ys_start_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            return sresponse()
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/ptz/stop', methods=['POST'])
@doc.post("ys7", YsYuntaiStopQuerySchema.__name__)
def stop():
    """停止云台控制"""
    query = RequestQuery(YsYuntaiStopQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data
        access_token = get_access_token()
        ys_stop_url = current_app.config.get("YS_STOP_URL")

        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial,
            'channelNo': qd.channel_no
        }
        if qd.direction:
            post_data["direction"] = qd.direction

        data = requests.post(ys_stop_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            return sresponse()
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/ptz/mirror', methods=['POST'])
@doc.post("ys7", YsYuntaiStopQuerySchema.__name__)
def mirror():
    """镜像翻转"""
    query = RequestQuery(YsYuntaiMirrorQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data
        access_token = get_access_token()
        ys_mirror_url = current_app.config.get("YS_MIRROR_URL")

        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial,
            'channelNo': qd.channel_no,
            'command': qd.command
        }

        data = requests.post(ys_mirror_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            return sresponse()
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/info', methods=['POST'])
@doc.post("ys7", YsDeviceInfoQuerySchema.__name__, YsDeviceInfoRspSchema.__name__)
def device_info():
    """获取单个设备信息"""
    query = RequestQuery(YsDeviceInfoQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data
        access_token = get_access_token()
        ys_mirror_url = current_app.config.get("YS_DEVICE_INFO_URL")
        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial
        }

        rsp_data = requests.post(ys_mirror_url, data=post_data).json()
        rsp_code = rsp_data.get("code", 200)
        if rsp_code == "200":
            data = YsDeviceInfoRspSchema().dump(rsp_data['data'])
            return sresponse(data)
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/capture', methods=['POST'])
@doc.post("ys7", YsCaptureQuerySchema.__name__)
def capture():
    """设备抓拍图片"""
    query = RequestQuery(YsCaptureQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data

        cache_key = f"{qd.device_serial}_pic_url"
        pic_url = cache.get(cache_key, None)
        if pic_url:
            return sresponse(pic_url)

        access_token = get_access_token()
        ys_mirror_url = current_app.config.get("YS_CAPTURE_URL")
        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial,
            'channelNo': qd.channel_no
        }

        data = requests.post(ys_mirror_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            pic_url = data["data"]["picUrl"]
            cache.set(cache_key, pic_url, ttl=3600)
            return sresponse(pic_url)
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/capacity', methods=['POST'])
@doc.post("ys7", YsDeviceInfoQuerySchema.__name__)
def capacity():
    """根据设备序列号查询设备能力集"""
    query = RequestQuery(YsDeviceInfoQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data
        access_token = get_access_token()
        ys_url = current_app.config.get("YS_DEVICE_CAPACITY_URL")
        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial
        }

        data = requests.post(ys_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            return sresponse(data["data"])
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('v2/live/address/get', methods=['POST'])
@doc.post("ys7", YsLiveAddressQuerySchema.__name__, YsLiveAddressRspSchema.__name__)
def live_address():
    """获取直播地址"""
    query = RequestQuery(YsLiveAddressQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsLiveAddressQuery = query.data

        access_token = get_access_token()
        ys_url = current_app.config.get("YS_LIVE_ADDRESS_URL")
        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial
        }
        if qd.channel_no:
            post_data['channelNo'] = qd.channel_no
        if qd.code:
            post_data['code'] = qd.code
        if qd.expire_time:
            post_data['expireTime'] = qd.expire_time
        if qd.protocol:
            post_data['protocol'] = qd.protocol
        if qd.quality:
            post_data['quality'] = qd.quality
        if qd.start_time:
            post_data['startTime'] = qd.start_time
        if qd.stop_time:
            post_data['stopTime'] = qd.stop_time
        if qd.type:
            post_data['type'] = qd.type

        rsp_data = requests.post(ys_url, data=post_data).json()
        rsp_code = rsp_data.get("code", 200)
        if rsp_code == "200":
            data = YsLiveAddressRspSchema().dump(rsp_data["data"])
            return sresponse(data)
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/scene/switch/status', methods=['POST'])
@doc.post("ys7", YsSceneSwitchStatusQuerySchema.__name__, YsSceneSwitchStatusRspSchema.__name__)
def device_scene_switch_status():
    """获取镜头遮蔽开关状态"""
    query = RequestQuery(YsSceneSwitchStatusQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsYuntaiControlQuery = query.data
        access_token = get_access_token()
        ys_url = current_app.config.get("YS_SCENE_SWITCH_STATUS_URL")
        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial
        }

        rsp_data = requests.post(ys_url, data=post_data).json()
        rsp_code = rsp_data.get("code", 200)
        if rsp_code == "200":
            data = YsSceneSwitchStatusRspSchema().dump(rsp_data["data"])
            return sresponse(data)
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('device/scene/switch/set', methods=['POST'])
@doc.post("ys7", YsSceneSwitchSetQuerySchema.__name__, string.__name__)
def device_scene_switch_set():
    """设置镜头遮蔽开关"""
    query = RequestQuery(YsSceneSwitchSetQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    try:
        qd: YsSceneSwitchSetQuery = query.data

        access_token = get_access_token()
        ys_url = current_app.config.get("YS_SCENE_SWITCH_SET_URL")
        post_data = {
            'accessToken': access_token,
            'deviceSerial': qd.device_serial
        }
        if qd.channel_no:
            post_data['channelNo'] = qd.channel_no

        rsp_data = requests.post(ys_url, data=post_data).json()
        rsp_code = rsp_data.get("code", 200)
        if rsp_code == "200":
            return sresponse("")
        else:
            return eresponse(get_err_msg(rsp_code))
    except AccessTokenError as ex:
        logger.error(ex)
        return eresponse("获取AccessToken失败")
    except RequestException as ex:
        logger.error(ex)
        return eresponse("访问萤石云失败")
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
