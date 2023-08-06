import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from it_finance_api.response import ItFinanceResponse
from it_finance_api.exceptions import InvalidLicenseError
from it_finance_api.endpoints import *
from it_finance_api.models.account import (
    AccountData,
    CapabilitiesType,
)
from it_finance_api.models.credit_score import (
    CreditScoreDetailData,
    CreditScoreOverviewData,
)


class ItFinanceApi:

    def __init__(
            self,
            base_uri='https://api-test.itfinance.it/IT4FRest/rest/',
            return_raw=False,
    ):
        """
        :param base_uri: the url of the api
        :param return_raw: return the data as json do not wrap into class
        """
        self.fiscal_code_user = None
        self.base_uri = base_uri
        self.return_raw = return_raw
        self.__auth = ''

        self._account_partner_data = None

    def login(self, username, password):
        self.__auth = HTTPBasicAuth(username, password)

        self._account_partner_data = self.get_account_partner()

    def _evaluate_license(self, capabilities):
        """
        Check if the endpoint can be called based on the user licenses
        :param capabilities: list of capabilities
        :return: none
        :raise: InvalidLicenseError: if the endpoint cant be called
        """
        self._account_partner_data: AccountData
        if datetime.now() - self._account_partner_data.last_call_update > timedelta(hours=5):
            # update the partner data
            self._account_partner_data = self.get_account_partner()

        if not self._account_partner_data.has_capabilities(capabilities):
            diff = list(set(capabilities) - set(self._account_partner_data.capabilities_list))
            raise InvalidLicenseError(diff)

    def force_update_account_partner(self):
        self._account_partner_data = self.get_account_partner()

    def get_account_partner(self):
        """
        :return: user's partner
        """
        res = requests.get(
            self.base_uri+ACCOUNT_PARTNER,
            auth=self.__auth
        )

        if self.return_raw:
            return res.content

        data = ItFinanceResponse(res)()
        return AccountData(data)

    def get_score_companies_detail(self, fiscal_code_user, fiscal_id, search_type='fiscalCode'):
        """
        :param fiscal_code_user: The fiscal code of the user sending the request (company)
        :param fiscal_id: The Fiscal ID of the company, can be a VAT CODE or a FISCAL CODE depending on the search type
        :param search_type: The kind of search between:
                - fiscalCode
                - vatNumber
        :return:
        """
        self._evaluate_license([
            CapabilitiesType.CREDIT_SCORE,
        ])

        uri_params = f'?fiscalCodeUser={fiscal_code_user}&fiscalId={fiscal_id}&searchType={search_type}'

        res = requests.get(
            self.base_uri+SCORE_COMPANIES_DETAIL+uri_params,
            auth=self.__auth
        )

        if self.return_raw:
            return res.content

        data = ItFinanceResponse(res)()
        return CreditScoreDetailData(data)

    def get_score_companies_overview(self, fiscal_code_user, fiscal_id, search_type='fiscalCode'):
        """
        :param fiscal_code_user: The fiscal code of the user sending the request (company)
        :param fiscal_id: The Fiscal ID of the company, can be a VAT CODE or a FISCAL CODE depending on the search type
        :param search_type: The kind of search between:
                - fiscalCode
                - vatNumber
        :return:
        """
        uri_params = f'?fiscalCodeUser={fiscal_code_user}&fiscalId={fiscal_id}&searchType={search_type}'

        res = requests.get(
            self.base_uri+SCORE_COMPANIES_DETAIL+uri_params,
            auth=self.__auth
        )

        if self.return_raw:
            return res.content

        data = ItFinanceResponse(res)()
        return CreditScoreOverviewData(data)
