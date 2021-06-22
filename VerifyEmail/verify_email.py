import requests


"""
APP:       Verify Email
Reference:      https://verify-email.org/
API Version:    v1.0
API Type:       REST API
API Auth:       API key
Auth Type:      Basic Auth
Access Type:    API Level
"""


class Verifyemail(object):
    def __init__(self, api_key, **kwargs):
        self.base_url = 'https://app.verify-email.org/api/v1'
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            }

    def request_handler(self, method, endpoint, query_params=None,
                        payload=None,
                        **kwargs):
        """
        request and response handler
        :param method: http method
        :param endpoint: api endpoint
        :param query_params: params
        :param payload: payload
        :param file: file path or file url
        :param kwargs:
        :return:
        """
        try:
            url = "{0}/{1}/{2}".format(self.base_url, self.api_key, endpoint)
            if method == "GET":
                response = requests.request("GET", url, params=query_params,
                                            headers=self.headers)
            else:
                method_error = "Invalid Method {0} Requested!".format(method)
                return {"response": method_error,
                        "function_status": 'ERROR'}

            response_data = {'status_code': response.status_code}
            if response.ok:
                response_data['response'] = response.json()
                response_data['function_status'] = 'SUCCESS'
            elif response.status_code >= 400 or response.status_code < 500:
                response_data['response'] = response.json()
                response_data['function_status'] = 'ERROR'
            else:
                response_data['response'] = response.text
                response_data['function_status'] = 'ERROR'
        except Exception as e:
            response_data['response'] = str(e)
            response_data['function_status'] = 'ERROR'
        return response_data

    def verify_email(self, email, **kwargs):
        """
        The action is used to verify an email.

        :param email: Input an Email Address. (Eg: abc@email.com)
        :param kwargs:
        :return:
        """

        endpoint = "verify/{0}".format(email)
        return self.request_handler('GET', endpoint)

api_key = input('Please Enter the Verify Email API Key: ')
x = Verifyemail(api_key)
data = input ('Enter The Email: ')
data = str (data)
x1 = x.verify_email (email=data)
print (x1) 