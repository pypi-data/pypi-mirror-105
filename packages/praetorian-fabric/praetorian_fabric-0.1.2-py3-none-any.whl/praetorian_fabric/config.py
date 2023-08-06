import os

from praetorian_api_client.api_client import ApiClient
from praetorian_api_client.configuration import Environment, Configuration
from fabric import Connection
from invoke import Context


class PraetorianConfig:
    def __init__(self, project_name):
        environment = Environment(name='praetorian-api', api_url=os.getenv('PRAETORIAN_API_URL'), read_only=False)
        configuration = Configuration(
            environment=environment, key=os.getenv('PRAETORIAN_API_KEY'), secret=os.getenv('PRAETORIAN_API_SECRET')
        )
        self._api_client = ApiClient.create_from_auth(
            configuration=configuration,
            username=os.getenv('PRAETORIAN_USERNAME'),
            password=os.getenv('PRAETORIAN_PASSWORD')
        )

        self._user = self._api_client.user.get_me()
        self._project = self._api_client.project.list(user_id=self._user.id, name=project_name)[0]

        self._remote = None
        self._variables = None
        self._temporary_user = None

    def get_variable(self, name):
        if '.' in name:
            nested_variables = name.split('.')
            temp_variables = self._variables

            for nested_variable in nested_variables:
                if temp_variables:
                    temp_variables = temp_variables.get(nested_variable)
                else:
                    break

            value = temp_variables
        else:
            value = self._variables.get(name)
        return value

    def connect(self, ctx: Context, remote_name: str) -> Connection:
        self._remote = self._api_client.remote.list(project_id=self._project.id, name=remote_name)[0]
        self._variables = self._remote.variables

        self._temporary_user = self._api_client.user.create_temporary(
            project_id=self._project.id, remote_id=self._remote.id
        )

        ctx.host = os.getenv('PROXY_HOST')
        ctx.port = int(os.getenv('PROXY_PORT'))

        ctx.user = self._temporary_user.username
        ctx.connect_kwargs.password = self._temporary_user.password

        ctx = Connection(
            host=ctx.host,
            user=ctx.user,
            port=ctx.port,
            connect_kwargs=ctx.connect_kwargs,
        )

        ctx.config['run']['echo'] = True
        return ctx
