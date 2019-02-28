
from test_base import TestBase


class TestAuth(TestBase):

    """
    """

    def test_token_info(self, api_factory):

        resp = api_factory.base_controller.token_info(api_factory._auths)

        if 'memberOf' in api_factory._auths and api_factory._auths['memberOf']:
            assert resp == api_factory._auths['memberOf']
        else:
            assert resp == []

    """
    """

    def test_authorizer(self, api_factory):

        context = {}
        if 'memberOf' in api_factory._auths and api_factory._auths['memberOf']:
            for group in api_factory._auths['memberOf']:
                context[group] = True

        resp = api_factory.base_controller.authorizer(context)

        if 'memberOf' in api_factory._auths and api_factory._auths['memberOf']:
            assert resp == api_factory._auths['memberOf']
        else:
            assert resp == []
