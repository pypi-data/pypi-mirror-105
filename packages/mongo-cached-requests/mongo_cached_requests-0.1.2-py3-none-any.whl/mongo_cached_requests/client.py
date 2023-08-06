import pymongo
import requests
import datetime
import urllib.parse
from requests.models import Response
from typing import Any, Dict, Union
from pymongo import MongoClient
from pymongo.collection import Collection


class RequestDocument:
    path: str
    params: str
    time: datetime
    response: Any

    def __init__(self, path: str, query: str, time: datetime, response: Any):
        self.path = path
        self.params = query
        self.time = time
        self.response = response

    @staticmethod
    def from_dict(d: Dict):
        return RequestDocument(d['url'], d['params'], d['time'], d['response'])


class CachedRequestClient:
    __mongoClient: MongoClient

    def __init__(self, mongo_client: MongoClient):
        self.__mongoClient = mongo_client

    def get(self, url, params=None, time_diff_allowance=datetime.timedelta(days=1), no_cache=False, **kwargs):

        if no_cache:
            self.__get_from_http__(url, params, **kwargs)
            return

        params = {} if params is None else params

        collection = self.__get_collection_from_url__(url)

        now: datetime = datetime.datetime.utcnow()
        most_recent_match: Union[Dict, None] = collection.find_one(
            params, sort=[('time', pymongo.DESCENDING)]
        )

        if most_recent_match is not None:
            time_since_most_recent_request = now - most_recent_match['time']

            if time_since_most_recent_request > time_diff_allowance:
                self.__get_from_http__(url, params, **kwargs)
                return

        else:
            self.__get_from_http__(url, params, **kwargs)
            return

    def __get_collection_from_url__(self, url) -> Collection:
        parsed_url = urllib.parse.urlsplit(url)
        return self.__mongoClient.get_database(parsed_url.hostname.replace('.', '-')).get_collection(parsed_url.path)

    def __get_from_http__(self, url, params=None, **kwargs):
        r: Response = requests.get(url, params, **kwargs)
        doc = {**params, 'time': datetime.datetime.utcnow(), 'response': r.json()}
        collection = self.__get_collection_from_url__(url)
        collection.insert_one(doc)
