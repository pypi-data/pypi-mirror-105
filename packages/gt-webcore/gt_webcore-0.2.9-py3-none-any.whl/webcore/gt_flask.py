# coding:utf-8
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from .result import Result
from .api_encoder import ApiEncoder
from .error_handler import init_error_handler
from .interceptor import init_interceptor

class GtFlask(Flask):
    def make_response(self, rv):
        try:
            if isinstance(rv, Result):
                return super().make_response(jsonify(rv))
            else:
                return super().make_response(rv)
        except Exception as e:
            self.logger.error(e)
            return super().make_response(jsonify(Result.error()))

    def init_app(self):
        self.db = None
        self.celery = None
        self.processor = None
        self.cache = None
        self.mongo_db = None

        CORS(self, resources={r'/*': {"origins": '*'}})
        self.json_encoder = ApiEncoder
        init_error_handler(self)
        init_interceptor(self)
        
    def register_encoder(self, encoder):
        self.json_encoder.add_encoder(encoder)

    def unregister_encoder(self, encoder):
        self.json_encoder.remove_encoder(encoder)