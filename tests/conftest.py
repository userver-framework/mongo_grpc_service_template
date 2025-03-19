import pathlib
import sys

import pytest
import grpc

import handlers.hello_pb2_grpc as hello_services  # noqa: E402, E501

USERVER_CONFIG_HOOKS = ['prepare_service_config']
pytest_plugins = [
    'pytest_userver.plugins.mongo',
    'pytest_userver.plugins.grpc',
]


MONGO_COLLECTIONS = {
    'hello_users': {
        'settings': {
            'collection': 'hello_users',
            'connection': 'admin',
            'database': 'admin',
        },
        'indexes': [],
    },
}


@pytest.fixture(scope='session')
def mongodb_settings():
    return MONGO_COLLECTIONS


@pytest.fixture
def grpc_service(grpc_channel, service_client):
    return hello_services.HelloServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def prepare_service_config(grpc_mockserver_endpoint):
    def patch_config(config, config_vars):
        components = config['components_manager']['components']
        components['hello-client']['endpoint'] = grpc_mockserver_endpoint

    return patch_config
