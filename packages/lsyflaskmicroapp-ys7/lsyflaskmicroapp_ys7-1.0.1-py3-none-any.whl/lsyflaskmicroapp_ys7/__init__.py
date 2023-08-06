from lsyflaskmicroapp_ys7 import apis


def init_app(app, url_prefix='/api/lapp'):
    app.config.setdefault('YS_TOKEN_GET_URL', 'https://open.ys7.com/api/lapp/token/get')
    app.config.setdefault('YS_START_URL', 'https://open.ys7.com/api/lapp/device/ptz/start')
    app.config.setdefault('YS_STOP_URL', 'https://open.ys7.com/api/lapp/device/ptz/stop')
    app.config.setdefault('YS_MIRROR_URL', 'https://open.ys7.com/api/lapp/device/ptz/mirror')
    app.config.setdefault('YS_MOVE_URL', 'https://open.ys7.com/api/lapp/device/preset/move')
    app.config.setdefault('YS_ADD_URL', 'https://open.ys7.com/api/lapp/device/preset/add')
    app.config.setdefault('YS_CAPTURE_URL', 'https://open.ys7.com/api/lapp/device/capture')
    app.config.setdefault('YS_LIVE_ADDRESS_URL', 'https://open.ys7.com/api/lapp/v2/live/address/get')
    app.config.setdefault('YS_DEVICE_INFO_URL', 'https://open.ys7.com/api/lapp/device/info')
    app.config.setdefault('YS_SCENE_SWITCH_STATUS_URL', 'https://open.ys7.com/api/lapp/device/scene/switch/status')
    app.config.setdefault('YS_SCENE_SWITCH_SET_URL', 'https://open.ys7.com/api/lapp/device/scene/switch/set')
    app.config.setdefault('YS_DEVICE_CAPACITY_URL', 'https://open.ys7.com/api/lapp/device/capacity')

    if not app.config.get("YS_APP_KEY", None):
        raise Exception("YS_APP_KEY NOT IN CONFIG")

    if not app.config.get("YS_APP_SECRET", None):
        raise Exception("YS_APP_SECRET NOT IN CONFIG")

    app.register_blueprint(apis.bp, url_prefix=url_prefix)


__all__ = ["init_app"]
