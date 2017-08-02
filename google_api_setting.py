"""
Settings for Google AdWords API.
"""

# List of selected fields of entities, e.g., Campaign, AdGroup, Keyword.
SELECTOR_FIELDS = {
    'VERSION': 'v201702',
    'BUDGET': [
        'BudgetId',
        'BudgetName',
        'Amount',
        'DeliveryMethod',
        'BudgetReferenceCount',
        'IsBudgetExplicitlyShared',
        'BudgetStatus',
    ],
    'CAMPAIGN': [
        # id.
        'Id',
        # name.
        'Name',
        # status.
        'Status',
        # servingStatus.
        'ServingStatus',
        # startDate.
        'StartDate',
        # endDate.
        'EndDate',
        # budget.
        'BudgetId',
        'BudgetName',
        'Amount',
        'DeliveryMethod',
        'BudgetReferenceCount',
        'IsBudgetExplicitlyShared',
        'BudgetStatus',
        # conversionOptimizerEligibility.
        'Eligible',
        'RejectionReasons',
        # adServingOptimizationStatus.
        'AdServingOptimizationStatus',
        # frequencyCap.
        'FrequencyCapMaxImpressions',
        'TimeUnit',
        'Level',
        # settings.
        'Settings',
        # advertisingChannelType.
        'AdvertisingChannelType',
        # advertisingChannelSubType.
        'AdvertisingChannelSubType',
        # networkSetting.
        'TargetGoogleSearch',
        'TargetSearchNetwork',
        'TargetContentNetwork',
        'TargetPartnerSearchNetwork',
        # labels.
        'Labels',
        # biddingStrategyConfiguration.
        'BiddingStrategyId',
        'BiddingStrategyName',
        'BiddingStrategyType',
        # biddingScheme.BudgetOptimizerBiddingScheme.
        'BidCeiling',
        'EnhancedCpcEnabled',
        # biddingScheme.ConversionOptimizerBiddingScheme.
        'PricingMode',
        'BidType',
        # biddingScheme.TargetCpaBiddingScheme.
        'TargetCpa',
        'TargetCpaMaxCpcBidCeiling',
        'TargetCpaMaxCpcBidFloor',
        # biddingScheme.TargetRoasBiddingScheme.
        'TargetRoas',
        'TargetRoasBidCeiling',
        'TargetRoasBidFloor',
        # biddingScheme.TargetSpendBiddingScheme.
        'TargetSpendBidCeiling',
        'TargetSpendSpendTarget',
        # campaignTrialType.
        'CampaignTrialType',
        # baseCampaignId.
        'BaseCampaignId',
        # trackingUrlTemplate.
        'TrackingUrlTemplate',
        # urlCustomParameters.
        'UrlCustomParameters',
        # vanityPharma.
        'VanityPharmaDisplayUrlMode',
        'VanityPharmaText',
    ],
    'CAMPAIGN_CRITERION': [
        # campaignId.
        'CampaignId',
        # isNegative.
        'IsNegative',
        # bidModifier.
        'BidModifier',
        # baseCampaignId.
        'BaseCampaignId',
        'Id',
        # criteriaType.
        'CriteriaType',
        # AdSchedule.
        'DayOfWeek',
        'StartHour',
        'StartMinute',
        'EndHour',
        'EndMinute',
        # AgeRange.
        'AgeRangeType',
        # Carrier.
        'CarrierName',
        'CarrierCountryCode',
        # ContentLabel.
        'ContentLabelType',
        # CriterionUserInterest.
        'UserInterestId',
        'UserInterestParentId',
        'UserInterestName',
        # CriterionUserList.
        'UserListId',
        'UserListName',
        'UserListMembershipStatus',
        'UserListEligibleForSearch',
        'UserListEligibleForDisplay',
        # Gender.
        'GenderType',
        # IpBlock.
        'IpAddress',
        # Keyword.
        'KeywordText',
        'KeywordMatchType',
        # Language.
        'LanguageCode',
        'LanguageName',
        # Location.
        'LocationName',
        'DisplayType',
        'TargetingStatus',
        'ParentLocations',
        # LocationGroups.
        'FeedId',
        'MatchingFunction',
        # MobileAppCategory.
        'MobileAppCategoryId',
        # MobileApplication.
        'AppId',
        'DisplayName',
        # MobileDevice.
        'DeviceName',
        'ManufacturerName',
        'DeviceType',
        # OperatingSystemVersion.
        'OperatingSystemName',
        'OsMajorVersion',
        'OsMinorVersion',
        'OperatorType',
        # Parent.
        'ParentType',
        # Placement.
        'PlacementUrl',
        # Platform.
        'PlatformName',
        # ProductScope.
        'Dimensions',
        # Proximity.
        'GeoPoint',
        'RadiusDistanceUnits',
        'RadiusInUnits',
        'Address',
        # Vertical.
        'VerticalId',
        'VerticalParentId',
        'Path',
        # Webpage.
        'Parameter',
        # YouTubeChannel.
        'ChannelId',
        'ChannelName',
        # YouTubeVideo.
        'VideoId',
        'VideoName',
    ],
    'ADGROUP': [
        # id.
        'Id',
        # campaignId.
        'CampaignId',
        # campaignName.
        'CampaignName',
        # name.
        'Name',
        # status.
        'Status',
        # settings.
        'Settings',
        # experimentData.
        'ExperimentId',
        'ExperimentDeltaStatus',
        'ExperimentDataStatus',
        # experimentBidMultipliers.ManualCPCAdGroupExperimentBidMultipliers.
        'MaxCpcMultiplier',
        'MaxContentCpcMultiplier',
        # experimentBidMultipliers.ManualCPMAdGroupExperimentBidMultipliers.
        'MaxCpmMultiplier',
        # labels.
        'Labels',
        # biddingStrategyConfiguration.
        'BiddingStrategyId',
        'BiddingStrategyName',
        'BiddingStrategyType',
        'BiddingStrategySource',
        # biddingScheme.BudgetOptimizerBiddingScheme.
        'EnhancedCpcEnabled',
        # biddingScheme.ConversionOptimizerBiddingScheme.
        'BidType',
        # biddingScheme.TargetCpaBiddingScheme.
        'TargetCpa',
        # bids.
        'TargetCpaBid',
        'TargetCpaBidSource',
        'CpcBid',
        'CpmBid',
        # contentBidCriterionTypeGroup.
        'ContentBidCriterionTypeGroup',
        # baseCampaignId.
        'BaseCampaignId',
        # baseAdGroupId.
        'BaseAdGroupId',
        # trackingUrlTemplate.
        'TrackingUrlTemplate',
        # urlCustomParameters.
        'UrlCustomParameters',
    ],
    'AD': [
        # adGroupId.
        'AdGroupId',
        # ad.
        'Id',
        'Url',
        'DisplayUrl',
        'CreativeFinalUrls',
        'CreativeFinalMobileUrls',
        'CreativeFinalAppUrls',
        'CreativeTrackingUrlTemplate',
        'CreativeUrlCustomParameters',
        'DevicePreference',
        'AdType',
        # ad.CallOnlyAd.
        'CallOnlyAdCountryCode',
        'CallOnlyAdPhoneNumber',
        'CallOnlyAdBusinessName',
        'CallOnlyAdDescription1',
        'CallOnlyAdDescription2',
        'CallOnlyAdCallTracked',
        'CallOnlyAdDisableCallConversion',
        'CallOnlyAdConversionTypeId',
        'CallOnlyAdPhoneNumberVerificationUrl',
        # ad.DeprecatedAd.
        'Name',
        'Type',
        # ad.ExpandedTextAd.
        'HeadlinePart1',
        'HeadlinePart2',
        'Description',
        'Path1',
        'Path2',
        # ad.ImageAd.
        'MediaId',
        'ReferenceId',
        'Dimensions',
        'Urls',
        'MimeType',
        'SourceUrl',
        'FileSize',
        'CreationTime',
        'ImageCreativeName',
        # ad.ResponsiveDisplayAd.
        'ShortHeadline',
        'LongHeadline',
        'BusinessName',
        # ad.RichMediaAd.
        'RichMediaAdName',
        'Width',
        'Height',
        'RichMediaAdSnippet',
        'RichMediaAdImpressionBeaconUrl',
        'RichMediaAdDuration',
        'RichMediaAdCertifiedVendorFormatId',
        'RichMediaAdSourceUrl',
        'RichMediaAdType',
        # ad.RichMediaAd.ThirdPartyRedirectAd.
        'IsCookieTargeted',
        'IsUserInterestTargeted',
        'IsTagged',
        'VideoTypes',
        'ExpandingDirections',
        # ad.TemplateAd.
        'TemplateId',
        'TemplateAdUnionId',
        'UniqueName',
        'TemplateElementFieldName',
        'TemplateElementFieldType',
        'TemplateElementFieldText',
        'DurationMillis',
        'StreamingUrl',
        'ReadyToPlayOnTheWeb',
        'IndustryStandardCommercialIdentifier',
        'AdvertisingId',
        'YouTubeVideoIdString',
        'TemplateAdName',
        'TemplateAdDuration',
        'TemplateOriginAdId',
        # ad.TextAd.
        'Headline',
        'Description1',
        'Description2',
        # experimentData.
        'ExperimentId',
        'ExperimentDeltaStatus',
        'ExperimentDataStatus',
        # status.
        'Status',
        # approvalStatus.
        'AdGroupCreativeApprovalStatus',
        # trademarks.
        'Trademarks',
        # disapprovalReasons.
        'AdGroupAdDisapprovalReasons',
        # trademarkDisapproved.
        'AdGroupAdTrademarkDisapproved',
        # labels.
        'Labels',
        # baseCampaignId.
        'BaseCampaignId',
        # baseAdGroupId.
        'BaseAdGroupId',
    ],
    'ADGROUP_CRITERION': [
        # adGroupId.
        'AdGroupId',
        # criterionUse.
        'CriterionUse',
        # criterion.
        'Id',
        'Status',
        'SystemServingStatus',
        'ApprovalStatus',
        'DisapprovalReasons',
        'CriteriaType',
        # criterion.AgeRange.
        'AgeRangeType',
        # criterion.AppPaymentModel.
        'AppPaymentModelType',
        # criterion.CriterionUserInterest.
        'UserInterestId',
        'UserInterestParentId',
        'UserInterestName',
        # criterion.CriterionUserList.
        'UserListId',
        'UserListName',
        'UserListMembershipStatus',
        'UserListEligibleForSearch',
        'UserListEligibleForDisplay',
        # criterion.Gender.
        'GenderType',
        # criterion.Keyword.
        'KeywordText',
        'KeywordMatchType',
        # criterion.MobileAppCategory.
        'MobileAppCategoryId',
        # criterion.MobileApplication.
        'AppId',
        'DisplayName',
        # criterion.Parent.
        'ParentType',
        # criterion.Placement.
        'PlacementUrl',
        # criterion.ProductPartition.
        'PartitionType',
        'ParentCriterionId',
        'CaseValue',
        # criterion.Vertical.
        'VerticalId',
        'VerticalParentId',
        'Path',
        # criterion.Webpage.
        'Parameter',
        'CriteriaCoverage',
        'CriteriaSamples',
        # criterion.YouTubeChannel.
        'ChannelId',
        'ChannelName',
        # criterion.YouTubeVideo.
        'VideoId',
        'VideoName',
        # labels.
        'Labels',
        # baseCampaignId.
        'BaseCampaignId',
        # baseAdGroupId.
        'BaseAdGroupId',
        # BiddableAdGroupCriterion.
        'FirstPageCpc',
        'TopOfPageCpc',
        'FirstPositionCpc',
        'QualityScore',
        'BidModifier',
    ],
    'KEYWORD_SUGGESTION': [
        'AVERAGE_CPC',
        'CATEGORY_PRODUCTS_AND_SERVICES',
        'COMPETITION',
        'EXTRACTED_FROM_WEBPAGE',
        'IDEA_TYPE',
        'KEYWORD_TEXT',
        'SEARCH_VOLUME',
        'TARGETED_MONTHLY_SEARCHES'
    ],
}


PERF_REPORT_FIELDS_OF_CAMPAIGN = [
    # 'AccountCurrencyCode',
    # 'AccountDescriptiveName',
    # 'AccountTimeZoneId',
    'ActiveViewCpm',
    'ActiveViewCtr',
    'ActiveViewImpressions',
    # 'ActiveViewMeasurability',
    # 'ActiveViewMeasurableCost',
    # 'ActiveViewMeasurableImpressions',
    # 'ActiveViewViewability',
    # 'AdNetworkType1',
    # 'AdNetworkType2',
    # 'AdvertisingChannelSubType',
    # 'AdvertisingChannelType',
    'Amount',
    'AverageCost',
    'AverageCpc',
    'AverageCpe',
    'AverageCpm',
    'AverageCpv',
    'AveragePosition',
    # 'BaseCampaignId',
    'BiddingStrategyId',
    'BiddingStrategyName',
    'BiddingStrategyType',
    'BidType',
    'BudgetId',
    'CampaignId',
    'CampaignName',
    # 'CampaignStatus',
    # 'CampaignTrialType',
    'Clicks',
    # 'ContentBudgetLostImpressionShare',
    # 'ContentImpressionShare',
    # 'ContentRankLostImpressionShare',
    'Cost',
    'Ctr',
    # 'CustomerDescriptiveName',
    'Date',
    # 'Device',
    # 'EndDate',
    # 'EngagementRate',
    # 'Engagements',
    # 'EnhancedCpcEnabled',
    # 'EnhancedCpvEnabled',
    # 'ExternalCustomerId',
    # 'GmailForwards',
    # 'GmailSaves',
    # 'GmailSecondaryClicks',
    'Impressions',
    # 'InteractionRate',
    # 'Interactions',
    # 'InteractionTypes',
    # 'InvalidClickRate',
    # 'InvalidClicks',
    # 'IsBudgetExplicitlyShared',
    # 'LabelIds',
    # 'Labels',
    # 'Month',
    # 'MonthOfYear',
    # 'Period',
    # 'PrimaryCompanyName',
    # 'Quarter',
    # 'SearchBudgetLostImpressionShare',
    # 'SearchExactMatchImpressionShare',
    # 'SearchImpressionShare',
    # 'SearchRankLostImpressionShare',
    # 'ServingStatus',
    # 'StartDate',
    # 'TrackingUrlTemplate',
    # 'UrlCustomParameters',
    'VideoQuartile100Rate',
    'VideoQuartile25Rate',
    'VideoQuartile50Rate',
    'VideoQuartile75Rate',
    'VideoViewRate',
    'VideoViews',
    # 'Week',
    # 'Year',
]


PERF_REPORT_FIELDS_OF_KEYWORD = [
    'AdGroupId',
    'AdGroupName',
    # 'AdGroupStatus',
    # 'AdNetworkType1',
    # 'AdNetworkType2',
    # 'ApprovalStatus',
    'AverageCost',
    'AverageCpc',
    'AverageCpm',
    'AverageCpv',
    # 'AveragePosition',
    # 'BiddingStrategyId',
    # 'BiddingStrategyName',
    # 'BiddingStrategySource',
    # 'BiddingStrategyType',
    # 'BidType',
    'CampaignId',
    'CampaignName',
    # 'CampaignStatus',
    'Clicks',
    # 'ClickType',
    'Cost',
    # 'CpcBid',
    # 'CpcBidSource',
    # 'CpmBid',
    # 'CreativeQualityScore',
    'Criteria',
    # 'CriteriaDestinationUrl',
    'Ctr',
    'Date',
    'DayOfWeek',
    # 'Device',
    # 'EnhancedCpcEnabled',
    # 'ExternalCustomerId',
    # 'FinalAppUrls',
    # 'FinalMobileUrls',
    # 'FinalUrls',
    # 'HasQualityScore',
    'Id',
    'Impressions',
    'IsNegative',
    'KeywordMatchType',
    # 'LabelIds',
    # 'Labels',
    'Month',
    'MonthOfYear',
    # 'QualityScore',
    'Quarter',
    # 'Slot',
    # 'Status',
    # 'SystemServingStatus',
    'Week',
    'Year',
]

PERF_REPORT_FIELDS_OF_AGE_RANGE = [
    'AdGroupId',
    'AdGroupName',
    # 'AdGroupStatus',
    # 'AdNetworkType1',
    # 'AdNetworkType2',
    'AverageCost',
    'AverageCpc',
    'AverageCpm',
    # 'BidModifier',
    # 'BidType',
    'CampaignId',
    'CampaignName',
    # 'CampaignStatus',
    'Clicks',
    # 'ClickType',
    'Cost',
    # 'CpcBid',
    # 'CpcBidSource',
    # 'CpmBid',
    # 'CpmBidSource',
    'Criteria',
    # 'CriteriaDestinationUrl',
    'Ctr',
    'Date',
    'DayOfWeek',
    # 'Device',
    # 'FinalAppUrls',
    # 'FinalMobileUrls',
    # 'FinalUrls',
    'Id',
    'Impressions',
    'IsNegative',
    # 'IsRestrict',
    'Month',
    'MonthOfYear',
    'Quarter',
    # 'Status',
    'Week',
    'Year',
]

PERF_REPORT_FIELDS_OF_GENDER = [
    'AdGroupId',
    'AdGroupName',
    # 'AdGroupStatus',
    # 'AdNetworkType1',
    # 'AdNetworkType2',
    'AverageCost',
    'AverageCpc',
    'AverageCpm',
    # 'BidModifier',
    # 'BidType',
    'CampaignId',
    'CampaignName',
    # 'CampaignStatus',
    'Clicks',
    # 'ClickType',
    'Cost',
    # 'CpcBid',
    # 'CpcBidSource',
    # 'CpmBid',
    # 'CpmBidSource',
    'Criteria',
    # 'CriteriaDestinationUrl',
    'Ctr',
    'Date',
    'DayOfWeek',
    # 'Device',
    # 'FinalAppUrls',
    # 'FinalMobileUrls',
    # 'FinalUrls',
    'Id',
    'Impressions',
    'IsNegative',
    # 'IsRestrict',
    'Month',
    'MonthOfYear',
    'Quarter',
    # 'Status',
    'Week',
    'Year',
]

PERF_REPORT_FIELDS_OF_GEO = [
    # 'AdFormat',
    'AdGroupId',
    'AdGroupName',
    # 'AdGroupStatus',
    # 'AdNetworkType1',
    # 'AdNetworkType2',
    'AverageCost',
    'AverageCpc',
    'AverageCpm',
    'CampaignId',
    'CampaignName',
    # 'CampaignStatus',
    'Clicks',
    'Cost',
    'CountryCriteriaId',
    'Ctr',
    'Date',
    'DayOfWeek',
    # 'Device',
    'Impressions',
    # 'IsTargetingLocation',
    # 'LocationType',
    'Month',
    'MonthOfYear',
    'Quarter',
    'RegionCriteriaId',
    'Week',
    'Year',
]

PERF_REPORT_FIELDS_OF_PLACEMENT = [
    # 'AdFormat',
    'AdGroupId',
    'AdGroupName',
    # 'AdGroupStatus',
    # 'AdNetworkType1',
    # 'AdNetworkType2',
    'AverageCost',
    'AverageCpc',
    'AverageCpm',
    'CampaignId',
    'CampaignName',
    # 'CampaignStatus',
    'Clicks',
    'Cost',
    'Device',
    'Ctr',
    'Date',
    'DayOfWeek',
    # 'Device',
    'Impressions',
    # 'IsTargetingLocation',
    # 'LocationType',
    'Month',
    'MonthOfYear',
    'Quarter',
    'Week',
    'Year',
]

# Refer to https://developers.google.com/adwords/api/docs/appendix/geotargeting
COUNTRIES = (
    # (Country Code, Criteria ID)
    ('AF', 2004),   # Afghanistan
    ('AL', 2008),   # Albania
    ('AQ', 2010),   # Antarctica
    ('DZ', 2012),   # Algeria
    ('AS', 2016),   # American Samoa
    ('AD', 2020),   # Andorra
    ('AO', 2024),   # Angola
    ('AG', 2028),   # Antigua and Barbuda
    ('AZ', 2031),   # Azerbaijan
    ('AR', 2032),   # Argentina
    ('AU', 2036),   # Australia
    ('AT', 2040),   # Austria
    ('BS', 2044),   # The Bahamas
    ('BH', 2048),   # Bahrain
    ('BD', 2050),   # Bangladesh
    ('AM', 2051),   # Armenia
    ('BB', 2052),   # Barbados
    ('BE', 2056),   # Belgium
    ('BT', 2064),   # Bhutan
    ('BO', 2068),   # Bolivia
    ('BA', 2070),   # Bosnia and Herzegovina
    ('BW', 2072),   # Botswana
    ('BR', 2076),   # Brazil
    ('BZ', 2084),   # Belize
    ('SB', 2090),   # Solomon Islands
    ('BN', 2096),   # Brunei
    ('BG', 2100),   # Bulgaria
    ('MM', 2104),   # Myanmar (Burma)
    ('BI', 2108),   # Burundi
    ('BY', 2112),   # Belarus
    ('KH', 2116),   # Cambodia
    ('CM', 2120),   # Cameroon
    ('CA', 2124),   # Canada
    ('CV', 2132),   # Cape Verde
    ('CF', 2140),   # Central African Republic
    ('LK', 2144),   # Sri Lanka
    ('TD', 2148),   # Chad
    ('CL', 2152),   # Chile
    ('CN', 2156),   # China
    ('CX', 2162),   # Christmas Island
    ('CC', 2166),   # Cocos (Keeling) Islands
    ('CO', 2170),   # Colombia
    ('KM', 2174),   # Comoros
    ('CG', 2178),   # Republic of the Congo
    ('CD', 2180),   # Democratic Republic of the Congo
    ('CK', 2184),   # Cook Islands
    ('CR', 2188),   # Costa Rica
    ('HR', 2191),   # Croatia
    ('CY', 2196),   # Cyprus
    ('CZ', 2203),   # Czech Republic
    ('BJ', 2204),   # Benin
    ('DK', 2208),   # Denmark
    ('DM', 2212),   # Dominica
    ('DO', 2214),   # Dominican Republic
    ('EC', 2218),   # Ecuador
    ('SV', 2222),   # El Salvador
    ('GQ', 2226),   # Equatorial Guinea
    ('ET', 2231),   # Ethiopia
    ('ER', 2232),   # Eritrea
    ('EE', 2233),   # Estonia
    ('GS', 2239),   # South Georgia and the South Sandwich Islands
    ('FJ', 2242),   # Fiji
    ('FI', 2246),   # Finland
    ('FR', 2250),   # France
    ('PF', 2258),   # French Polynesia
    ('TF', 2260),   # French Southern and Antarctic Lands
    ('DJ', 2262),   # Djibouti
    ('GA', 2266),   # Gabon
    ('GE', 2268),   # Georgia
    ('GM', 2270),   # The Gambia
    ('DE', 2276),   # Germany
    ('GH', 2288),   # Ghana
    ('KI', 2296),   # Kiribati
    ('GR', 2300),   # Greece
    ('GD', 2308),   # Grenada
    ('GU', 2316),   # Guam
    ('GT', 2320),   # Guatemala
    ('GN', 2324),   # Guinea
    ('GY', 2328),   # Guyana
    ('HT', 2332),   # Haiti
    ('HM', 2334),   # Heard Island and McDonald Islands
    ('VA', 2336),   # Vatican City
    ('HN', 2340),   # Honduras
    ('HU', 2348),   # Hungary
    ('IS', 2352),   # Iceland
    ('IN', 2356),   # India
    ('ID', 2360),   # Indonesia
    ('IQ', 2368),   # Iraq
    ('IE', 2372),   # Ireland
    ('IL', 2376),   # Israel
    ('IT', 2380),   # Italy
    ('CI', 2384),   # Cote d'Ivoire
    ('JM', 2388),   # Jamaica
    ('JP', 2392),   # Japan
    ('KZ', 2398),   # Kazakhstan
    ('JO', 2400),   # Jordan
    ('KE', 2404),   # Kenya
    ('KR', 2410),   # South Korea
    ('KW', 2414),   # Kuwait
    ('KG', 2417),   # Kyrgyzstan
    ('LA', 2418),   # Laos
    ('LB', 2422),   # Lebanon
    ('LS', 2426),   # Lesotho
    ('LV', 2428),   # Latvia
    ('LR', 2430),   # Liberia
    ('LY', 2434),   # Libya
    ('LI', 2438),   # Liechtenstein
    ('LT', 2440),   # Lithuania
    ('LU', 2442),   # Luxembourg
    ('MG', 2450),   # Madagascar
    ('MW', 2454),   # Malawi
    ('MY', 2458),   # Malaysia
    ('MV', 2462),   # Maldives
    ('ML', 2466),   # Mali
    ('MT', 2470),   # Malta
    ('MR', 2478),   # Mauritania
    ('MU', 2480),   # Mauritius
    ('MX', 2484),   # Mexico
    ('MC', 2492),   # Monaco
    ('MN', 2496),   # Mongolia
    ('MD', 2498),   # Moldova
    ('ME', 2499),   # Montenegro
    ('MA', 2504),   # Morocco
    ('MZ', 2508),   # Mozambique
    ('OM', 2512),   # Oman
    ('NA', 2516),   # Namibia
    ('NR', 2520),   # Nauru
    ('NP', 2524),   # Nepal
    ('NL', 2528),   # Netherlands
    ('NC', 2540),   # New Caledonia
    ('VU', 2548),   # Vanuatu
    ('NZ', 2554),   # New Zealand
    ('NI', 2558),   # Nicaragua
    ('NE', 2562),   # Niger
    ('NG', 2566),   # Nigeria
    ('NU', 2570),   # Niue
    ('NF', 2574),   # Norfolk Island
    ('NO', 2578),   # Norway
    ('MP', 2580),   # Northern Mariana Islands
    ('UM', 2581),   # United States Minor Outlying Islands
    ('FM', 2583),   # Federated States of Micronesia
    ('MH', 2584),   # Marshall Islands
    ('PW', 2585),   # Palau
    ('PK', 2586),   # Pakistan
    ('PA', 2591),   # Panama
    ('PG', 2598),   # Papua New Guinea
    ('PY', 2600),   # Paraguay
    ('PE', 2604),   # Peru
    ('PH', 2608),   # Philippines
    ('PN', 2612),   # Pitcairn Islands
    ('PL', 2616),   # Poland
    ('PT', 2620),   # Portugal
    ('GW', 2624),   # Guinea-Bissau
    ('TL', 2626),   # Timor-Leste
    ('QA', 2634),   # Qatar
    ('RO', 2642),   # Romania
    ('RU', 2643),   # Russia
    ('RW', 2646),   # Rwanda
    ('SH', 2654),   # Saint Helena
    ('KN', 2659),   # Saint Kitts and Nevis
    ('LC', 2662),   # Saint Lucia
    ('PM', 2666),   # Saint Pierre and Miquelon
    ('VC', 2670),   # Saint Vincent and the Grenadines
    ('SM', 2674),   # San Marino
    ('ST', 2678),   # Sao Tome and Principe
    ('SA', 2682),   # Saudi Arabia
    ('SN', 2686),   # Senegal
    ('RS', 2688),   # Serbia
    ('SC', 2690),   # Seychelles
    ('SL', 2694),   # Sierra Leone
    ('SG', 2702),   # Singapore
    ('SK', 2703),   # Slovakia
    ('VN', 2704),   # Vietnam
    ('SI', 2705),   # Slovenia
    ('SO', 2706),   # Somalia
    ('ZA', 2710),   # South Africa
    ('ZW', 2716),   # Zimbabwe
    ('ES', 2724),   # Spain
    ('SR', 2740),   # Suriname
    ('SZ', 2748),   # Swaziland
    ('SE', 2752),   # Sweden
    ('CH', 2756),   # Switzerland
    ('TJ', 2762),   # Tajikistan
    ('TH', 2764),   # Thailand
    ('TG', 2768),   # Togo
    ('TK', 2772),   # Tokelau
    ('TO', 2776),   # Tonga
    ('TT', 2780),   # Trinidad and Tobago
    ('AE', 2784),   # United Arab Emirates
    ('TN', 2788),   # Tunisia
    ('TR', 2792),   # Turkey
    ('TM', 2795),   # Turkmenistan
    ('TV', 2798),   # Tuvalu
    ('UG', 2800),   # Uganda
    ('UA', 2804),   # Ukraine
    ('MK', 2807),   # Macedonia (FYROM)
    ('EG', 2818),   # Egypt
    ('GB', 2826),   # United Kingdom
    ('TZ', 2834),   # Tanzania
    ('TW', 2158),   # Taiwan
    ('US', 2840),   # United States
    ('BF', 2854),   # Burkina Faso
    ('UY', 2858),   # Uruguay
    ('UZ', 2860),   # Uzbekistan
    ('VE', 2862),   # Venezuela
    ('WF', 2876),   # Wallis and Futuna
    ('WS', 2882),   # Samoa
    ('YE', 2887),   # Yemen
    ('ZM', 2894),   # Zambia
    ('HK', 2344),   # Hong Kong
    ('MO', 2446),   # Macau
)


# Refer to
# https://developers.google.com/adwords/api/docs/appendix/languagecodes
LANGUAGES = (
    # (Language Code, Criteria ID)
    ('ar', 1019),      # Arabic
    ('bg', 1020),      # Bulgarian
    ('ca', 1038),      # Catalan
    ('zh_CN', 1017),   # Chinese (simplified)
    ('zh', 1018),      # Chinese (traditional)
    ('hr', 1039),      # Croatian
    ('cs', 1021),      # Czech
    ('da', 1009),      # Danish
    ('nl', 1010),      # Dutch
    ('en', 1000),      # English
    ('et', 1043),      # Estonian
    ('tl', 1042),      # Filipino
    ('fi', 1011),      # Finnish
    ('fr', 1002),      # French
    ('de', 1001),      # German
    ('el', 1022),      # Greek
    ('iw', 1027),      # Hebrew
    ('hi', 1023),      # Hindi
    ('hu', 1024),      # Hungarian
    ('is', 1026),      # Icelandic
    ('id', 1025),      # Indonesian
    ('it', 1004),      # Italian
    ('ja', 1005),      # Japanese
    ('ko', 1012),      # Korean
    ('lv', 1028),      # Latvian
    ('lt', 1029),      # Lithuanian
    ('ms', 1102),      # Malay
    ('no', 1013),      # Norwegian
    ('fa', 1064),      # Persian
    ('pl', 1030),      # Polish
    ('pt', 1014),      # Portuguese
    ('ro', 1032),      # Romanian
    ('ru', 1031),      # Russian
    ('sr', 1035),      # Serbian
    ('sk', 1033),      # Slovak
    ('sl', 1034),      # Slovenian
    ('es', 1003),      # Spanish
    ('sv', 1015),      # Swedish
    ('th', 1044),      # Thai
    ('tr', 1037),      # Turkish
    ('uk', 1036),      # Ukrainian
    ('ur', 1041),      # Urdu
    ('vi', 1040),      # Vietnamese
)
