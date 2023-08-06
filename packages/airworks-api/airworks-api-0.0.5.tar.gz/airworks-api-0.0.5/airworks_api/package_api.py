import json
from functools import partial
from airworks_api.base_api import BaseApi


class AirWorksApi:

    def __init__(self, base_url, access_key, access_secret, default_app_id, **kwargs):
        self.base_api = BaseApi()
        BaseApi.base_url = base_url
        self.base_api.access_key = access_key
        self.base_api.access_secret = access_secret
        self.default_app_id = default_app_id
        self.default_api_method = kwargs.get("default_api_method", "GET")
        self.default_page_num = kwargs.get("default_page_num", 1)
        self.default_page_size = kwargs.get("default_page_size", 100)

    def _call(self, api_url, **kwargs):
        app_id = kwargs.get("app_id", self.default_app_id)
        api_url = api_url.replace("__", "/")

        kwargs.update({
            "app_url": f"{app_id}/{api_url}",
            "api_method": kwargs.get("api_method") or self.default_api_method,
            "page_num": kwargs.get("page_num") or self.default_page_num,
            "page_size": kwargs.get("page_size") or self.default_page_size,
        })
        return self.base_api.api_response(**kwargs)

    def __getattr__(self, key):
        return partial(self._call, api_url=key)


if __name__ == "__main__":
    awp = AirWorksApi(
        base_url="aw-airworks-frontend:30000",
        access_key="kB85aqPMFZs_14",
        access_secret="lh66YHfiE7qL6TcOOvbLTg",
        default_app_id=1
    )

    res = awp.baymax(
        country="中国",
        id=None,
        page_size=100,
        page_num=1)

    print(json.dumps(res, indent=2, ensure_ascii=False))
