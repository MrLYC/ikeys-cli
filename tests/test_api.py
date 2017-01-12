# coding: utf-8

import unittest

import mock

import ikeys_cli


class TestIKeytoneAPI(unittest.TestCase):
    def setUp(self):
        self.test_path = "test/path"
        PATH_META = {
            "test": {
                "check": ikeys_cli.APIPathInfo(
                    self.test_path, "POST", "",
                ),
                "get": ikeys_cli.APIPathInfo(
                    self.test_path, "GET", "",
                ),
            },
        }
        PATH_META.update(ikeys_cli.IKeytoneAPI.PATH_META)
        self.path_meta_patch = mock.patch(
            "ikeys_cli.IKeytoneAPI.PATH_META",
            new_callable=mock.PropertyMock(return_value=PATH_META),
        )
        self.path_meta = self.path_meta_patch.start()

        self.request_patch = mock.patch("requests.Session.request")
        self.request_mock = self.request_patch.start()

    def tearDown(self):
        self.request_patch.stop()
        self.path_meta = self.path_meta_patch.stop()

    def test_construction(self):
        api = ikeys_cli.IKeytoneAPI("http://ikeystone.yy.com")
        self.assertEqual(
            api.test.check._url_path, self.test_path,
        )
        self.assertEqual(
            api.test.check._method, "POST",
        )

    def test_get_signature_info(self):
        expires_millis = 1484207387000
        nonce = 511237945
        passwd = "456"
        user = "test"
        domain = "test"
        project = "test"
        signature_info = ikeys_cli.IKeytoneAPI.get_signature_info(
            domain=domain, user=user, password=passwd,
            expires_millis=expires_millis, nonce=nonce,
        )
        self.assertEqual(
            signature_info.signature,
            "017dd525ff60a6fac6016022d315903a",
        )

        signature_info = ikeys_cli.IKeytoneAPI.get_signature_info(
            domain=domain, user=user, password=passwd,
            expires_millis=expires_millis, nonce=nonce,
            project=project,
        )
        self.assertEqual(
            signature_info.signature,
            "9a3bfc0e5f714c1cd292fc0b483729b5",
        )

    def test_get_result_from_response1(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)

        data = {"value": 1}
        api.test.check(data=data)
        self.request_mock.assert_called_with(
            url=url + self.test_path, method="POST", json=data,
            headers=api._headers,
        )

        api.test.get(data=data)
        self.request_mock.assert_called_with(
            url=url + self.test_path, method="GET", params=data,
            headers=api._headers,
        )

    def test_get_result_from_response2(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)
        return_value = {
            "errno": 0,
            "data": id(self),
        }
        self.request_mock.return_value = mock.MagicMock(json=mock.MagicMock(
            return_value=return_value,
        ))

        result = api.test.check()
        self.assertEqual(result.errno, 0)
        self.assertEqual(result.errmsg, None)
        self.assertEqual(result.data, id(self))

    def test_get_result_from_response3(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)
        self.request_mock.return_value = mock.MagicMock(json=mock.MagicMock(
            side_effect=ValueError,
        ))

        with self.assertRaises(ikeys_cli.ResultParseError):
            api.test.check()

    def test_get_result_from_response4(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)
        self.request_mock.return_value = mock.MagicMock(json=mock.MagicMock(
            return_value={},
        ))
        domain = "domain"
        user = "user"
        password = "password"
        project = "project"
        api.authenticate(domain, user, password, project)
        headers = {}

        api.test.check(headers=headers)

        self.assertDictContainsSubset({
            "X-AUTH-DOMAIN": domain,
            "X-AUTH-USER": user,
            "X-AUTH-PROJECT": project,
        }, headers)
        self.assertIn("X-AUTH-EXPIRES", headers)
        self.assertIn("X-AUTH-NONCE", headers)
        self.assertIn("X-AUTH-SIGNATURE", headers)

    def test_get_authentication_headers(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)
        domain = "domain"
        user = "user"
        password = "password"
        project = "project"
        api.authenticate(domain, user, password, project)
        headers = api.get_authentication_headers()
        self.assertDictContainsSubset({
            "X-AUTH-DOMAIN": domain,
            "X-AUTH-USER": user,
            "X-AUTH-PROJECT": project,
        }, headers)

        api.authenticate(domain, user, password)
        headers = api.get_authentication_headers()
        self.assertNotIn("X-AUTH-PROJECT", headers)
