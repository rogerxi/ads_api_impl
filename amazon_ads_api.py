"""
Implementation of Amazon Advertising API. Refer to:
https://advertising.amazon.com/API
"""
from collections import defaultdict
from datetime import datetime
from gzip import GzipFile
from io import BytesIO
import json
import logging
import time
import requests
from requests.auth import HTTPBasicAuth


logger = logging.getLogger(__name__)


class AdsAPIError(Exception):
    """General error."""
    pass


class AdsAPIClient(object):
    """API reference: https://advertising.amazon.com/API
    """
    ENTITY_TYPE_AD_GROUPS = 'adGroups'
    ENTITY_TYPE_CAMPAIGNS = 'campaigns'
    ENTITY_TYPE_BIDDABLE_KEYWORDS = 'keywords'
    ENTITY_TYPE_NEGATIVE_KEYWORDS = 'negativeKeywords'
    ENTITY_TYPE_PRODUCT_ADS = 'productAds'
    ENTITY_TYPE_PROFILES = 'profiles'
    ENTITY_TYPE_REPORTS = 'reports'

    MIN_DAILY_BUDGET = 1.0
    MIN_BID = 0.02

    _API_ENDPOINT_EU = 'https://advertising-api-eu.amazon.com/v1/%s'
    _API_ENDPOINT_NA = 'https://advertising-api.amazon.com/v1/%s'
    _API_ENDPOINT_TEST = 'https://advertising-api-test.amazon.com/v1/%s'
    _API_ENDPOINT_TOKEN = 'https://api.amazon.com/auth/o2/token'

    _COUNTRY_TO_ENDPOINT_MAP = {
        'US': _API_ENDPOINT_NA,
        'CA': _API_ENDPOINT_NA,
        'MX': _API_ENDPOINT_NA,
        'UK': _API_ENDPOINT_EU,
        'FR': _API_ENDPOINT_EU,
        'IT': _API_ENDPOINT_EU,
        'ES': _API_ENDPOINT_EU,
        'DE': _API_ENDPOINT_EU,
        'IN': _API_ENDPOINT_EU,
    }

    _PAGE_SIZE = 1000           # 5000 entities by default.

    def __init__(self, profile_id, country, access_token, refresh_token,
                 token_time, expires_in=3600):
        self.redirect_uri = param.get('redirect_uri')
        self.client_id = param.get('client_id')
        self.client_secret = param.get('client_secret')
        self.client_auth = HTTPBasicAuth(self.client_id, self.client_secret)
        self.profile_id = str(profile_id)
        self.api_endpoint = AdsAPIClient._COUNTRY_TO_ENDPOINT_MAP[country]
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_time = token_time
        self.expires_in = expires_in
        self.headers = None

    def _rebuild_auth(self, content_type='application/json'):
        """Rebuild authentication headers.

        Args:
            content_type: string, typically 'application/json'.
        """
        self.access_token, self.token_time = (
            AdsAPIClient.refresh_access_token(
                self.refresh_token, self.access_token, self.token_time))
        self.headers = {'Authorization': 'Bearer ' + self.access_token,
                        'Amazon-Advertising-API-Scope': self.profile_id}
        if content_type:
            self.headers['Content-Type'] = content_type

    @staticmethod
    def get_tokens(auth_code):
        """Exchange the authorization code for access and refresh tokens.

        Note: Execute only once when client authorizes. The refresh token will
        never expire while access tokens are only valid for 60 minutes,
        so they need to be refreshed periodically using the refresh token.

        Args:
            auth_code: string, authorization code given by client.

        Returns:
            A dict:
                {
                    'access_token': <access_token>,
                    'refresh_token': <refresh_token>,
                    'token_type': 'bearer',
                    'token_time': 1488326000.0,
                    'expires_in': 3600,
                }
        """
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': 'Your Redirect URI',
            'client_id': 'Your Client ID',
            'client_secret': 'Your Client Secret',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        }
        response = requests.post(url=AdsAPIClient._API_ENDPOINT_TOKEN,
                                 data=data,
                                 headers=headers)
        response_json = response.json()
        if response.status_code == 200 or (
                response_json and response_json.get('refresh_token')):
            logger.info('Status Code: %s, Content: %s', response.status_code,
                        response.content)
            if 'token_time' not in response_json:
                # UTC time.
                response_json['token_time'] = time.mktime(
                    timezone.now().timetuple())
            return response_json
        else:
            logger.exception(response.content)
            raise AdsAPIError(response.status_code, response.content)

    @staticmethod
    def refresh_access_token(refresh_token, access_token=None,
                             token_time=None):
        """Refresh access token using the refresh token.

        Args:
            refresh_token: string.
            access_token: string.
            token_time: float, in UTC time.

        Returns:
            Access token and token time (UTC).
        """
        # Check if the token time has passed almost beyond one hour.
        if (not access_token or not token_time or
                time.mktime(timezone.now().timetuple()) > (
                    float(token_time) + 55 * 60)):
            response = requests.post(
                url=AdsAPIClient._API_ENDPOINT_TOKEN,
                data={
                    'grant_type': 'refresh_token',
                    'client_id': 'Your Client ID',
                    'client_secret': 'Your Client Secret',
                    'refresh_token': refresh_token,
                },
                headers={
                    'Content-Type':
                    'application/x-www-form-urlencoded;charset=UTF-8',
                }
            )
            logger.info(response.json())
            if response.status_code != 200:
                raise AdsAPIError(response.status_code, response.content)

            access_token = response.json().get('access_token')
            token_time = time.mktime(timezone.now().timetuple())

        return (access_token, token_time)

    @staticmethod
    def get_profiles(refresh_token):
        """Get the seller's profiles.

        Args:
            refresh_token: string.

        Return:
            List of the seller's profiles.
        """
        access_token, _ = AdsAPIClient.refresh_access_token(refresh_token)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token,
        }
        profiles = []
        for api_endpoint in (AdsAPIClient._API_ENDPOINT_NA,
                             # AdsAPIClient._API_ENDPOINT_TEST,
                             AdsAPIClient._API_ENDPOINT_EU):
            response = requests.get(
                url=api_endpoint % AdsAPIClient.ENTITY_TYPE_PROFILES,
                headers=headers)
            logger.info('Response headers: %s', response.headers)
            if response.status_code == 200:
                profiles.extend(response.json())

        return profiles

    @staticmethod
    def get_keyword_to_create(campaign_id, adgroup_id, keyword_text,
                              match_type='phrase', state='enabled', bid=None):
        """Get a dict of biddable or negative keyword to create for Ad Group.

        Args:
            campaign_id: long, ID of the assigned campaign.
            adgroup_id: long, ID of the assigned ad group.
            keyword_text: string.
            match_type: string, e.g., broad, phrase, exact for biddable
                keyword; negativePhrase, negativeExact for negative keyword.
            state: string, e.g., enabled, paused, archived.
            bid: float, bid of the biddable keyword.

        Return:
            A dict of biddable keyword or negative keyword as:
                {
                    'campaignId': <campaign id>,
                    'adGroupId': <ad group id>,
                    'keywordText': <keyword text>,
                    'matchType': <broad / phrase / exact>,
                    'state': <enabled / paused / archived>,
                    'bid': <1.0>,
                }.
            The keyword is biddable when match type is broad/phrase/exact;
            otherwise, it is negative.
        """
        keyword_dict = {
            'campaignId': long(campaign_id),
            'adGroupId': long(adgroup_id),
            'keywordText': keyword_text,
            'matchType': match_type,
            'state': state,
        }

        if bid and match_type in ('broad', 'phrase', 'exact'):
            keyword_dict['bid'] = max(float(bid), AdsAPIClient.MIN_BID)

        return keyword_dict

    @staticmethod
    def get_keyword_to_update(keyword_id, state='enabled', is_biddable=True,
                              bid=None):
        """Get a dict of biddable or negative keyword to update for Ad Group.

        Args:
            keyword_id: long, ID of keyword to be updated.
            state: string, e.g., enabled, paused, archived.
            is_biddable: boolean, True/False: biddable/negative keyword.
            bid: float, bid of the biddable keyword.

        Return:
            A dict of biddable or negative keyword as:
                {
                    'keywordId': <keyword_id>,
                    'state': <enabled / paused / archived>,
                    'bid': <1.0>,
                }.
        """
        keyword_dict = {
            'keywordId': long(keyword_id),
            'state': state,
        }

        if is_biddable and bid:
            keyword_dict['bid'] = max(float(bid), AdsAPIClient.MIN_BID)

        return keyword_dict

    def create_ad(self, campaign_id, adgroup_id, sku, state='enabled'):
        """Create a product ad.

        Args:
            campaign_id: long, ID of the assigned campaign.
            adgroup_id: long, ID of the assigned ad group.
            sku: string, SKU.
            state: string, e.g., enabled, paused, archived.

        Return:
            Created product ad.
        """
        data = [
            {
                'campaignId': campaign_id,
                'adGroupId': adgroup_id,
                'sku': sku,
                'state': state,
            }
        ]
        return self._create_entities(self.ENTITY_TYPE_PRODUCT_ADS, data)[0]

    def create_adgroup(self, campaign_id, default_bid, name=None,
                       state='enabled'):
        """Create an ad group.

        Args:
            campaign_id: long, ID of the assigned campaign.
            default_bid: float, $0.02 at minimum.
            name: string, name of ad group.
            state: string, e.g., enabled, paused, archived.

        Return:
            Created ad group.
        """
        data = [
            {
                'campaignId': campaign_id,
                'name': name or ('Ad Group #' +
                                 datetime.utcnow().strftime('%Y%m%d%H%M%S%f')),
                'state': state,
                'defaultBid': max(float(default_bid), AdsAPIClient.MIN_BID),
            }
        ]
        return self._create_entities(self.ENTITY_TYPE_AD_GROUPS, data)[0]

    def create_campaign(self, name, daily_budget, start_date, end_date=None,
                        state='enabled', campaign_type='sponsoredProducts',
                        targeting_type='manual'):
        """Create a campaign.

        Args:
            name: string, campaign name.
            daily_budget: float.
            start_date: string, in format: 'YYYYMMDD'.
            end_date: string, in format: 'YYYYMMDD'.
            state: string, e.g., enabled, paused, archived.
            campaign_type: string, e.g., sponsoredProducts.
            targeting_type: string, e.g., auto, manual (keyword-targeted).

        Return:
            Created campaign.
        """
        data = {
            'name': name,
            'dailyBudget': max(
                float(daily_budget), AdsAPIClient.MIN_DAILY_BUDGET),
            'startDate': start_date,
            'state': state,
            'campaignType': campaign_type,
            'targetingType': targeting_type,
        }
        if end_date:
            data['endDate'] = end_date

        return self._create_entities(self.ENTITY_TYPE_CAMPAIGNS, [data])[0]

    def create_keywords(self, campaign_id, adgroup_id, keyword_texts,
                        match_type='phrase', state='enabled', is_biddable=True,
                        bid=None):
        """Create biddable keywords or negative Keywords in batch for Ad Group.

        Note: keyword can only be created for keyword-targeted campaign.

        Args:
            campaign_id: long, ID of the assigned campaign.
            adgroup_id: long, ID of the assigned ad group.
            keyword_texts: string[].
            match_type: string, e.g., broad, phrase, exact for biddable
                keyword; negativePhrase, negativeExact for negative keyword.
            state: string, e.g., enabled, paused, archived.
            is_biddable: boolean, True/False: biddable/negative keyword.
            bid: float, bid of the keywords.

        Return:
            Created biddable keywords or negative Keywords.
        """
        if not keyword_texts:
            return None

        data = [
            {
                'campaignId': campaign_id,
                'adGroupId': adgroup_id,
                'keywordText': text,
                'matchType': match_type,
                'state': state,
                'bid': max(float(bid), AdsAPIClient.MIN_BID) if bid else None,
            } for text in keyword_texts
        ]
        if is_biddable:
            entity_type = self.ENTITY_TYPE_BIDDABLE_KEYWORDS
        else:
            entity_type = self.ENTITY_TYPE_NEGATIVE_KEYWORDS

        return self._create_entities(entity_type, data)

    def create_keywords_v2(self, data, is_biddable=True):
        """Create biddable / negative keywords in batch for Ad Group.

        Note: keyword can only be created for keyword-targeted campaign.

        Args:
            data: list of keyword info, refer to method get_keyword_to_create()
            is_biddable: boolean, True/False: biddable/negative keyword.

        Return:
            Created biddable / negative keywords.
        """
        if not data:
            return None

        if is_biddable:
            entity_type = self.ENTITY_TYPE_BIDDABLE_KEYWORDS
        else:
            entity_type = self.ENTITY_TYPE_NEGATIVE_KEYWORDS

        return self._create_entities(entity_type, data)

    def delete_ads(self, ad_ids):
        """Delete product ads.

        Args:
            ad_ids: long[], IDs of the ads.

        Return:
            Deleted ads.
        """
        return self._delete_entities(
            self.ENTITY_TYPE_PRODUCT_ADS, 'adId', ad_ids)

    def delete_adgroups(self, adgroup_ids):
        """Delete adgroups.

        Args:
            adgroup_ids: long[], IDs of the adgroups.

        Return:
            Deleted adgroups.
        """
        return self._delete_entities(
            self.ENTITY_TYPE_AD_GROUPS, 'adGroupId', adgroup_ids)

    def delete_campaigns(self, campaign_ids):
        """Delete campaigns.

        Args:
            campaign_ids: long[], IDs of the campaigns.

        Return:
            Deleted campaigns.
        """
        return self._delete_entities(
            self.ENTITY_TYPE_CAMPAIGNS, 'campaignId', campaign_ids)

    def get_ads(self, ad_ids=None, adgroup_ids=None, asin=None,
                campaign_ids=None, campaign_type=None, sku=None,
                state=('enabled', 'paused'), load_extended_fields=True):
        """Get a list of product ads.

        Args:
            ad_ids: long[], IDs of ads.
            adgroup_ids: long[], IDs of ad groups.
            asin: string.
            campaign_ids: long[], IDs of campaigns.
            campaign_type: string, type of campaigns.
            sku: string.
            state: string[], state of ads, e.g., enabled, paused, archived.
            load_extended_fields: boolean, if True, retrieve a complete fields
                of ads.

        Return:
            A list of product ads.
        """
        params = {}
        if ad_ids:
            params['adIdFilter'] = ','.join(str(i) for i in ad_ids)
        if adgroup_ids:
            params['adGroupIdFilter'] = ','.join(str(i) for i in adgroup_ids)
        if asin:
            params['asin'] = asin
        if campaign_ids:
            params['campaignIdFilter'] = ','.join(str(i) for i in campaign_ids)
        if campaign_type:
            params['campaignType'] = campaign_type
        if sku:
            params['sku'] = sku
        if state:
            params['stateFilter'] = ','.join(str(i) for i in state)
        if load_extended_fields:
            entity_type = self.ENTITY_TYPE_PRODUCT_ADS + '/extended'
        else:
            entity_type = self.ENTITY_TYPE_PRODUCT_ADS

        return self._get_entities(entity_type, params)

    def get_adgroups(self, adgroup_ids=None, campaign_ids=None,
                     campaign_type=None, name=None,
                     state=('enabled', 'paused'), load_extended_fields=True):
        """Get a list of ad groups.

        Args:
            adgroup_ids: long[], IDs of ad groups.
            campaign_ids: long[], IDs of campaigns.
            campaign_type: string, type of campaign.
            name: string, name of ad group.
            state: string[], state of ad groups, e.g.,
                enabled, paused, archived.
            load_extended_fields: boolean, if True, retrieve a complete fields
                of ad groups.

        Return:
            A list of ad groups.
        """
        params = {}
        if adgroup_ids:
            params['adGroupIdFilter'] = ','.join(str(i) for i in adgroup_ids)
        if campaign_ids:
            params['campaignIdFilter'] = ','.join(str(i) for i in campaign_ids)
        if campaign_type:
            params['campaignType'] = campaign_type
        if name:
            params['name'] = name
        if state:
            params['stateFilter'] = ','.join(str(i) for i in state)
        if load_extended_fields:
            entity_type = self.ENTITY_TYPE_AD_GROUPS + '/extended'
        else:
            entity_type = self.ENTITY_TYPE_AD_GROUPS

        adgroups = self._get_entities(entity_type, params)
        return adgroups

    def get_campaign_by_id(self, campaign_id, load_extended_fields=True,
                           load_nested_ads=False, load_nested_keywords=False):
        """Get campaign details by campaign ID.

        Args:
            campaign_id: long, ID of campaign.
            load_extended_fields: boolean, if True, load a complete fields
                of campaign.
            load_nested_ads: boolean, if True, load ads of the ad groups.
            load_nested_keywords: boolean, if True, load keywords of
                the ad groups.

        Return:
            A dict of campaign details.
        """
        if not campaign_id:
            return None

        campaigns = [
            c for c in self.get_campaigns(
                campaign_ids=[campaign_id],
                load_extended_fields=load_extended_fields,
                load_nested_ads=load_nested_ads,
                load_nested_keywords=load_nested_keywords)]
        return campaigns[0] if campaigns else None

    def get_campaigns(self, campaign_ids=None, campaign_type=None, name=None,
                      state=None, load_extended_fields=True):
        """Get a list of campaigns.

        Args:
            campaign_ids: long[], IDs of campaigns.
            campaign_type: string, type of campaigns.
            name: string, name of campaign.
            state: string, state of campaigns, e.g., enabled, paused, archived.
            load_extended_fields: boolean, if True, load a complete fields
                of campaign.

        Return:
            An iterator of campaign.
        """
        params = {}
        if campaign_ids:
            params['campaignIdFilter'] = ','.join(str(i) for i in campaign_ids)
        if campaign_type:
            params['campaignType'] = campaign_type
        if name:
            params['name'] = name
        if state:
            params['stateFilter'] = state
        if load_extended_fields:
            entity_type = self.ENTITY_TYPE_CAMPAIGNS + '/extended'
        else:
            entity_type = self.ENTITY_TYPE_CAMPAIGNS

        campaigns = self._get_entities(entity_type, params)
        for campaign in campaigns:
            yield campaign

    def get_keywords(self, adgroup_ids=None, campaign_ids=None,
                     campaign_type=None, keyword_ids=None, keyword_text=None,
                     match_type=None, state=None, is_biddable=True,
                     load_extended_fields=True):
        """Get a list of biddable keywords or negative keywords.

        Args:
            adgroup_ids: long[], IDs of ad groups.
            campaign_ids: long[], IDs of campaigns.
            campaign_type: string, type of campaigns.
            keyword_ids: long[], IDs of keywords.
            keyword_text: string.
            match_type: string[].
            state: string, state of keywords, e.g., enabled, paused, archived.
            is_biddable: boolean, True/False: biddable/negative keyword.
            load_extended_fields: boolean, if True, retrieve a complete fields
                of keyword.

        Return:
            A list of biddable keywords or negative keywords.
        """
        params = {}
        if adgroup_ids:
            params['adGroupIdFilter'] = ','.join(str(i) for i in adgroup_ids)
        if campaign_ids:
            params['campaignIdFilter'] = ','.join(str(i) for i in campaign_ids)
        if campaign_type:
            params['campaignType'] = campaign_type
        if keyword_ids:
            params['keywordIdFilter'] = ','.join(str(i) for i in keyword_ids)
        if keyword_text:
            params['keywordText'] = keyword_text
        if match_type:
            params['matchTypeFilter'] = match_type
        if state:
            params['stateFilter'] = state
        if is_biddable:
            entity_type = self.ENTITY_TYPE_BIDDABLE_KEYWORDS
        else:
            entity_type = self.ENTITY_TYPE_NEGATIVE_KEYWORDS
        if load_extended_fields:
            entity_type += '/extended'

        return self._get_entities(entity_type, params)

    def get_report(self, entity_type, report_date, query=None):
        """Get performance report of campaigns/adGroups/...

        Args:
            entity_type: string, type of entity, refer to: _ENTITY_TYPE_*.
            report_date: string, in format: 'YYYYMMDD'.
            query: string, it can only be used in Keyword reports.

        Return:
            A performance report.
        """
        # Request a report.
        url = self.api_endpoint % (entity_type + '/report')
        data = {
            'campaignType': 'sponsoredProducts',
            'segment': query,
            'reportDate': report_date,
            'metrics': (
                'impressions,clicks,cost,attributedConversions1dSameSKU,'
                'attributedConversions1d,attributedSales1dSameSKU,'
                'attributedSales1d,attributedConversions7dSameSKU,'
                'attributedConversions7d,attributedSales7dSameSKU,'
                'attributedSales7d,attributedConversions30dSameSKU,'
                'attributedConversions30d,attributedSales30dSameSKU,'
                'attributedSales30d'),
        }
        self._rebuild_auth()
        response = requests.post(url=url, headers=self.headers, json=data)
        if response.status_code != 202:
            logger.exception(response.content)
            raise AdsAPIError(response.status_code, response.content)

        report_id = response.json()['reportId']

        # Generate the requested report.
        url = self.api_endpoint % (
            self.ENTITY_TYPE_REPORTS + '/' + report_id)
        download_uri = None
        for _ in range(0, 60):
            self._rebuild_auth()
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                if response.json()['status'] == 'SUCCESS':
                    logger.info(response.json())
                    download_uri = response.json().get('location')
                    break
            else:
                logger.exception(response.json())
                if (response.status_code == 404 and
                        response.json().get('code') == 'NOT_FOUND'):
                    break
                else:
                    raise AdsAPIError(response.status_code, response.content)
            time.sleep(5)

        if not download_uri:
            logger.exception('Failed to generate the requested report.')
            return []

        # Download the report.
        self._rebuild_auth(content_type=None)
        # response = requests.get(download_uri, headers=headers, stream=True)
        response = requests.get(download_uri, headers=self.headers)
        if response.status_code == 200:
            report = GzipFile('', 'r', 0, BytesIO(response.content)).read()
            return json.loads(report)
        else:
            logger.exception(response.content)
            raise AdsAPIError(response.status_code, response.content)

    def update_ad(self, ad_id, state=None):
        """Update a product ad.

        Args:
            ad_id: long, ID of product ad.
            state: string, e.g., enabled, paused, archived.

        Return:
            Updated product ad.
        """
        data = {}
        if state:
            data['state'] = state
        if data:
            data['adId'] = ad_id
            response = self._update_entities(
                self.ENTITY_TYPE_PRODUCT_ADS, [data])
            return response

        return None

    def update_adgroup(self, adgroup_id, name=None, default_bid=None,
                       state=None):
        """Update an ad group.

        Args:
            adgroup_id: long, ID of ad group.
            name: string, name of ad group.
            default_bid: float.
            state: string, e.g., enabled, paused, archived.

        Return:
            Updated ad group.
        """
        data = {}
        if name:
            data['name'] = name
        if default_bid is not None:
            data['defaultBid'] = max(float(default_bid), AdsAPIClient.MIN_BID)
        if state:
            data['state'] = state
        if data:
            data['adGroupId'] = adgroup_id
            response = self._update_entities(
                self.ENTITY_TYPE_AD_GROUPS, [data])
            return response

        return None

    def update_campaign(self, campaign_id, name=None, state=None,
                        daily_budget=None, start_date=None, end_date=None,
                        premium_bid_adjustment=None):
        """Update a campaign.

        Args:
            campaign_id: long, ID of campaign.
            name: string, name of campaign.
            state: string, e.g., enabled, paused, archived.
            daily_budget: float.
            start_date: string, format: 'YYYYMMDD'.
            end_date: string, format: 'YYYYMMDD'.
            premium_bid_adjustment: boolean.

        Return:
            Updated campaign.
        """
        data = {}
        if name:
            data['name'] = name
        if state:
            data['state'] = state
        if daily_budget is not None:
            data['dailyBudget'] = max(
                float(daily_budget), AdsAPIClient.MIN_DAILY_BUDGET)
        if start_date:
            data['startDate'] = start_date
        if end_date:
            data['endDate'] = end_date
        if premium_bid_adjustment is not None:
            data['premiumBidAdjustment'] = premium_bid_adjustment
        if data:
            data['campaignId'] = campaign_id
            response = self._update_entities(
                self.ENTITY_TYPE_CAMPAIGNS, [data])
            return response

        return None

    def update_keywords(self, keyword_ids, bid=None, state=None,
                        is_biddable=True):
        """Update biddable keywords or negative keywords.

        Note: keyword can only be updated for keyword-targeted campaign.

        Args:
            keyword_ids: long[], IDs of keywords.
            bid: float.
            state: string, e.g., enabled, paused, archived for biddable
                keywords; enabled, disabled for negative keywords.
            is_biddable: boolean, True/False: biddable/negative keyword.

        Return:
            Updated biddable keywords or negative keywords.
        """
        data = [
            {
                'bid': max(float(bid), AdsAPIClient.MIN_BID) if bid else None,
                'state': state,
                'keywordId': k_id,
            } for k_id in keyword_ids
        ]
        if is_biddable:
            entity_type = self.ENTITY_TYPE_BIDDABLE_KEYWORDS
        else:
            entity_type = self.ENTITY_TYPE_NEGATIVE_KEYWORDS

        return self._update_entities(entity_type, data)

    def update_keywords_v2(self, data, is_biddable=True):
        """Update biddable keywords or negative keywords.

        Note: keyword can only be updated for keyword-targeted campaign.

        Args:
            data: a list of keyword info of type dict, refer to method:
                get_keyword_to_update().
            is_biddable: boolean, True/False: biddable/negative keyword.

        Return:
            Updated biddable keywords or negative keywords.
        """
        if not data:
            return

        if is_biddable:
            entity_type = self.ENTITY_TYPE_BIDDABLE_KEYWORDS
        else:
            entity_type = self.ENTITY_TYPE_NEGATIVE_KEYWORDS

        return self._update_entities(entity_type, data)

    def _create_entities(self, entity_type, data):
        """Create entities, e.g., Campaign, Ad Group.

        Args:
            entity_type: string, type of the entity, e.g., 'adGroups'.
            data: dict[], data to be created.

        Return:
            Created entities.
        """
        # Build URL endpoint for POST method.
        url = self.api_endpoint % entity_type

        self._rebuild_auth()
        response = requests.post(
            url, data=json.dumps(data), headers=self.headers)
        if response.status_code != 207:
            raise AdsAPIError(
                response.status_code, response.json()['details'])

        return response.json()

    def _delete_entities(self, entity_type, entity_id_field, entity_ids):
        """Archive entities as deleted.

        Note: Archived entities cannot be made active again.

        Args:
            entity_type: string, type of the entity, e.g., 'adGroups'.
            entity_id_field: string, e.g., 'campaignId', 'adGroupId'.
            entity_ids: long[], IDs of entities to be archived.

        Return:
            Archived entities.
        """
        # Build URL endpoint for PUT method.
        url = self.api_endpoint % entity_type

        data = [{entity_id_field: long(entity_id), 'state': 'archived'}
                for entity_id in entity_ids]
        self._rebuild_auth()
        response = requests.put(
            url, data=json.dumps(data), headers=self.headers)
        if response.status_code != 200:
            raise AdsAPIError(
                response.status_code, response.json()['details'])

        return response.json()

    def _get_entities(self, entity_type, params=None, page_offset=-1,
                      page_size=_PAGE_SIZE):
        """Get entities (e.g., Campaign, Ads).

        Args:
            entity_type: string, type of the entity, e.g., 'adGroups'.
            params: dict, search parameters.
            page_offset: int, start index of a page of entities. If page_offset
                equals to -1, fetch all pages; otherwise, fetch only one page.
            page_size: int, maximum number of entities to return in the page.

        Return:
            A list of entities.
        """
        # Build URL endpoint for GET method.
        url = self.api_endpoint % entity_type

        if not params:
            params = {}

        entities = []
        if page_offset == -1:
            params['startIndex'] = 0
            params['count'] = page_size
            more_pages = True
            while more_pages:
                self._rebuild_auth()
                response = requests.get(
                    url, headers=self.headers, params=params)
                if (response.status_code == 200 and
                        isinstance(response.json(), list) and
                        len(response.json()) > 0):
                    entities.extend(response.json())
                    params['startIndex'] += page_size
                    more_pages = len(response.json()) == page_size
                else:
                    more_pages = False
        else:
            params['startIndex'] = page_offset
            params['count'] = page_size
            self._rebuild_auth()
            response = requests.get(url, headers=self.headers, params=params)
            entities = response.json()

        return entities

    def _update_entities(self, entity_type, data):
        """Update entities, e.g., Campaign, Ad Group.

        Args:
            entity_type: string, type of the entity, e.g., 'adGroups'.
            data: dict[], list of data to be updated.

        Return:
            Updated entities.
        """
        # Build URL endpoint for PUT method.
        url = self.api_endpoint % entity_type

        self._rebuild_auth()
        response = requests.put(
            url, data=json.dumps(data), headers=self.headers)
        if response.status_code != 207:
            raise AdsAPIError(
                response.status_code, response.json()['details'])

        return response.json()
