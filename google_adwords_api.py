# -*- coding: utf-8 -*-
from collections import OrderedDict
from copy import deepcopy
from datetime import date
from datetime import datetime
import logging
import suds
import urllib

from googleads.adwords import AdWordsClient
from googleads.oauth2 import GoogleRefreshTokenClient

from .google_api_setting import COUNTRIES
from .google_api_setting import LANGUAGES
from .google_api_setting import SELECTOR_FIELDS



logging.getLogger('suds.client').setLevel(logging.CRITICAL)
logging.getLogger('suds.resolver').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)



class GoogleAdsClient(ads_api.AdsAPIClient):
    API_VERSION = 'v201702'

    STATUS_ACTIVE = 'ENABLED'
    STATUS_PAUSED = 'PAUSED'
    STATUS_DELETED = 'REMOVED'
    ALLOWED_CAMPAIGN_STATUS = (STATUS_ACTIVE, STATUS_PAUSED)
    EQUIV_CAMPAIGN_ACTIVE = (STATUS_ACTIVE, )
    EQUIV_CAMPAIGN_PAUSED = (STATUS_PAUSED, )

    CAMPAIGN_NAME_FIELD = 'name'
    CAMPAIGN_ID_FIELD = 'id'
    CAMPAIGN_STATUS_FIELD = 'status'

    # Targeted device. Mapping from device name to criteria ID:
    # {'Desktop': 30000, 'HighEndMobile': 30001, 'Tablet': 30002}.
    DEVICE_PC = (30000, )
    DEVICE_MOBILE = (30001, 30002)
    DEVICE_MOBILEANDPC = (30000, 30001, 30002)
    ALLOWED_DEVICES = (DEVICE_PC, DEVICE_MOBILE, DEVICE_MOBILEANDPC)

    COUNTRY_CODES = [country_code for country_code, _ in COUNTRIES]
    LANGUAGE_CODES = [lang_code for lang_code, _ in LANGUAGES]

    _COUNTRY_TO_CRITERIA_MAP = dict((country_code, criteria_id)
                                    for country_code, criteria_id in COUNTRIES)
    _CRITERIA_TO_COUNTRY_MAP = dict((criteria_id, country_code)
                                    for country_code, criteria_id in COUNTRIES)
    _LANGUAGE_TO_CRITERIA_MAP = dict((lang_code, criteria_id)
                                     for lang_code, criteria_id in LANGUAGES)

    _DEFAULT_END_DATE = '20371230'      # Default end date of campaign.

    _PAGE_SIZE = 50              # Number of entities fetched per API request.
    _PAGE_SIZE_CRITERION = 2000  # Number of criteria fetched per API request.
    _BATCH_SIZE = 1000           # Number of entities updated per API request.

    # Attributes to be overridden as following.
    ADVERTISING_CHANNEL_TYPE = None     # e.g., 'SEARCH', 'DISPLAY'.

    TARGET_GOOGLE_SEARCH = 'true'
    TARGET_SEARCH_NETWORK = 'true'
    TARGET_CONTENT_NETWORK = 'true'
    TARGET_PARTNER_SEARCH_NETWORK = 'false'

    def __init__(self):
        super(GoogleAdsClient, self).__init__()
        self.client = None

    def _auth_impl(self):
        self.client = AdWordsClient(
            'Your Developer Token',
            GoogleRefreshTokenClient(
                'Your Client ID',
                'Your Client Secret',
                'Your Refresh Token'),
            'Your User Agent ID'
        )
        self.client.SetClientCustomerId('Your Client Customer ID')

    def _create_ad(self, adgroup_id, creative, dest_url=None, display_url=None,
                   status='ENABLED', **kwargs):
        """Create an ad which is assigned to an ad group.

        Args:
            adgroup_id: long, ID of the assigned ad group.
            creative: dict, ad creative.
            dest_url: string, destination URL of the ads.
            display_url: string, display URL of the ads.
            status: string, status of the ad, e.g., ENABLED, PAUSED, REMOVED.
            kwargs: keyword arguments, additional data.

        Returns:
            A new object of type AdGroupAd.

        Raises:
            AdsAPIError: errors occurred when prepare data for template ad.
        """
        if not (adgroup_id and creative):
            return None

        ad = None
        if creative.get('type') == 'TextAd':
            ad = {
                'description1': creative.get('description1'),
                'description2': creative.get('description2'),
                'headline': creative.get('headline'),
            }
        elif creative.get('type') == 'ExpandedTextAd':
            ad = {
                'headlinePart1': creative.get('headlinePart1'),
                'headlinePart2': creative.get('headlinePart2'),
                'description':  creative.get('description'),
            }
        elif creative.get('type') == 'ImageAd':
            ad = {
                'name': creative.get('name') or (
                    'Ad Image #' + datetime.utcnow().strftime('%Y%m%d%H%M%S')),
            }
            if creative.get('data'):
                ad['image'] = {
                    'data': creative.get('data'),
                }
            if creative.get('copy_ad_id'):
                ad['adToCopyImageFrom'] = creative['copy_ad_id']
        elif creative.get('type') == 'TemplateAd':
            media_bundle = {
                'xsi_type': 'MediaBundle',
                'data': creative.get('data'),
                # 'entryPoint': 'index.html',
                'type': 'MEDIA_BUNDLE',
            }
            template_elements = [
                {
                    'uniqueName': 'adData',
                    'fields': [
                        # Required fields.
                        {
                            'name': 'Custom_layout',
                            'type': 'MEDIA_BUNDLE',
                            'fieldMedia': media_bundle,
                        },
                        {
                            'name': 'layout',
                            'type': 'ENUM',
                            'fieldText': 'Custom',
                        },
                    ]
                },
            ]
            ad = {
                'name': creative.get('name') or (
                    'Ad Idea #' + datetime.utcnow().strftime('%Y%m%d%H%M%S')),
                'templateId': 419,      # HTML5 bundle.
                'templateElements': template_elements,
            }

        if ad:
            ad.update({
                'xsi_type': creative.get('type'),
                'finalUrls': [dest_url or creative.get('dest_url')],
            })
            if creative.get('type') != 'ExpandedTextAd':
                ad['displayUrl'] = display_url or creative.get('display_url')
            data_added = {
                # Required fields.
                'xsi_type': 'AdGroupAd',
                'adGroupId': adgroup_id,
                'ad': ad,
                # Optional fields.
                'status': status,
            }
            data_added.update(kwargs)
            ads = self._update_entities(
                'AdGroupAdService',
                [self._get_operation('ADD', **data_added)]
            )
            return ads[0] if ads else None
        return None

    def _create_adgroup(self, campaign_id, adgroup_name, max_cpc,
                        status='ENABLED', **kwargs):
        """Create an ad group which is assigned to a campaign.

        Args:
            campaign_id: long, ID of the assigned campaign.
            adgroup_name: string, name of the ad group.
            max_cpc: long, maximum CPC (in micro) of the ad group.
            status: string, status of the ad group, e.g.,
                UNKNOWN, ENABLED, PAUSED, REMOVED.
            kwargs: keyword arguments, additional data.

        Returns:
            A new object of type AdGroup.
        """
        data_added = {
            # Required fields.
            'campaignId': campaign_id,
            'name': adgroup_name,
            # Optional fields.
            'biddingStrategyConfiguration': {
                'biddingStrategyType': 'MANUAL_CPC',
                'bids': [{
                    'xsi_type': 'CpcBid',
                    'bid': {'microAmount': max_cpc}
                }]
            },
            'status': status,
            'settings': [
                {
                    'xsi_type': 'TargetingSetting',
                    'details': [
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'AGE_RANGE',
                            'targetAll': 'true',
                        },
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'GENDER',
                            'targetAll': 'true',
                        },
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'PARENT',
                            'targetAll': 'true',
                        },
                    ],
                },
            ],
        }
        data_added.update(kwargs)
        adgroups = self._update_entities(
            'AdGroupService',
            [self._get_operation('ADD', **data_added)]
        )
        return adgroups[0] if adgroups else None

    def _create_budget(self, micro_amount, budget_name=None, **kwargs):
        """Create an object of type Budget.

        Args:
            micro_amount: long, the budget represented in micros.
            name: string, name of the budget.
            kwargs: keyword arguments, additional data.

        Returns:
            A new object of type Budget.
        """
        if not budget_name:
            budget_name = 'Budget #' + datetime.utcnow().strftime(
                '%Y%m%d%H%M%S%f')
        data_added = {
            'name': budget_name,
            'amount': {'microAmount': micro_amount},
            'deliveryMethod': 'STANDARD',
            'isExplicitlyShared': False,    # Exclusively used in one campaign.
        }
        data_added.update(kwargs)
        budgets = self._update_entities(
            'BudgetService',
            [self._get_operation('ADD', **data_added)]
        )
        return budgets[0] if budgets else None

    def _create_campaign(self, campaign_name, budget_amount, start_date,
                         end_date=_DEFAULT_END_DATE, status='ENABLED',
                         ad_channel_type=ADVERTISING_CHANNEL_TYPE, **kwargs):
        """Create a campaign to the client account.

        Args:
            campaign_name: string, name of the campaign.
            budget_amount: long, budget (in micros) of the campaign.
            start_date: string, date the campaign begins, format: 'YYYYMMDD'.
            end_date: string, date the campaign ends, format: 'YYYYMMDD'.
            status: string, status of the campaign, e.g.,
                UNKNOWN, ENABLED, PAUSED, REMOVED.
            ad_channel_type: string, the primary serving target for ads
                within the campaign, e.g., UNKNOWN, SEARCH, DISPLAY, SHOPPING.
            kwargs: keyword arguments, additional data.

        Returns:
            A new object of type Campaign.
        """
        # Set budget.
        budget = self._create_budget(budget_amount)

        data_added = {
            # Required fields.
            'name': campaign_name,
            'advertisingChannelType': ad_channel_type,
            'biddingStrategyConfiguration': {
                'biddingStrategyType': 'MANUAL_CPC',
            },
            # Optional fields.
            'budget': {
                'budgetId': budget['budgetId']
            },
            'networkSetting': {
                'targetGoogleSearch': self.TARGET_GOOGLE_SEARCH,
                'targetSearchNetwork': self.TARGET_SEARCH_NETWORK,
                'targetContentNetwork': self.TARGET_CONTENT_NETWORK,
                'targetPartnerSearchNetwork':
                    self.TARGET_PARTNER_SEARCH_NETWORK,
            },
            'startDate': start_date,
            'endDate': end_date,
            'status': status,
            'settings': [
                {
                    'xsi_type': 'GeoTargetTypeSetting',
                    'positiveGeoTargetType': 'LOCATION_OF_PRESENCE',
                },
            ],
        }
        data_added.update(kwargs)
        campaigns = self._update_entities(
            'CampaignService',
            [self._get_operation('ADD', **data_added)]
        )
        return campaigns[0] if campaigns else None

    def _create_campaign_criteria(self, campaign_id, country, language,
                                  device):
        """Create targeting criteria which is assigned to a campaign.

        Args:
            campaign_id: long, ID of the assigned campaign.
            country: string, code of targeting country, e.g. US, GB.
            language: string, code of targeting languages, e.g. en, zh_CN.
            device: long[], a tuple of criteria IDs of devices.

        Returns:
            A list of new objects of type CampaignCriterion.
        """
        if not (country or language or device is not None):
            return []

        operations = []
        # Get criterion ID of targeting locations via LocationCriterionService.
        # Refer to the documentation:
        # https://developers.google.com/adwords/api/docs/appendix/geotargeting
        if country:
            location_id = self._COUNTRY_TO_CRITERIA_MAP.get(country)
            if location_id:
                # Set targeting locations for campaign.
                operations.append(
                    self._get_operation(
                        'ADD', campaignId=campaign_id,
                        criterion={'xsi_type': 'Location', 'id': location_id})
                )
            else:
                raise ads_api.InvalidParameterError(
                    'Country %s is invalid.' % country)

        # Get criterion ID of targeting languages via ConstantDataService.
        # Refer to the documentation:
        # https://developers.google.com/adwords/api/docs/appendix/languagecodes
        if language:
            language_id = self._LANGUAGE_TO_CRITERIA_MAP.get(language)
            if language_id:
                # Set targeting languages for campaign.
                operations.append(
                    self._get_operation(
                        'ADD', campaignId=campaign_id,
                        criterion={'xsi_type': 'Language', 'id': language_id})
                )
            else:
                raise ads_api.InvalidParameterError(
                    'Language %s is invalid.' % language)

        # Set targeted platform. Refer to Codes & Formats in AdWords API Docs.
        if device is not None:
            for criterion_id in self.DEVICE_MOBILEANDPC:
                bid_modifier = 1
                if criterion_id not in device:
                    bid_modifier = 0
                operations.append(
                    self._get_operation(
                        'SET', campaignId=campaign_id,
                        criterion={'xsi_type': 'Platform', 'id': criterion_id},
                        bidModifier=bid_modifier,
                    )
                )

        return self._update_entities('CampaignCriterionService', operations)

    def _create_keyword(self, adgroup_id, text, match_type='BROAD', **kwargs):
        """Create a keyword which is assigned to an ad group.

        Args:
            adgroup_id: long, ID of the assigned ad group.
            text: string, text of the keyword.
            match_type: string, match type of the keyword, e.g.,
                EXACT, PHRASE, BROAD.
            kwargs: keyword arguments, additional data.

        Returns:
            A new object of type Keyword.
        """
        data_added = {
            # Required fields.
            'xsi_type': 'BiddableAdGroupCriterion',
            'adGroupId': adgroup_id,
            'criterion': {
                'xsi_type': 'Keyword',
                'matchType': match_type,
                'text': text
            }
        }
        data_added.update(kwargs)
        keywords = self._update_entities(
            'AdGroupCriterionService',
            [self._get_operation('ADD', **data_added)]
        )
        return keywords[0] if keywords else None

    def _delete_ads(self, adgroup_id, ad_ids):
        """Delete ads which are assigned to an ad group.

        Args:
            adgroup_ids: long[], list of ad group IDs.
            ad_ids: long[], list of ad IDs.

        Returns:
            Deleted ads.
        """
        if adgroup_id and ad_ids:
            operations = []
            for ad_id in ad_ids:
                data_deleted = {
                    'adGroupId': adgroup_id,
                    'ad': {
                        'id': ad_id
                    },
                }
                operations.append(
                    self._get_operation('REMOVE', **data_deleted))
            if operations:
                return self._update_entities('AdGroupAdService', operations)
        return []

    def _delete_adgroups(self, adgroup_ids):
        """Delete ad groups.

        Args:
            adgroup_ids: long[], list of ad group IDs.

        Returns:
            Deleted ad groups.
        """
        operations = []
        for adgroup_id in adgroup_ids:
            data_deleted = {
                'id': adgroup_id,
                'status': 'REMOVED',
            }
            operations.append(self._get_operation('SET', **data_deleted))
        if operations:
            return self._update_entities('AdGroupService', operations)
        return []

    def _delete_budgets(self, budget_ids):
        """Delete budgets.

        Args:
            budget_ids: long[], list of budget IDs.

        Returns:
            Deleted budgets.
        """
        operations = []
        for budget_id in budget_ids:
            data_deleted = {
                'budgetId': budget_id,
                'status': 'REMOVED',
            }
            operations.append(self._get_operation('SET', **data_deleted))
        if operations:
            return self._update_entities('BudgetService', operations)
        return []

    def _delete_campaigns(self, campaign_ids):
        """Delete campaigns.

        Args:
            campaign_ids: long[], list of campaign IDs.

        Returns:
            Deleted campaigns.
        """
        operations = []
        for campaign_id in campaign_ids:
            data_deleted = {
                'id': campaign_id,
                'status': 'REMOVED',
            }
            operations.append(self._get_operation('SET', **data_deleted))
        if operations:
            return self._update_entities('CampaignService', operations)
        return []

    def _get_adgroups(self, adgroup_ids, campaign_ids, fields=None,
                      load_nested_ads=False, load_nested_keywords=False):
        """Get ad groups by given ad group IDs and/or campaign IDs.

        Args:
            adgroup_ids: long[], list of ad group IDs.
            campaign_ids: long[], list of campaign IDs.
            fields: string[], list of fields to select.
            load_nested_ads: bool, if True, load ads of the ad groups.
            load_nested_keywords: bool, if True, load keywords of
                the ad groups.

        Return:
            A list of ad groups.
        """
        predicates = []
        if adgroup_ids:
            predicates.append(self._get_predicate('Id', 'IN', adgroup_ids))
        if campaign_ids:
            predicates.append(
                self._get_predicate('CampaignId', 'IN', campaign_ids))
        if not predicates:
            return []

        # Get ad groups.
        adgroups = self._get_entities(
            'AdGroupService',
            self._get_selector(
                fields=fields or SELECTOR_FIELDS['ADGROUP'],
                predicates=predicates,
            )
        )

        if not adgroups:
            return []

        # Get the ads, keywords of the selected ad groups.
        if load_nested_ads or load_nested_keywords:
            adgroup_ids = [ag['id'] for ag in adgroups]
            if load_nested_ads:
                ads = self._get_ads(adgroup_ids)
                self.merge_up_entities(adgroups, ads, 'id', 'adGroupId', 'ads')
            if load_nested_keywords:
                keywords = self._get_keywords(adgroup_ids)
                self.merge_up_entities(
                    adgroups, keywords, 'id', 'adGroupId', 'keywords')

        return adgroups

    def _get_ad(self, adgroup_id, ad_id, fields=None):
        """Get ad by ad group ID and ad ID.

        Args:
            adgroup_id: long, ID of ad group.
            ad_id: long, ID of ad.
            fields: string[], list of fields to select.

        Return:
            An object of AdGroupAd.
        """
        if adgroup_id and ad_id:
            ads = self._get_entities(
                'AdGroupAdService',
                self._get_selector(
                    fields=fields or SELECTOR_FIELDS['AD'],
                    predicates=[
                        self._get_predicate('AdGroupId', 'EQUALS', adgroup_id),
                        self._get_predicate('Id', 'EQUALS', ad_id),
                    ]
                )
            )
            return ads[0] if ads else None
        return None

    def _get_ads(self, adgroup_ids, fields=None):
        """Get ads of the specified ad groups.

        Args:
            adgroup_ids: long[], list of ad group IDs.
            fields: string[], list of fields to select.

        Return:
            A list of ads.
        """
        if adgroup_ids:
            return self._get_entities(
                'AdGroupAdService',
                self._get_selector(
                    fields=fields or SELECTOR_FIELDS['AD'],
                    predicates=[
                        self._get_predicate('AdGroupId', 'IN', adgroup_ids),
                    ]
                )
            )
        return []

    def _get_budgets(self, budget_ids, budget_names, campaign_ids):
        """Get budgets.

        Args:
            budget_ids: long[], list of budget IDs.
            budget_names: string[], list of budget names.
            campaign_ids: long[], list of campaign IDs.

        Returns:
            A list of budgets.
        """
        if not budget_ids:
            budget_ids = []

        if budget_names:
            budgets = self._get_entities(
                'BudgetService',
                self._get_selector(
                    fields=['BudgetId'],
                    predicates=[
                        self._get_predicate(
                            'BudgetName', 'IN', budget_names),
                    ],
                )
            )
            budget_ids.extend([b['budgetId'] for b in budgets])

        if campaign_ids:
            budgets = self._get_entities(
                'CampaignService',
                self._get_selector(
                    fields=['BudgetId'],
                    predicates=[
                        self._get_predicate('Id', 'IN', campaign_ids),
                    ],
                )
            )
            budget_ids.extend([b['budget']['budgetId'] for b in budgets])

        budget_ids = list(set(budget_ids))
        if not budget_ids:
            return []

        budgets = self._get_entities(
            'BudgetService',
            self._get_selector(
                fields=SELECTOR_FIELDS['BUDGET'],
                predicates=[
                    self._get_predicate('BudgetId', 'IN', budget_ids),
                ],
            )
        )
        return budgets

    def _get_campaign_criteria(self, campaign_ids):
        """Get campaign criteria of the specified campaigns.

        Args:
            campaign_ids: long[], list of campaign IDs.

        Return:
            A list of campaign criteria.
        """
        if not campaign_ids:
            return []

        campaign_criteria = self._get_entities(
            'CampaignCriterionService',
            self._get_selector(
                fields=SELECTOR_FIELDS['CAMPAIGN_CRITERION'],
                predicates=[
                    self._get_predicate('CampaignId', 'IN', campaign_ids),
                ]
            ),
            self._PAGE_SIZE_CRITERION
        )
        return campaign_criteria

    def _get_campaigns_by_ids(self, campaign_ids, load_nested_entities=False):
        """Get campaigns by IDs.

        Args:
            campaign_ids: long[], list of campaign IDs.
            load_nested_entities: bool, if true, load nested entities inside
                campaign, e.g. ad groups.

        Return:
            A list of objects including campaigns (and nested ad groups & ads).
        """
        if not campaign_ids:
            return []

        campaigns = self._get_entities(
            'CampaignService',
            self._get_selector(
                fields=SELECTOR_FIELDS['CAMPAIGN'],
                predicates=[
                    self._get_predicate('Id', 'IN', [campaign_ids]),
                ],
            )
        )
        if not campaigns:
            return []

        if load_nested_entities:
            # Get campaign criteria and ad groups of the selected campaigns.
            campaign_ids = [item['id'] for item in campaigns]
            campaign_criteria = self._get_campaign_criteria(campaign_ids)
            adgroups = self._get_adgroups(None, campaign_ids, None, True, True)
            self.merge_up_entities(
                campaigns, campaign_criteria, self.CAMPAIGN_ID_FIELD,
                'campaignId', 'criterion')
            self.merge_up_entities(
                campaigns, adgroups, self.CAMPAIGN_ID_FIELD,
                'campaignId', 'adgroups')

        return campaigns

    def _get_entities(self, service_name, selector, page_size=_PAGE_SIZE):
        """Get entities (e.g., Campaign, AdGroup) via API services.

        If paging information is given in selector, fetch the specified
        pages; otherwise, retrieve all pages.

        Args:
            service_name: string, service name, e.g., 'CampaignService'.
            selector: Selector, filters for retrieving entities.
            page_size: int, maximum number of results to return in the page.

        Returns:
            A dict which represents the selected entities.
        """
        # Initialize the service.
        service = self.client.GetService(
            service_name, version=self.API_VERSION)

        # If paging is given, select the entities specified by the paging;
        # otherwise, retrieve all the entities.
        entities = []
        if 'paging' in selector:
            logger.debug('GoogleAdsClient get entity %s, %s',
                         service_name, selector)
            page = service.get(selector)
            if page and 'entries' in page:
                entities = page['entries']
        else:
            logger.debug('GoogleAdsClient get all entities %s', service_name)
            offset = 0
            more_pages = True
            while more_pages:
                selector['paging'] = self._get_paging(offset, page_size)
                logger.debug('GoogleAdsClient get entity %s, %s',
                             service_name, selector)
                page = service.get(selector)
                if page and 'entries' in page:
                    entities.extend(page['entries'])
                    offset += page_size
                    more_pages = offset < int(page['totalNumEntries'])
                else:
                    more_pages = False

        return [self.convert_suds_to_dict(e) for e in entities]

    def _get_keyword_performance(self, min_date, max_date, adgroup_ids=None):
        """Get AdWords performance statistics aggregated at the keyword level.

        Args:
            min_date: string, start date which should be in 'YYYYMMDD' format.
            max_date: string, end date which should be in 'YYYYMMDD' format.
            adgroup_ids: long[], a list of ad group IDs.

        Return:
            A custom report of keyword performance metrics.
        """
        predicates = []
        if adgroup_ids:
            predicates = [
                self._get_predicate('AdGroupId', 'IN', adgroup_ids),
            ]

        return self._get_report('Keyword Performance Report',
                                'KEYWORDS_PERFORMANCE_REPORT',
                                PERF_REPORT_FIELDS_OF_KEYWORD,
                                min_date,
                                max_date,
                                predicates)

    def _get_keywords(self, adgroup_ids):
        """Get keywords of the specified ad groups.

        Args:
            adgroup_ids: long[], a list of ad group IDs.

        Return:
            A list of keywords.
        """
        if not adgroup_ids:
            return []

        keywords = self._get_entities(
            'AdGroupCriterionService',
            self._get_selector(
                fields=SELECTOR_FIELDS['ADGROUP_CRITERION'],
                predicates=[
                    self._get_predicate('AdGroupId', 'IN', adgroup_ids),
                    self._get_predicate('CriteriaType', 'EQUALS', 'KEYWORD'),
                ]
            ),
            self._PAGE_SIZE_CRITERION
        )
        return keywords

    def _get_report(self, report_name, report_type, fields, min_date, max_date,
                    predicates=None):
        """Get AdWords report.

        Args:
            report_name: string, report name.
            report_type: string, report type, e.g., 'AD_PERFORMANCE_REPORT'.
            fields: list, list of fields to be queried.
            min_date: string, start date which should be in 'YYYYMMDD' format.
            max_date: string, end date which should be in 'YYYYMMDD' format.
            predicates: Predicate[], query filters.

        Return:
            A dict of custom report.
        """
        report = {
            'reportName': report_name,
            'reportType': report_type,
            'dateRangeType': 'CUSTOM_DATE',
            'downloadFormat': 'CSV',
            'selector': {
                'fields': fields,
                'dateRange': {
                    'min': min_date,
                    'max': max_date
                }
            }
        }

        if predicates:
            report['selector']['predicates'] = predicates

        downloader = self.client.GetReportDownloader(self.API_VERSION)
        csv_str = downloader.DownloadReportAsString(
            report,
            skip_report_header=True,
            skip_column_header=True,
            skip_report_summary=True,
            include_zero_impressions=False
        )
        # return [dict(zip(fields, row))
        #         for row in csv_util.parse_csv_string(csv_str)]
        for row in csv_util.parse_csv_string(csv_str):
            yield dict(zip(fields, row))

    def _update_ad(self, ad, creative=None, dest_url=None, display_url=None):
        """Update an ad.

        Args:
            ad: AdGroupAd.Ad, ad to be updated.
            creative: dict, ad creative, if {}, delete ad only.
            dest_url: string, destination URL of the ad.
            display_url: string, display URL of the ad.

        Returns:
            An updated ad.
        """
        if not ad or not (creative is not None or dest_url or display_url):
            return None

        # Note: Since API only supports some specific template ad IDs,
        # leave template ad excluding template id 419 out for now.
        # Refer to: https://goo.gl/c8v67d
        if (ad['ad']['Ad.Type'] == 'TemplateAd' and
                ad['ad']['templateId'] != 419):
            return None

        # Note: Creative changes only for text ad, image ad and
        # template ad with template id 419 for now.
        if (creative is not None and
            (ad['ad']['Ad.Type'] == 'TextAd' or
             ad['ad']['Ad.Type'] == 'ImageAd' or
             ad['ad']['Ad.Type'] == 'ExpandedTextAd' or
             (ad['ad']['Ad.Type'] == 'TemplateAd' and
              ad['ad']['templateId'] == 419))):
            ad_new = None
            ad_creative = self.get_creative_from_ad(ad)
            if creative is {}:
                self._delete_ads(ad['adGroupId'], [ad['ad']['id']])
            elif ad_creative != creative:
                ad_new = self._create_ad(
                    ad['adGroupId'], creative, dest_url, display_url)
                self._delete_ads(ad['adGroupId'], [ad['ad']['id']])
            return ad_new

        ad_c = deepcopy(ad)
        need_to_update = False

        if dest_url:
            ad_c['ad']['finalUrls'] = [dest_url]
            need_to_update = True

        # Note: Expanded text ads do not use displayUrl.
        if display_url and ad_c['ad']['Ad.Type'] != 'ExpandedTextAd':
            ad_c['ad']['displayUrl'] = display_url
            need_to_update = True

        if need_to_update:
            # Delete ad and add ad in one API request to keep consistence.
            data_deleted = {
                'adGroupId': ad_c['adGroupId'],
                'ad': {
                    'id': ad_c['ad']['id']
                }
            }

            ad_c['ad'].pop('id')
            ad_c['ad']['xsi_type'] = ad_c['ad'].pop('Ad.Type')
            if ad_c['ad']['xsi_type'] == 'ImageAd':
                ad_c['ad'] = {
                    'xsi_type': 'ImageAd',
                    'finalUrls': [dest_url],
                    'displayUrl': display_url or ad['ad']['displayUrl'],
                    'name': ad['ad']['name'],
                    'adToCopyImageFrom': ad['ad']['id'],
                }

            data_added = {
                'xsi_type': 'AdGroupAd',
                'adGroupId': ad_c['adGroupId'],
                'ad': ad_c['ad'],
                'status': ad_c['status'],
            }
            ads = self._update_entities(
                'AdGroupAdService',
                [self._get_operation('ADD', **data_added),
                 self._get_operation('REMOVE', **data_deleted)]
            )
            return ads[0] if ads else None
        return None

    def _update_campaign_criteria(self, campaign_id, country, language,
                                  device):
        """Update targeting criteria which is assigned to a campaign.

        Args:
            campaign_id: long, ID of the assigned campaign.
            country: string, code of targeting country, e.g. US, GB.
            language: string, code of targeting languages, e.g. en, zh_CN.
            device: long[], a tuple of criteria IDs of devices.

        Returns:
            A list of updated objects of type CampaignCriterion.
        """
        # Remove existing criteria firstly, then add new criteria.
        campaign_criteria = self._get_campaign_criteria([campaign_id])
        if campaign_criteria:
            operations = []
            for criterion in campaign_criteria:
                if ((country and
                     criterion['criterion']['Criterion.Type'] == 'Location') or
                    (language and
                     criterion['criterion']['Criterion.Type'] == 'Language')):
                    operations.append(self._get_operation(
                        'REMOVE', campaignId=campaign_id,
                        criterion={'id': criterion['criterion']['id']}))
            if operations:
                self._update_entities('CampaignCriterionService', operations)

        return self._create_campaign_criteria(
            campaign_id, country, language, device)

    def _update_entities(self, service_name, operations,
                         partial_failure=False):
        """Update entities (e.g., Campaign, AdGroup) via API services.

        Args:
            service_name: string, service name, e.g., 'CampaignService'.
            operations: Operation[], list of operators & operands.
            partial_failure: boolean, true when it is allowed to commit valid
                operations and return failed ones instead of raise errors.

        Returns:
            A list of updated objects (and a list of partial failure errors).
        """
        if not (service_name and operations):
            return ([], []) if partial_failure else []

        if partial_failure:
            self.client.partial_failure = True

        service = self.client.GetService(
            service_name, version=self.API_VERSION)
        response = service.mutate(operations)
        self.client.partial_failure = False
        if partial_failure:
            return (response['value'],
                    response['partialFailureErrors']
                    if 'partialFailureErrors' in response else [])
        else:
            return response['value']

    def _update_keywords_impl(self, adgroup_id, criterion_ids, max_cpc=None,
                              status=None):
        """Update bid amount or status of keywords.

        Args:
            adgroup_id: long, ID of the assigned ad group.
            criterion_ids: long[], list of keyword IDs.
            max_cpc: long, maximum CPC (in micros) of the keyword.
            status: string, e.g., ENABLED, REMOVED, PAUSED.

        Returns:
            List of updated keywords and list of partial errors.
        """
        if not (adgroup_id and criterion_ids and (max_cpc or status)):
            return None

        operations = []
        for criterion_id in criterion_ids:
            data_to_update = {
                'xsi_type': 'BiddableAdGroupCriterion',
                'adGroupId': adgroup_id,
                'criterion': {
                    'id': criterion_id
                },
            }
            if max_cpc:
                data_to_update['biddingStrategyConfiguration'] = {
                    'bids': [{
                        'xsi_type': 'CpcBid',
                        'bid': {
                            'microAmount': max_cpc
                        }
                    }]
                }
            if status:
                data_to_update['userStatus'] = status
            operations.append(self._get_operation('SET', **data_to_update))
        keywords, partial_errors = self._update_entities(
            'AdGroupCriterionService', operations, True)
        return keywords, partial_errors

    @staticmethod
    def _get_data_range(since='19700101', until='20380101'):
        """Get an object of type DateRange. The date format is YYYYMMDD.

        Args:
            since: string, the lower bound of the date range, inclusive.
            until: string, the upper bound of the date range, inclusive.

        Returns:
            A dict which represents an object of type DateRange.
        """
        return {'min': since, 'max': until}

    @staticmethod
    def _get_operation(operator, **operand):
        """Generate an object of a subtype of Operation, e.g. CampaignOperation.

        Args:
            operator: Operator, e.g., 'ADD', 'REMOVE', 'SET'.
            operand: specified type (e.g., Campaign), the keyword arguments:
                id: long, ID of the campaign.
                name: string, name of the campaign.
                ...

        Returns:
            A dict which represents an object of a subtype of Operation.
        """
        if not operator or not operand:
            return None

        return {'operator': operator, 'operand': operand}

    @staticmethod
    def _get_ordering(field, sort_order='ASCENDING'):
        """Get an object of type OrderBy.

        Args:
            field: string, the field to sort the results on.
            sortOrder: string, the order to sort the results on.
                       Possible values: ASCENDING, DESCENDING.

        Returns:
            A dict which represents an object of type OrderBy.
        """
        return {'field': field, 'sortOrder': sort_order}

    @staticmethod
    def _get_paging(start_index, number_results):
        """Get an object of type Paging.

        Args:
            start_index: int, index of the first result to return in the page.
            number_results: int, maximum number of results to return.

        Returns:
            A dict which represents an object of type Paging.
        """
        return {'startIndex': start_index, 'numberResults': number_results}

    @staticmethod
    def _get_predicate(field, operator, values=None):
        """Get an object of type Predicate.

        Args:
            field: string, the field by which to filter the returned data.
            operator: Predicate.Operator, the operator to use for filtering
                      the data returned, e.g., EQUALS, IN, CONTAINS.
            values: string[], the values by which to filter the field.

        Returns:
            A dict which represents an object of type Predicate.
        """
        return {'field': field, 'operator': operator, 'values': values}

    @staticmethod
    def _get_selector(fields, predicates=None, date_range=None,
                      ordering=None, paging=None):
        """Get an object of type Selector for services (e.g., CampaignService).

        Args:
            fields: string[], list of fields to select.
            predicates: Predicate[], filters for entity (eg. campaign, ad).
            dateRange: DateRange, range of dates for filtering the objects.
            ordering: OrderBy[], the fields to sort and the sort order.
            paging: Paging, the page of results to return.

        Returns:
            A dict which represents an object of type Selector.

        Raises:
            InvalidParameterError: An error occurred when fields are missing.
        """
        if not fields:
            raise ads_api.InvalidParameterError('fields are missing')

        # Construct selector.
        selector = {'fields': fields}
        if predicates:
            selector['predicates'] = predicates
        if date_range:
            selector['dateRange'] = date_range
        if ordering:
            selector['ordering'] = ordering
        if paging:
            selector['paging'] = paging

        return selector
