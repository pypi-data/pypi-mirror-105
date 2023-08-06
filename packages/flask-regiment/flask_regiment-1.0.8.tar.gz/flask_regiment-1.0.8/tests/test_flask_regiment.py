from flask import Flask
from flask_regiment import InstaLog
import time

instalog = InstaLog()

print("instalog loaded")

def create_app(test_config=None):
    print("create_app called")
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        INSTALOG_API_KEY='df8ff78b-76ee-4a80-8c40-5396fad1f5ad',
        INSTALOG_API_SECRET_KEY='e30e81c6-09ad-4df9-8a7c-bab2dec2dccb',
        INSTALOG_META_DATA={
            "environment": "staging",
            "service_name": "test_app",
            "namespace": "zeroone"
        },
        INSTALOG_LOG_TYPE='string'
    )

    instalog.init_app(app)

    app.instalog.log_info("custom log from flask")

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/e')
    def error():
        1/0
        return '', 200

    print("create_app done")

    return app
