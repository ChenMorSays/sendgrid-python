"""
This library allows you to quickly and easily use the SendGrid Web API v3 via
Python.

For more information on this library, see the README on Github.
    http://github.com/sendgrid/sendgrid-python
For more information on the SendGrid v3 API, see the v3 docs:
    http://sendgrid.com/docs/API_Reference/api_v3.html
For the user guide, code examples, and more, visit the main docs page:
    http://sendgrid.com/docs/index.html

This file provides the SendGrid API Client.
"""


import os
import warnings

import python_http_client


class SendGridAPIClient(object):
    """The SendGrid API Client.

    Use this object to interact with the v3 API.  For example:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        ...
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())

    For examples and detailed use instructions, see
        https://github.com/sendgrid/sendgrid-python
    """

    def __init__(
            self,
            api_key=None,
            host='https://api.sendgrid.com',
            impersonate_subuser=None):
        """
        Construct SendGrid v3 API object.
        Note that the underlying client is being set up during initialization, therefore changing
            attributes in runtime will not affect HTTP client behaviour.

        :param api_key: SendGrid API key to use. If not provided, key will be read from
            environment variable "SENDGRID_API_KEY"
        :type api_key: string
        :param impersonate_subuser: the subuser to impersonate. Will be passed by
            "On-Behalf-Of" header by underlying client.
            See https://sendgrid.com/docs/User_Guide/Settings/subusers.html for more details
        :type impersonate_subuser: string
        :param host: base URL for API calls
        :type host: string
        """
        from . import __version__
        self.api_key = api_key or os.environ.get('SENDGRID_API_KEY')
        self.impersonate_subuser = impersonate_subuser
        self.host = host
        self.version = __version__
        self.useragent = 'sendgrid/{};python'.format(self.version)

        self.client = python_http_client.Client(host=self.host,
                                                request_headers=self._default_headers,
                                                version=3)

    @property
    def _default_headers(self):
        headers = {
            "Authorization": 'Bearer {}'.format(self.api_key),
            "User-agent": self.useragent,
            "Accept": 'application/json'
        }
        if self.impersonate_subuser:
            headers['On-Behalf-Of'] = self.impersonate_subuser

        return headers

    def reset_request_headers(self):
        self.client.request_headers = self._default_headers

    def send(self, message):
        response = self.client.mail.send.post(request_body=message.get())
        return response
