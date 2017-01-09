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
        sid = "my_domain-abc-2b7535e356d3c"
        effect_millis = 3600000
        nonce = 421186121
        signature_info = ikeys_cli.IKeytoneAPI.get_signature_info(
            sid=sid, effect_millis=effect_millis, nonce=nonce,
        )
        self.assertEqual(signature_info.sid, sid)
        self.assertEqual(signature_info.effect_millis, effect_millis)
        self.assertEqual(signature_info.nonce, nonce)
        self.assertEqual(
            signature_info.signature,
            "a9530ef1b4e8f31c3bf5c0574f724d33",
        )
        self.assertEqual(
            signature_info.token,
            "my_domain-abc-2b7535e356d3c-191aca49-a9530ef1b4e8f31c3bf5c0574f724d33",
        )

    def test_get_result_from_response1(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)

        data = {"value": 1}
        api.test.check(data=data)
        self.request_mock.assert_called_with(
            url=url + self.test_path, method="POST", json=data,
        )

        api.test.get(data=data)
        self.request_mock.assert_called_with(
            url=url + self.test_path, method="GET", params=data,
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
