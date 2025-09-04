"""
Test cases for error_handlers module
"""

import unittest
from flask import Flask
from service.common import error_handlers as eh
from service.common import status
from service.models import DataValidationError


class TestErrorHandlers(unittest.TestCase):
    """Unit tests for Flask error handlers"""

    @classmethod
    def setUpClass(cls):
        """Setup Flask app for testing"""
        cls.app = Flask(__name__)
        cls.app.config["TESTING"] = True
        cls.app.config["PROPAGATE_EXCEPTIONS"] = False
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        """Tear down app context"""
        cls.ctx.pop()

    ######################################################################
    #  H A N D L E R   T E S T S
    ######################################################################

    def test_data_validation_error(self):
        """Test handler for DataValidationError"""
        exc = DataValidationError("Invalid data!")
        response, code = eh.request_validation_error(exc)
        self.assertEqual(code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertEqual(data["error"], "Bad Request")
        self.assertIn("Invalid data!", data["message"])

    def test_400_bad_request(self):
        """Test handler for 400 Bad Request"""
        exc = "Bad request data"
        response, code = eh.bad_request(exc)
        self.assertEqual(code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertEqual(data["error"], "Bad Request")
        self.assertIn("Bad request data", data["message"])

    def test_404_not_found(self):
        """Test handler for 404 Not Found"""
        exc = "Resource missing"
        response, code = eh.not_found(exc)
        self.assertEqual(code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertEqual(data["error"], "Not Found")
        self.assertIn("Resource missing", data["message"])

    def test_405_method_not_allowed(self):
        """Test handler for 405 Method Not Allowed"""
        exc = "Method not supported"
        response, code = eh.method_not_supported(exc)
        self.assertEqual(code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.get_json()
        self.assertEqual(data["error"], "Method not Allowed")
        self.assertIn("Method not supported", data["message"])

    def test_415_unsupported_media_type(self):
        """Test handler for 415 Unsupported Media Type"""
        exc = "Wrong media type"
        response, code = eh.mediatype_not_supported(exc)
        self.assertEqual(code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data = response.get_json()
        self.assertEqual(data["error"], "Unsupported media type")
        self.assertIn("Wrong media type", data["message"])

    def test_500_internal_server_error(self):
        """Test handler for 500 Internal Server Error"""
        exc = Exception("Something went wrong!")
        response, code = eh.internal_server_error(exc)
        self.assertEqual(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.get_json()
        self.assertEqual(data["error"], "Internal Server Error")
        self.assertIn("Something went wrong!", data["message"])


if __name__ == "__main__":
    unittest.main()
