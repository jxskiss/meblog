# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/4/2
#

from os.path import abspath, dirname, join
_root = abspath(dirname(__file__))


class Config:
    SECRET_KEY = 'I will never ever tell you!'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    POSTS_PER_PAGE = 10
    REG_CODE = 'REGCODE'

    # meblog site configuration
    MEBLOG_SITE_NAME = 'meblog'
    MEBLOG_SITE_TITLE = "meblog's website"
    MEBLOG_UYAN_UID = 'dummy'
    MEBLOG_SHOW_LOGIN = False


    @staticmethod
    def init_app(app):
        pass


class DevelConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_root, 'data-dev.sqlite')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_root, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_root, 'data.sqlite')
    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        # TODO: do initialization work here
        pass


class SAEConfig(ProdConfig):
    MEBLOG_USE_NULLPOOL = True

    @staticmethod
    def init_app( app):
        ProdConfig.init_app(app)
        try:
            import config_sae
        except ImportError:
            config_sae = None
        if config_sae:
            app.config.from_object(config_sae)
        # TODO: add logging and other settings


config = {
    'devel': DevelConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'sae': SAEConfig,

    'default': DevelConfig
}
