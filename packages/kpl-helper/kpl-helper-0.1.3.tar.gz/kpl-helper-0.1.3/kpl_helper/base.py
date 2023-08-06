import requests
from requests.adapters import HTTPAdapter
import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("kpl-helper")

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))


class _BaseConfig:
    def __init__(self):
        _inner = os.getenv("KPL_INNER")
        self._inner = False if _inner is None else True
        if not self._inner:
            return
        # KPL_ENV: notebook/pipeline/deploy
        self._env_type = os.getenv("KPL_ENV")
        self._input_root = os.getenv("KPL_ENV_INPUT_ROOT_PATH")
        self._output_root = os.getenv("KPL_ENV_OUTPUT_ROOT_PATH", "/")
        self._parameter = os.getenv("KPL_ENV_PARAMETER")
        self._task_id = int(os.getenv("KPL_ENV_TASK_ID", 0))
        # TODO: remove  KPL_METRIC_TOKEN, KPL_METRIC_API
        self._metric_api = os.getenv("KPL_METRIC_API")
        self._metric_token = os.getenv("KPL_METRIC_TOKEN")
        self._api_url = os.getenv("KPL_ENV_INTERNAL_API_HOST", "http://seetaas--monitor.seetaas.svc.cluster.local:8920")
        if not self._api_url.endswith("/"):
            self._api_url = self._api_url + "/"
        jwt_token_path = os.getenv("KPL_TOKEN_LOCATE")
        with open(jwt_token_path) as fi:
            self._jwt_token = fi.read().strip()

    def get_api_url(self):
        if not self._inner:
            return ""
        if self._api_url.endswith("/"):
            return self._api_url[:len(self._api_url) - 1]
        return self._api_url

    def get_jwt_token(self):
        if not self._inner:
            return ""
        return self._jwt_token

    def get_inner(self):
        return self._inner

    def get_input_root(self):
        if not self._inner:
            return ""
        return self._input_root

    def get_output_root(self):
        if not self._inner:
            return ""
        return self._output_root

    def get_parameter(self):
        if not self._inner:
            return "{}"
        return self._parameter

    def get_metric_api(self):
        if not self._inner:
            return ""
        return self._metric_api

    def get_metric_token(self):
        if not self._inner:
            return ""
        return self._metric_token

    def get_env_type(self):
        if not self._inner:
            return None
        return self._env_type

    def get_task_id(self):
        if not self._inner:
            return None
        return self._task_id

    def get_cluster(self):
        pass


__base_config = None


def get_config():
    global __base_config
    if __base_config is None:
        __base_config = _BaseConfig()
    return __base_config


def ready():
    logging.info("[kpl-helper]: ready for using.")


def done():
    logging.info("[kpl-helper]: execute kpl done()")


class _MsgType:
    NewMetric = "NewMetric"
    MetricData = "MetricData"


class _ResultType:
    SCALAR_RESULT = 'scalar_result'  # 用于如Rank1，Rank5，LFW，MegaFace测试协议输出的单精度值测试结果
    CURVE_RESULT = 'curve_result'  # 用于如ROC测试协议输出的测试曲线
    PROGRESS = 'progress'


class _APIBase:
    def __init__(self):
        self._api = get_config().get_api_url()
        self._token = get_config().get_jwt_token()
        self.sess = requests.session()
        self.post = self._wrap(self.sess.post)

    def _wrap(self, func):
        def wrapped_http(router, **kwargs):
            if "headers" not in kwargs:
                kwargs["headers"] = {"Authorization": self._token}
            else:
                kwargs["headers"]["Authorization"] = self._token
            kwargs["url"] = self._api + router
            res = func(**kwargs)
            if not res.ok:
                raise Exception("Network error. status code:", res.status_code)
            response = res.json()
            if response['code'] != 'Success':
                raise Exception("Response error. code: [{}]. message: [{}]".format(response['code'], response['msg']))
            return response.get('data', None)

        return wrapped_http
