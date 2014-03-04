from http.request import HSRequest
from resource.account import Account
from resource.signature_request import SignatureRequest


class HSClient(object):

    """docstring for HSClient"""
    ACCOUNT_CREATE_URL = 'https://api.hellosign.com/v3/account/create'
    ACCOUNT_INFO_URL = 'https://api.hellosign.com/v3/account'
    ACCOUNT_UPDATE_URL = 'https://api.hellosign.com/v3/account'

    SIGNATURE_REQUEST_INFO_URL = 'https://api.hellosign.com/v3/signature_request/'
    SIGNATURE_REQUEST_LIST_URL = 'https://api.hellosign.com/v3/signature_request/list'
    SIGNATURE_REQUEST_DOWNLOAD_PDF_URL = 'https://api.hellosign.com/v3/signature_request/files/'
    SIGNATURE_REQUEST_DOWNLOAD_FINAL_COPY_URL = 'https://api.hellosign.com/v3/signature_request/files/'

    EMBEDDED_OBJECT_GET_URL = 'https://api.hellosign.com/v3/embedded/sign_url/'

    UNCLAIMED_DRAFT_CREATE_URL = 'https://api.hellosign.com/v3/unclaimed_draft/create'

    REUSABLE_FORM_GET_URL = 'https://api.hellosign.com/v3/reusable_form/'
    REUSABLE_FORM_GET_LIST_URL = 'https://api.hellosign.com/v3/reusable_form/list'

    # TODO: Put api account in HSClient's __init__ function instead of
    # HSRequest

    def __init__(self):
        super(HSClient, self).__init__()
        self.account = Account()
        self.get_account_info()

    def create_account(self, email, password):
        # TODO: make the check exceptions
        if email is None:
            print("Email is not valid")
        if password is None:
            print("Password is not valid")
        request = HSRequest()
        response = request.post(self.ACCOUNT_CREATE_URL, {
                                'email_address': email, 'password': password})
        # print response
        return Account(response["account"])

    # Get account info and put in self.account
    def get_account_info(self):
        request = HSRequest()
        response = request.get(self.ACCOUNT_INFO_URL)
        # self.account = Account(response, "account")
        self.account.json_data = response["account"]

    def update_account_info(self):
        request = HSRequest()
        request.post(self.ACCOUNT_UPDATE_URL, {
                     'callback_url': self.account.callback_url})
        # return response

    # Get a signature request
    # param @signature_request_id
    def get_signature_request(self, signature_request_id):
        request = HSRequest()
        response = request.get(
            self.SIGNATURE_REQUEST_INFO_URL + signature_request_id)
        return SignatureRequest(response["signature_request"])

    def get_signature_request_list(self):
        sr_list = []
        request = HSRequest()
        response = request.get(self.SIGNATURE_REQUEST_LIST_URL)
        for signature_request in response["signature_requests"]:
            sr_list.append(SignatureRequest(signature_request))
        return sr_list

    def get_signature_request_file(self, signature_request_id, filename):
        request = HSRequest()
        request.get_file(
            self.SIGNATURE_REQUEST_DOWNLOAD_PDF_URL + signature_request_id, filename)

    def get_signature_request_final_copy(self, signature_request_id, filename):
        request = HSRequest()
        request.get_file(
            self.SIGNATURE_REQUEST_DOWNLOAD_FINAL_COPY_URL + signature_request_id, filename)

    def get_embeded_object(self, signature_id):
        request = HSRequest()
        response = request.get(self.EMBEDDED_OBJECT_GET_URL, signature_id)
        return Embeded(response["embedded"])

    # TODO: unfinshed
    def create_unclaimed_draft(self, data={}):
        pass

    def get_reusable_form(self, reusable_form_id):
        request = HSRequest()
        response = request.get(self.REUSABLE_FORM_GET_URL + reusable_form_id)
        return ReusableForm(response["reusable_form"])

    def get_reusable_form_list(self, page=1):
        request = HSRequest()
        response = request.get(self.REUSABLE_FORM_GET_LIST_URL, parameters={"page": page})
        # TODO: process the response and return a list of ReusableForm
