# coding: utf-8

import unittest

import mock

import ikeys_cli


class TestSha1(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(
            ikeys_cli.sha1(b"lyc"),
            "05a6dfe7568c72fa1ac0598459af1735df3be258",
        )

    def test_unicode(self):
        self.assertEqual(
            ikeys_cli.sha1(b"lyc".decode("utf-8")),
            "05a6dfe7568c72fa1ac0598459af1735df3be258",
        )


class TestMD5(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(
            ikeys_cli.md5(b"lyc"),
            "efa664720fac0075674862b40d490830",
        )

    def test_unicode(self):
        self.assertEqual(
            ikeys_cli.md5(b"lyc".decode("utf-8")),
            "efa664720fac0075674862b40d490830",
        )


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
        url, method = api._get_url_and_method(api.test.check)
        self.assertEqual(url, "http://ikeystone.yy.com/%s" % api.test.check._url_path)
        self.assertEqual(method, api.test.check._method)
        url, method = api._get_url_and_method(api.nothing.to.get)
        self.assertEqual(url, "http://ikeystone.yy.com/nothing/to")
        self.assertEqual(method, "GET")

    def test_get_signature_info(self):
        expires = "159aa7c5377"
        nonce = "6321930faa5"
        passwd = "123"
        user = "my_admin"
        domain = "my_domain"
        signature_info = ikeys_cli.IKeytoneAPI.get_signature_info(
            domain=domain, user=user, password=passwd,
            expires=expires, nonce=nonce,
        )
        self.assertEqual(
            signature_info.signature,
            "beef3ce36aed1211a4af2e6bc24fe0de",
        )

        expires = "159aa793a91"
        nonce = "63167719887"
        project = "ut_project_01b59072_a48d_4005_971b_8ac44dd2672a"
        passwd = "ut_pass_a46690e9_2825_4fa5_a7f2_6c7e0f2d7e09"
        user = "ut_user_a46690e9_2825_4fa5_a7f2_6c7e0f2d7e09"
        domain = "ut_domain_da82c6a5_4b24_4f96_8e83_6b85fdfd4d43"
        signature_info = ikeys_cli.IKeytoneAPI.get_signature_info(
            domain=domain, user=user, password=passwd,
            expires=expires, nonce=nonce,
            project=project,
        )
        self.assertEqual(
            signature_info.signature,
            "02c5adc1f5874f29a68c303678cb6b2f",
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
        }, headers)
        self.assertIsInstance(headers["X-AUTH-EXPIRES"], str)
        self.assertIsInstance(headers["X-AUTH-NONCE"], str)
        self.assertIsInstance(headers["X-AUTH-SIGNATURE"], str)

    def test_get_request_headers(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)
        domain = "domain"
        user = "user"
        password = "password"
        project = "project"
        api.authenticate(domain, user, password, project)
        headers = api.get_request_headers()
        self.assertDictContainsSubset({
            "X-AUTH-DOMAIN": domain,
            "X-AUTH-USER": user,
            "X-AUTH-PROJECT": project,
        }, headers)

    def test_get_authentication_headers(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)
        domain = "domain"
        user = "user"
        password = "password"

        api.authenticate(domain, user, password)
        headers = api.get_authentication_headers()
        self.assertDictContainsSubset({
            "X-AUTH-DOMAIN": domain,
            "X-AUTH-USER": user,
        }, headers)
        self.assertNotIn("X-AUTH-PROJECT", headers)

    def test_domain_verify_request(self):
        url = "http://ikeystone.yy.com/v1/"
        api = ikeys_cli.IKeytoneAPI(url)

        domain = "my_domain"
        user = "my_user"
        password = "password"
        project = "my_project"
        api.authenticate(domain, user, password, project)

        response_data = {
            "domain": domain, "user": user,
            project: "my_project", "expires": "1598b5b3eb7",
            "nonce": "74a465fddab8b", "api": "api_name_0",
            "signature": "56f8519d7f31460821e4722de0c77c5f",
            "roles": ["SERVICE"],
        }
        self.request_mock.return_value = mock.MagicMock(json=mock.MagicMock(
            return_value={"errno": 0, "data": response_data}))

        result = api.domain.request.verify(data={
            "domain": domain, "user": user,
            project: "my_project", "expires": "1598b5b3eb7",
            "nonce": "74a465fddab8b", "api": "api_name_0",
            "signature": "56f8519d7f31460821e4722de0c77c5f",
        })
        data = result.data
        self.assertEqual(result.errno, 0)
        self.assertEqual(result.errmsg, None)
        self.assertEqual(data, response_data)
