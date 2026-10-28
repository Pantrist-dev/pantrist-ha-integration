"""Contains all the data models used in inputs/outputs"""

from .access_token_controller_authorize_code_challenge_method import AccessTokenControllerAuthorizeCodeChallengeMethod
from .access_token_controller_authorize_response_200 import AccessTokenControllerAuthorizeResponse200
from .access_token_response_dto import AccessTokenResponseDto
from .add_by_barcode_dto import AddByBarcodeDto
from .add_by_name_dto import AddByNameDto
from .add_pantry_by_barcode_dto import AddPantryByBarcodeDto
from .add_pantry_by_name_dto import AddPantryByNameDto
from .add_recipe_collection import AddRecipeCollection
from .add_user_to_list_dto import AddUserToListDto
from .affiliate_product_dto import AffiliateProductDto
from .ai_quota_dto import AiQuotaDto
from .ai_role import AiRole
from .aisle_order_dto import AisleOrderDto
from .aisle_order_dto_confidence import AisleOrderDtoConfidence
from .aisle_order_markets_dto import AisleOrderMarketsDto
from .aisle_orders_dto import AisleOrdersDto
from .aisle_rank_dto import AisleRankDto
from .allergen import Allergen
from .analysis_emergency_supply_settings_dto import AnalysisEmergencySupplySettingsDto
from .analysis_emergency_supply_settings_dto_mappings import AnalysisEmergencySupplySettingsDtoMappings
from .analysis_emergency_supply_settings_dto_standard import AnalysisEmergencySupplySettingsDtoStandard
from .analysis_pantry_settings_dto import AnalysisPantrySettingsDto
from .analysis_settings_dto import AnalysisSettingsDto
from .analysis_shopping_settings_dto import AnalysisShoppingSettingsDto
from .api_filter_dto import ApiFilterDto
from .api_filter_dto_categories_item import ApiFilterDtoCategoriesItem
from .api_filter_dto_dietary_styles_item import ApiFilterDtoDietaryStylesItem
from .api_filter_dto_exclude_allergens_item import ApiFilterDtoExcludeAllergensItem
from .api_filter_dto_language import ApiFilterDtoLanguage
from .api_filter_dto_pantry_filter import ApiFilterDtoPantryFilter
from .api_filter_dto_sort_by import ApiFilterDtoSortBy
from .app_version_controller_get_policy_platform import AppVersionControllerGetPolicyPlatform
from .app_version_policy_dto import AppVersionPolicyDto
from .app_version_policy_dto_platform import AppVersionPolicyDtoPlatform
from .article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
from .article_catalog_dto import ArticleCatalogDto
from .article_catalog_dto_price_per_market_type_0 import ArticleCatalogDtoPricePerMarketType0
from .article_catalog_overlay_dto import ArticleCatalogOverlayDto
from .article_catalog_overlay_row_dto import ArticleCatalogOverlayRowDto
from .article_catalog_overlay_row_dto_price_per_market_type_0 import ArticleCatalogOverlayRowDtoPricePerMarketType0
from .article_dto import ArticleDto
from .article_dto_price_per_market_type_0 import ArticleDtoPricePerMarketType0
from .article_nutriments_dto import ArticleNutrimentsDto
from .article_product_group import ArticleProductGroup
from .auth_controller_login_with_provider_provider import AuthControllerLoginWithProviderProvider
from .auth_controller_unlink_provider_provider import AuthControllerUnlinkProviderProvider
from .auth_methods_dto import AuthMethodsDto
from .auth_methods_dto_providers_item import AuthMethodsDtoProvidersItem
from .auth_rollout_dto import AuthRolloutDto
from .auth_rollout_dto_mode import AuthRolloutDtoMode
from .auth_session_info_dto import AuthSessionInfoDto
from .auth_session_response_dto import AuthSessionResponseDto
from .auto_reduce_config_dto import AutoReduceConfigDto
from .auto_reduce_cursor_dto import AutoReduceCursorDto
from .auto_reduce_interval_dto import AutoReduceIntervalDto
from .auto_reduce_interval_dto_mode import AutoReduceIntervalDtoMode
from .auto_reduce_interval_dto_unit import AutoReduceIntervalDtoUnit
from .auto_reduce_weekday_dto import AutoReduceWeekdayDto
from .auto_reduce_weekday_dto_mode import AutoReduceWeekdayDtoMode
from .barcode_affiliate_product_dto import BarcodeAffiliateProductDto
from .barcode_dto import BarcodeDto
from .barcode_dto_language_specific import BarcodeDtoLanguageSpecific
from .barcode_page_dto import BarcodePageDto
from .barcode_page_dto_name_by_language import BarcodePageDtoNameByLanguage
from .barcode_summary_dto import BarcodeSummaryDto
from .block_settings_dto import BlockSettingsDto
from .buy_reminder_last_purchase_dto import BuyReminderLastPurchaseDto
from .buy_reminder_row_dto import BuyReminderRowDto
from .buy_reminder_row_dto_confidence import BuyReminderRowDtoConfidence
from .catalog_mapping_entry_dto import CatalogMappingEntryDto
from .category_dto import CategoryDto
from .category_dto_name_type_1 import CategoryDtoNameType1
from .category_item_type import CategoryItemType
from .change_amount_of_item_dto import ChangeAmountOfItemDto
from .change_amount_of_item_dto_source import ChangeAmountOfItemDtoSource
from .change_email_dto import ChangeEmailDto
from .change_password_dto import ChangePasswordDto
from .client_log_batch_dto import ClientLogBatchDto
from .client_log_entry_dto import ClientLogEntryDto
from .client_log_entry_dto_data import ClientLogEntryDtoData
from .client_log_entry_dto_level import ClientLogEntryDtoLevel
from .client_log_ingest_result_dto import ClientLogIngestResultDto
from .collection_with_recipe_flag import CollectionWithRecipeFlag
from .create_barcode_dto import CreateBarcodeDto
from .create_barcode_dto_language_specific import CreateBarcodeDtoLanguageSpecific
from .create_billing_session_dto import CreateBillingSessionDto
from .create_invitation_dto import CreateInvitationDto
from .create_invite_dto import CreateInviteDto
from .create_list_dto import CreateListDto
from .create_list_permission_dto import CreateListPermissionDto
from .create_nfc_tag_dto import CreateNfcTagDto
from .create_subscription_dto import CreateSubscriptionDto
from .create_user_dto import CreateUserDto
from .current_work_dto import CurrentWorkDto
from .dietary_preferences_dto import DietaryPreferencesDto
from .dietary_preferences_dto_allergens_item import DietaryPreferencesDtoAllergensItem
from .dietary_preferences_dto_dietary_styles_item import DietaryPreferencesDtoDietaryStylesItem
from .discount_type import DiscountType
from .firebase_exchange_dto import FirebaseExchangeDto
from .forgot_password_dto import ForgotPasswordDto
from .general_nutriments_dto import GeneralNutrimentsDto
from .get_recipe_collections_with_images_dto import GetRecipeCollectionsWithImagesDto
from .help_article_dto import HelpArticleDto
from .history_event_type import HistoryEventType
from .history_item_type import HistoryItemType
from .household_details_dto import HouseholdDetailsDto
from .ingredient_dto import IngredientDto
from .ingredient_dto_volume_unit import IngredientDtoVolumeUnit
from .invited_user_dto import InvitedUserDto
from .item_dto import ItemDto
from .item_list_dto import ItemListDto
from .item_pantry_settings_dto import ItemPantrySettingsDto
from .linked_store_dto import LinkedStoreDto
from .list_catalog_mapping_controller_replace_mapping_body import ListCatalogMappingControllerReplaceMappingBody
from .list_catalog_mapping_controller_replace_mapping_response_200 import (
    ListCatalogMappingControllerReplaceMappingResponse200,
)
from .list_dto import ListDto
from .list_invite_dto import ListInviteDto
from .list_item_history_dto import ListItemHistoryDto
from .list_item_history_page_dto import ListItemHistoryPageDto
from .list_purchases_controller_get_purchases_response_200 import ListPurchasesControllerGetPurchasesResponse200
from .list_user_dto import ListUserDto
from .list_week_plan_controller_remove_entry_type import ListWeekPlanControllerRemoveEntryType
from .localization_dto import LocalizationDto
from .location_type import LocationType
from .login_dto import LoginDto
from .logout_dto import LogoutDto
from .loyalty_card_dto import LoyaltyCardDto
from .loyalty_card_format import LoyaltyCardFormat
from .market_arrival_device_dto import MarketArrivalDeviceDto
from .market_arrival_payload_dto import MarketArrivalPayloadDto
from .market_arrival_transition_dto import MarketArrivalTransitionDto
from .market_arrival_transition_dto_transition import MarketArrivalTransitionDtoTransition
from .merged_category_dto import MergedCategoryDto
from .merged_category_dto_list_category_ids import MergedCategoryDtoListCategoryIds
from .merged_category_dto_name_type_1 import MergedCategoryDtoNameType1
from .merged_pantry_dto import MergedPantryDto
from .merged_pantry_dto_list_pantry_ids import MergedPantryDtoListPantryIds
from .merged_pantry_dto_name_type_1 import MergedPantryDtoNameType1
from .merged_supermarket_dto import MergedSupermarketDto
from .merged_supermarket_dto_list_supermarket_ids import MergedSupermarketDtoListSupermarketIds
from .merged_unit_dto import MergedUnitDto
from .merged_unit_dto_list_unit_ids import MergedUnitDtoListUnitIds
from .message_dto import MessageDto
from .metric_equivalent_dto import MetricEquivalentDto
from .metric_equivalent_dto_unit import MetricEquivalentDtoUnit
from .minimum_amount_mode import MinimumAmountMode
from .next_feature_with_votes_dto import NextFeatureWithVotesDto
from .nfc_tag_dto import NfcTagDto
from .notification_payload_dto import NotificationPayloadDto
from .notification_settings_dto import NotificationSettingsDto
from .nutri_score import NutriScore
from .offer_dto import OfferDto
from .offer_dto_kind import OfferDtoKind
from .offer_ingredient_match_dto import OfferIngredientMatchDto
from .offer_ingredient_match_dto_allergens_item import OfferIngredientMatchDtoAllergensItem
from .offer_ingredient_match_dto_diet import OfferIngredientMatchDtoDiet
from .offer_ingredient_match_dto_match_method import OfferIngredientMatchDtoMatchMethod
from .offer_recipe_idea_dto import OfferRecipeIdeaDto
from .offer_recipe_ideas_controller_find_categories_item import OfferRecipeIdeasControllerFindCategoriesItem
from .offer_recipe_ideas_controller_find_dietary_styles_item import OfferRecipeIdeasControllerFindDietaryStylesItem
from .offer_recipe_ideas_controller_find_exclude_allergens_item import (
    OfferRecipeIdeasControllerFindExcludeAllergensItem,
)
from .offer_recipe_ideas_response_dto import OfferRecipeIdeasResponseDto
from .offer_recipe_ingredient_dto import OfferRecipeIngredientDto
from .offer_search_result_dto import OfferSearchResultDto
from .optional_range_dto import OptionalRangeDto
from .pagination_response_dto import PaginationResponseDto
from .pantry_list_items_controller_get_sorted_items_order import PantryListItemsControllerGetSortedItemsOrder
from .pantry_list_items_controller_get_sorted_items_sort_by import PantryListItemsControllerGetSortedItemsSortBy
from .pantry_location_dto import PantryLocationDto
from .pantry_location_dto_name_type_1 import PantryLocationDtoNameType1
from .pantry_offer_match_dto import PantryOfferMatchDto
from .pantry_settings_dto import PantrySettingsDto
from .parse_nutriments_ingredient_dto import ParseNutrimentsIngredientDto
from .parse_nutriments_request_dto import ParseNutrimentsRequestDto
from .parse_nutriments_result_dto import ParseNutrimentsResultDto
from .parse_recipe_additional_attachment import ParseRecipeAdditionalAttachment
from .parse_recipe_collection_attachment_dto import ParseRecipeCollectionAttachmentDto
from .parse_recipe_collection_request_dto import ParseRecipeCollectionRequestDto
from .parse_recipe_from_attachment import ParseRecipeFromAttachment
from .parse_recipe_request_dto import ParseRecipeRequestDto
from .parse_recipe_request_dto_type import ParseRecipeRequestDtoType
from .parse_recipe_text_request_dto import ParseRecipeTextRequestDto
from .partial_step_dto import PartialStepDto
from .premium_invitation_base_data_dto import PremiumInvitationBaseDataDto
from .premium_invitation_data_dto import PremiumInvitationDataDto
from .premium_invitation_dto import PremiumInvitationDto
from .price_trend_content_change_dto import PriceTrendContentChangeDto
from .price_trend_detail_dto import PriceTrendDetailDto
from .price_trend_item_dto import PriceTrendItemDto
from .price_trend_point_dto import PriceTrendPointDto
from .price_trends_page_dto import PriceTrendsPageDto
from .price_type import PriceType
from .price_with_date_dto import PriceWithDateDto
from .process_stripe_session_dto import ProcessStripeSessionDto
from .provider_login_dto import ProviderLoginDto
from .provider_profile_dto import ProviderProfileDto
from .public_user_dto import PublicUserDto
from .public_user_dto_forced_premium_tariff import PublicUserDtoForcedPremiumTariff
from .purchase_page_dto import PurchasePageDto
from .purchased_item_dto import PurchasedItemDto
from .purchased_item_dto_discount_type import PurchasedItemDtoDiscountType
from .purchased_item_dto_price_type import PurchasedItemDtoPriceType
from .receipt_category import ReceiptCategory
from .recipe_api import RecipeApi
from .recipe_collection_controller_get_collections_type import RecipeCollectionControllerGetCollectionsType
from .recipe_collection_dto import RecipeCollectionDto
from .recipe_deck_request_dto import RecipeDeckRequestDto
from .recipe_deck_request_dto_categories_item import RecipeDeckRequestDtoCategoriesItem
from .recipe_deck_request_dto_dietary_styles_item import RecipeDeckRequestDtoDietaryStylesItem
from .recipe_deck_request_dto_exclude_allergens_item import RecipeDeckRequestDtoExcludeAllergensItem
from .recipe_deck_request_dto_language import RecipeDeckRequestDtoLanguage
from .recipe_deck_request_dto_pantry_filter import RecipeDeckRequestDtoPantryFilter
from .recipe_deck_request_dto_sort_by import RecipeDeckRequestDtoSortBy
from .recipe_dto import RecipeDto
from .recipe_dto_language import RecipeDtoLanguage
from .recipe_match_state_dto import RecipeMatchStateDto
from .recipe_match_state_dto_ingredient_densities import RecipeMatchStateDtoIngredientDensities
from .recipe_match_state_request_dto import RecipeMatchStateRequestDto
from .recipe_matched_ingredient_dto import RecipeMatchedIngredientDto
from .recipe_origin import RecipeOrigin
from .recipe_parser_controller_parse_file_recipe_body import RecipeParserControllerParseFileRecipeBody
from .recipe_parser_controller_parse_recipe_collection_from_file_body import (
    RecipeParserControllerParseRecipeCollectionFromFileBody,
)
from .recipe_parsing_collection_result_dto import RecipeParsingCollectionResultDto
from .recipe_parsing_result_dto import RecipeParsingResultDto
from .recipe_parsing_result_dto_language import RecipeParsingResultDtoLanguage
from .recipe_plan_stats_dto import RecipePlanStatsDto
from .recipe_source_dto import RecipeSourceDto
from .recipe_substitutable_ingredient_dto import RecipeSubstitutableIngredientDto
from .recipe_substitutable_ingredient_dto_confidence import RecipeSubstitutableIngredientDtoConfidence
from .recipe_substitutable_ingredient_dto_kind import RecipeSubstitutableIngredientDtoKind
from .refresh_token_dto import RefreshTokenDto
from .register_dto import RegisterDto
from .register_market_arrival_device_dto import RegisterMarketArrivalDeviceDto
from .report_substitution_dto import ReportSubstitutionDto
from .report_substitution_result_dto import ReportSubstitutionResultDto
from .report_substitution_result_dto_status import ReportSubstitutionResultDtoStatus
from .reset_password_dto import ResetPasswordDto
from .role import Role
from .s3_controller_delete_file_owner_type import S3ControllerDeleteFileOwnerType
from .saved_for_recipe_dto import SavedForRecipeDto
from .search_for_barcode_dto import SearchForBarcodeDto
from .send_notification_dto import SendNotificationDto
from .send_notification_dto_data import SendNotificationDtoData
from .set_user_stores_dto import SetUserStoresDto
from .shopping_cart_item_dto import ShoppingCartItemDto
from .shopping_cart_items_controller_get_count_response_200 import ShoppingCartItemsControllerGetCountResponse200
from .shopping_list_items_controller_get_sorted_items_order import ShoppingListItemsControllerGetSortedItemsOrder
from .shopping_list_settings_dto import ShoppingListSettingsDto
from .smart_suggestions_settings_dto import SmartSuggestionsSettingsDto
from .social_platform import SocialPlatform
from .step_dto import StepDto
from .storage_location_dto import StorageLocationDto
from .store_dto import StoreDto
from .store_dto_no_offers_reason import StoreDtoNoOffersReason
from .store_dto_opening_hours import StoreDtoOpeningHours
from .store_offers_dto import StoreOffersDto
from .store_offers_dto_no_offers_reason import StoreOffersDtoNoOffersReason
from .subscription_validation_response_dto import SubscriptionValidationResponseDto
from .substitution_suggestion_dto import SubstitutionSuggestionDto
from .substitution_suggestion_dto_confidence import SubstitutionSuggestionDtoConfidence
from .substitution_suggestion_dto_kind import SubstitutionSuggestionDtoKind
from .success_dto import SuccessDto
from .supermarket_dto import SupermarketDto
from .swipe_decision_dto import SwipeDecisionDto
from .swipe_decision_dto_decision import SwipeDecisionDtoDecision
from .swipe_week_plan_target_dto import SwipeWeekPlanTargetDto
from .sync_firebase_invitation_dto import SyncFirebaseInvitationDto
from .unit_dto import UnitDto
from .update_collection_assignment_dto import UpdateCollectionAssignmentDto
from .update_item_dto import UpdateItemDto
from .update_list_dto import UpdateListDto
from .update_nfc_tag_dto import UpdateNfcTagDto
from .update_user_dto import UpdateUserDto
from .upsert_loyalty_card_dto import UpsertLoyaltyCardDto
from .user_dto import UserDto
from .user_dto_forced_premium_tariff import UserDtoForcedPremiumTariff
from .user_dto_user_country_source import UserDtoUserCountrySource
from .user_permissions_dto import UserPermissionsDto
from .user_subscription_dto import UserSubscriptionDto
from .user_subscription_dto_status import UserSubscriptionDtoStatus
from .user_subscription_dto_store import UserSubscriptionDtoStore
from .value_with_metric_and_opening_dto import ValueWithMetricAndOpeningDto
from .value_with_metric_and_opening_dto_metric import ValueWithMetricAndOpeningDtoMetric
from .value_with_metric_dto import ValueWithMetricDto
from .value_with_metric_dto_metric import ValueWithMetricDtoMetric
from .verify_email_dto import VerifyEmailDto
from .verify_email_response_dto import VerifyEmailResponseDto
from .volume_unit import VolumeUnit
from .vote_dto import VoteDto
from .week_plan_day_dto import WeekPlanDayDto
from .week_plan_receipt_dto import WeekPlanReceiptDto
from .week_plan_receipt_dto_type import WeekPlanReceiptDtoType
from .weighing_dto import WeighingDto
from .weighing_unit import WeighingUnit
from .ws_data_collection import WsDataCollection
from .ws_event_collection_dto import WsEventCollectionDto

__all__ = (
    "AccessTokenControllerAuthorizeCodeChallengeMethod",
    "AccessTokenControllerAuthorizeResponse200",
    "AccessTokenResponseDto",
    "AddByBarcodeDto",
    "AddByNameDto",
    "AddPantryByBarcodeDto",
    "AddPantryByNameDto",
    "AddRecipeCollection",
    "AddUserToListDto",
    "AffiliateProductDto",
    "AiQuotaDto",
    "AiRole",
    "AisleOrderDto",
    "AisleOrderDtoConfidence",
    "AisleOrderMarketsDto",
    "AisleOrdersDto",
    "AisleRankDto",
    "Allergen",
    "AnalysisEmergencySupplySettingsDto",
    "AnalysisEmergencySupplySettingsDtoMappings",
    "AnalysisEmergencySupplySettingsDtoStandard",
    "AnalysisPantrySettingsDto",
    "AnalysisSettingsDto",
    "AnalysisShoppingSettingsDto",
    "ApiFilterDto",
    "ApiFilterDtoCategoriesItem",
    "ApiFilterDtoDietaryStylesItem",
    "ApiFilterDtoExcludeAllergensItem",
    "ApiFilterDtoLanguage",
    "ApiFilterDtoPantryFilter",
    "ApiFilterDtoSortBy",
    "AppVersionControllerGetPolicyPlatform",
    "AppVersionPolicyDto",
    "AppVersionPolicyDtoPlatform",
    "ArticleCatalogBestBeforeDatesDto",
    "ArticleCatalogDto",
    "ArticleCatalogDtoPricePerMarketType0",
    "ArticleCatalogOverlayDto",
    "ArticleCatalogOverlayRowDto",
    "ArticleCatalogOverlayRowDtoPricePerMarketType0",
    "ArticleDto",
    "ArticleDtoPricePerMarketType0",
    "ArticleNutrimentsDto",
    "ArticleProductGroup",
    "AuthControllerLoginWithProviderProvider",
    "AuthControllerUnlinkProviderProvider",
    "AuthMethodsDto",
    "AuthMethodsDtoProvidersItem",
    "AuthRolloutDto",
    "AuthRolloutDtoMode",
    "AuthSessionInfoDto",
    "AuthSessionResponseDto",
    "AutoReduceConfigDto",
    "AutoReduceCursorDto",
    "AutoReduceIntervalDto",
    "AutoReduceIntervalDtoMode",
    "AutoReduceIntervalDtoUnit",
    "AutoReduceWeekdayDto",
    "AutoReduceWeekdayDtoMode",
    "BarcodeAffiliateProductDto",
    "BarcodeDto",
    "BarcodeDtoLanguageSpecific",
    "BarcodePageDto",
    "BarcodePageDtoNameByLanguage",
    "BarcodeSummaryDto",
    "BlockSettingsDto",
    "BuyReminderLastPurchaseDto",
    "BuyReminderRowDto",
    "BuyReminderRowDtoConfidence",
    "CatalogMappingEntryDto",
    "CategoryDto",
    "CategoryDtoNameType1",
    "CategoryItemType",
    "ChangeAmountOfItemDto",
    "ChangeAmountOfItemDtoSource",
    "ChangeEmailDto",
    "ChangePasswordDto",
    "ClientLogBatchDto",
    "ClientLogEntryDto",
    "ClientLogEntryDtoData",
    "ClientLogEntryDtoLevel",
    "ClientLogIngestResultDto",
    "CollectionWithRecipeFlag",
    "CreateBarcodeDto",
    "CreateBarcodeDtoLanguageSpecific",
    "CreateBillingSessionDto",
    "CreateInvitationDto",
    "CreateInviteDto",
    "CreateListDto",
    "CreateListPermissionDto",
    "CreateNfcTagDto",
    "CreateSubscriptionDto",
    "CreateUserDto",
    "CurrentWorkDto",
    "DietaryPreferencesDto",
    "DietaryPreferencesDtoAllergensItem",
    "DietaryPreferencesDtoDietaryStylesItem",
    "DiscountType",
    "FirebaseExchangeDto",
    "ForgotPasswordDto",
    "GeneralNutrimentsDto",
    "GetRecipeCollectionsWithImagesDto",
    "HelpArticleDto",
    "HistoryEventType",
    "HistoryItemType",
    "HouseholdDetailsDto",
    "IngredientDto",
    "IngredientDtoVolumeUnit",
    "InvitedUserDto",
    "ItemDto",
    "ItemListDto",
    "ItemPantrySettingsDto",
    "LinkedStoreDto",
    "ListCatalogMappingControllerReplaceMappingBody",
    "ListCatalogMappingControllerReplaceMappingResponse200",
    "ListDto",
    "ListInviteDto",
    "ListItemHistoryDto",
    "ListItemHistoryPageDto",
    "ListPurchasesControllerGetPurchasesResponse200",
    "ListUserDto",
    "ListWeekPlanControllerRemoveEntryType",
    "LocalizationDto",
    "LocationType",
    "LoginDto",
    "LogoutDto",
    "LoyaltyCardDto",
    "LoyaltyCardFormat",
    "MarketArrivalDeviceDto",
    "MarketArrivalPayloadDto",
    "MarketArrivalTransitionDto",
    "MarketArrivalTransitionDtoTransition",
    "MergedCategoryDto",
    "MergedCategoryDtoListCategoryIds",
    "MergedCategoryDtoNameType1",
    "MergedPantryDto",
    "MergedPantryDtoListPantryIds",
    "MergedPantryDtoNameType1",
    "MergedSupermarketDto",
    "MergedSupermarketDtoListSupermarketIds",
    "MergedUnitDto",
    "MergedUnitDtoListUnitIds",
    "MessageDto",
    "MetricEquivalentDto",
    "MetricEquivalentDtoUnit",
    "MinimumAmountMode",
    "NextFeatureWithVotesDto",
    "NfcTagDto",
    "NotificationPayloadDto",
    "NotificationSettingsDto",
    "NutriScore",
    "OfferDto",
    "OfferDtoKind",
    "OfferIngredientMatchDto",
    "OfferIngredientMatchDtoAllergensItem",
    "OfferIngredientMatchDtoDiet",
    "OfferIngredientMatchDtoMatchMethod",
    "OfferRecipeIdeaDto",
    "OfferRecipeIdeasControllerFindCategoriesItem",
    "OfferRecipeIdeasControllerFindDietaryStylesItem",
    "OfferRecipeIdeasControllerFindExcludeAllergensItem",
    "OfferRecipeIdeasResponseDto",
    "OfferRecipeIngredientDto",
    "OfferSearchResultDto",
    "OptionalRangeDto",
    "PaginationResponseDto",
    "PantryListItemsControllerGetSortedItemsOrder",
    "PantryListItemsControllerGetSortedItemsSortBy",
    "PantryLocationDto",
    "PantryLocationDtoNameType1",
    "PantryOfferMatchDto",
    "PantrySettingsDto",
    "ParseNutrimentsIngredientDto",
    "ParseNutrimentsRequestDto",
    "ParseNutrimentsResultDto",
    "ParseRecipeAdditionalAttachment",
    "ParseRecipeCollectionAttachmentDto",
    "ParseRecipeCollectionRequestDto",
    "ParseRecipeFromAttachment",
    "ParseRecipeRequestDto",
    "ParseRecipeRequestDtoType",
    "ParseRecipeTextRequestDto",
    "PartialStepDto",
    "PremiumInvitationBaseDataDto",
    "PremiumInvitationDataDto",
    "PremiumInvitationDto",
    "PriceTrendContentChangeDto",
    "PriceTrendDetailDto",
    "PriceTrendItemDto",
    "PriceTrendPointDto",
    "PriceTrendsPageDto",
    "PriceType",
    "PriceWithDateDto",
    "ProcessStripeSessionDto",
    "ProviderLoginDto",
    "ProviderProfileDto",
    "PublicUserDto",
    "PublicUserDtoForcedPremiumTariff",
    "PurchasedItemDto",
    "PurchasedItemDtoDiscountType",
    "PurchasedItemDtoPriceType",
    "PurchasePageDto",
    "ReceiptCategory",
    "RecipeApi",
    "RecipeCollectionControllerGetCollectionsType",
    "RecipeCollectionDto",
    "RecipeDeckRequestDto",
    "RecipeDeckRequestDtoCategoriesItem",
    "RecipeDeckRequestDtoDietaryStylesItem",
    "RecipeDeckRequestDtoExcludeAllergensItem",
    "RecipeDeckRequestDtoLanguage",
    "RecipeDeckRequestDtoPantryFilter",
    "RecipeDeckRequestDtoSortBy",
    "RecipeDto",
    "RecipeDtoLanguage",
    "RecipeMatchedIngredientDto",
    "RecipeMatchStateDto",
    "RecipeMatchStateDtoIngredientDensities",
    "RecipeMatchStateRequestDto",
    "RecipeOrigin",
    "RecipeParserControllerParseFileRecipeBody",
    "RecipeParserControllerParseRecipeCollectionFromFileBody",
    "RecipeParsingCollectionResultDto",
    "RecipeParsingResultDto",
    "RecipeParsingResultDtoLanguage",
    "RecipePlanStatsDto",
    "RecipeSourceDto",
    "RecipeSubstitutableIngredientDto",
    "RecipeSubstitutableIngredientDtoConfidence",
    "RecipeSubstitutableIngredientDtoKind",
    "RefreshTokenDto",
    "RegisterDto",
    "RegisterMarketArrivalDeviceDto",
    "ReportSubstitutionDto",
    "ReportSubstitutionResultDto",
    "ReportSubstitutionResultDtoStatus",
    "ResetPasswordDto",
    "Role",
    "S3ControllerDeleteFileOwnerType",
    "SavedForRecipeDto",
    "SearchForBarcodeDto",
    "SendNotificationDto",
    "SendNotificationDtoData",
    "SetUserStoresDto",
    "ShoppingCartItemDto",
    "ShoppingCartItemsControllerGetCountResponse200",
    "ShoppingListItemsControllerGetSortedItemsOrder",
    "ShoppingListSettingsDto",
    "SmartSuggestionsSettingsDto",
    "SocialPlatform",
    "StepDto",
    "StorageLocationDto",
    "StoreDto",
    "StoreDtoNoOffersReason",
    "StoreDtoOpeningHours",
    "StoreOffersDto",
    "StoreOffersDtoNoOffersReason",
    "SubscriptionValidationResponseDto",
    "SubstitutionSuggestionDto",
    "SubstitutionSuggestionDtoConfidence",
    "SubstitutionSuggestionDtoKind",
    "SuccessDto",
    "SupermarketDto",
    "SwipeDecisionDto",
    "SwipeDecisionDtoDecision",
    "SwipeWeekPlanTargetDto",
    "SyncFirebaseInvitationDto",
    "UnitDto",
    "UpdateCollectionAssignmentDto",
    "UpdateItemDto",
    "UpdateListDto",
    "UpdateNfcTagDto",
    "UpdateUserDto",
    "UpsertLoyaltyCardDto",
    "UserDto",
    "UserDtoForcedPremiumTariff",
    "UserDtoUserCountrySource",
    "UserPermissionsDto",
    "UserSubscriptionDto",
    "UserSubscriptionDtoStatus",
    "UserSubscriptionDtoStore",
    "ValueWithMetricAndOpeningDto",
    "ValueWithMetricAndOpeningDtoMetric",
    "ValueWithMetricDto",
    "ValueWithMetricDtoMetric",
    "VerifyEmailDto",
    "VerifyEmailResponseDto",
    "VolumeUnit",
    "VoteDto",
    "WeekPlanDayDto",
    "WeekPlanReceiptDto",
    "WeekPlanReceiptDtoType",
    "WeighingDto",
    "WeighingUnit",
    "WsDataCollection",
    "WsEventCollectionDto",
)
