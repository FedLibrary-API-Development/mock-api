from typing import Optional, List, Dict
from pydantic import BaseModel, Field

# Pagination models for JSON API
class PageParams(BaseModel):
    number: int = 1
    size: int = 100

class JsonApiLinks(BaseModel):
    first: Optional[str] = None
    next: Optional[str] = None
    prev: Optional[str] = None
    last: Optional[str] = None

# JSON API models for schools
class SchoolAttributes(BaseModel):
    name: str

class SchoolData(BaseModel):
    id: str
    type: str = "schools"
    attributes: SchoolAttributes

class SchoolJsonApiResponse(BaseModel):
    data: SchoolData

class SchoolListJsonApiResponse(BaseModel):
    data: List[SchoolData]
    links: Optional[Dict[str, str]] = None
    

# JSON API models for unit
class UnitAttributes(BaseModel):
    code: str
    name: str
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        # allow_population_by_field_name = True
        validate_by_name = True

class UnitData(BaseModel):
    id: str
    type: str = "units"
    attributes: UnitAttributes

class UnitJsonApiResponse(BaseModel):
    data: UnitData

class UnitListJsonApiResponse(BaseModel):
    data: List[UnitData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for unit offering
class UnitOfferingAttributes(BaseModel):
    unit_id: int = Field(alias="unit-id")
    reading_list_id: Optional[int] = Field(None, alias="reading-list-id")
    source_unit_code: str = Field(alias="source-unit-code")
    source_unit_name: Optional[str] = Field(None, alias="source-unit-name")
    source_unit_offering: Optional[str] = Field(None, alias="source-unit-offering")
    result: str
    list_publication_method: str = Field(alias="list-publication-method")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class UnitOfferingData(BaseModel):
    id: str
    type: str = "unit-offerings"
    attributes: UnitOfferingAttributes

class UnitOfferingJsonApiResponse(BaseModel):
    data: UnitOfferingData

class UnitOfferingListJsonApiResponse(BaseModel):
    data: List[UnitOfferingData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for reading
class ReadingAttributes(BaseModel):
    reading_title: str = Field(alias="reading-title")
    source_document_title: str = Field(alias="source-document-title")
    source_document_genre: str = Field(alias="source-document-genre")
    source_document_genre_code: str = Field(alias="source-document-genre-code")
    source_document_kind: str = Field(alias="source-document-kind")
    source_document_authors: Optional[str] = Field(None, alias="source-document-authors")
    source_document_publisher: Optional[str] = Field(None, alias="source-document-publisher")
    source_document_publication_year: Optional[str] = Field(None, alias="source-document-publication-year")
    source_document_edition: Optional[str] = Field(None, alias="source-document-edition")
    source_document_volume: Optional[str] = Field(None, alias="source-document-volume")
    source_document_isbn: Optional[str] = Field(None, alias="source-document-isbn")
    source_document_eisbn: Optional[str] = Field(None, alias="source-document-eisbn")
    source_document_issn: Optional[str] = Field(None, alias="source-document-issn")
    source_document_eissn: Optional[str] = Field(None, alias="source-document-eissn")
    source_document_created_at: str = Field(alias="source-document-created-at")
    source_document_updated_at: str = Field(alias="source-document-updated-at")
    publication_year: Optional[str] = Field(None, alias="publication-year")
    volume: Optional[str] = Field(None, alias="volume")
    genre: str
    genre_code: str = Field(alias="genre-code")
    kind: str
    article_number: Optional[str] = Field(None, alias="article-number")
    date: Optional[str] = None
    date_accessed: Optional[str] = Field(None, alias="date-accessed")
    date_issued: Optional[str] = Field(None, alias="date-issued")
    authors: str
    pages: Optional[str] = None
    reading_url: Optional[str] = Field(None, alias="reading-url")
    count_kind: Optional[str] = Field(None, alias="count-kind")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class ReadingData(BaseModel):
    id: str
    type: str = "readings"
    attributes: ReadingAttributes

class ReadingJsonApiResponse(BaseModel):
    data: ReadingData

class ReadingListJsonApiResponse(BaseModel):
    data: List[ReadingData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for reading list
class ReadingListAttributes(BaseModel):
    unit_id: int = Field(alias="unit-id")
    teaching_session_id: Optional[int] = Field(None, alias="teaching-session-id")
    name: str
    duration: str
    start_date: str = Field(alias="start-date")
    end_date: str = Field(alias="end-date")
    hidden: bool
    item_count: int = Field(alias="item-count")
    approved_item_count: int = Field(alias="approved-item-count")
    usage_count: int = Field(alias="usage-count")
    deleted: bool
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class ReadingListData(BaseModel):
    id: str
    type: str = "reading-lists"
    attributes: ReadingListAttributes

class ReadingListJsonApiResponse(BaseModel):
    data: ReadingListData

class ReadingListListJsonApiResponse(BaseModel):
    data: List[ReadingListData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for reading list usage
class ReadingListUsageAttributes(BaseModel):
    list_id: int = Field(alias="list-id")
    integration_user_id: int = Field(alias="integration-user-id")
    item_usage_count: int = Field(alias="item-usage-count")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class ReadingListUsageData(BaseModel):
    id: str
    type: str = "reading-list-usages"
    attributes: ReadingListUsageAttributes

class ReadingListUsageJsonApiResponse(BaseModel):
    data: ReadingListUsageData

class ReadingListUsageListJsonApiResponse(BaseModel):
    data: List[ReadingListUsageData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for reading list item
class ReadingListItemAttributes(BaseModel):
    list_id: int = Field(alias="list-id")
    reading_id: int = Field(alias="reading-id")
    status: str
    hidden: bool
    reading_utilisations_count: int = Field(alias="reading-utilisations-count")
    reading_importance: str = Field(alias="reading-importance")
    usage_count: int = Field(alias="usage-count")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class ReadingListItemData(BaseModel):
    id: str
    type: str = "reading-list-items"
    attributes: ReadingListItemAttributes

class ReadingListItemJsonApiResponse(BaseModel):
    data: ReadingListItemData

class ReadingListItemListJsonApiResponse(BaseModel):
    data: List[ReadingListItemData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for reading list item usage
class ReadingListItemUsageAttributes(BaseModel):
    item_id: int = Field(alias="item-id")
    list_usage_id: int = Field(alias="list-usage-id")
    integration_user_id: int = Field(alias="integration-user-id")
    utilisation_count: int = Field(alias="utilisation-count")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class ReadingListItemUsageData(BaseModel):
    id: str
    type: str = "reading-list-item-usages"
    attributes: ReadingListItemUsageAttributes

class ReadingListItemUsageJsonApiResponse(BaseModel):
    data: ReadingListItemUsageData

class ReadingListItemUsageListJsonApiResponse(BaseModel):
    data: List[ReadingListItemUsageData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for reading-utilisations
class ReadingUtilisationAttributes(BaseModel):
    item_id: int = Field(alias="item-id")
    item_usage_id: int = Field(alias="item-usage-id")
    integration_user_id: int = Field(alias="integration-user-id")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class ReadingUtilisationData(BaseModel):
    id: str
    type: str = "reading-utilisations"
    attributes: ReadingUtilisationAttributes

class ReadingUtilisationJsonApiResponse(BaseModel):
    data: ReadingUtilisationData

class ReadingUtilisationListJsonApiResponse(BaseModel):
    data: List[ReadingUtilisationData]
    links: Optional[Dict[str, str]] = None
    
# JSON API models for integration-users
class IntegrationUserAttributes(BaseModel):
    identifier: str
    roles: str
    first_name: str = Field(alias="first-name")
    last_name: str = Field(alias="last-name")
    email: str
    lti_consumer_user_id: str = Field(alias="lti-consumer-user-id")
    lti_lis_person_sourcedid: str = Field(alias="lti-lis-person-sourcedid")
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class IntegrationUserData(BaseModel):
    id: str
    type: str = "integration-users"
    attributes: IntegrationUserAttributes

class IntegrationUserJsonApiResponse(BaseModel):
    data: IntegrationUserData

class IntegrationUserListJsonApiResponse(BaseModel):
    data: List[IntegrationUserData]
    links: Optional[Dict[str, str]] = None

# JSON API models for teaching-sessions
class TeachingSessionAttributes(BaseModel):
    name: str
    start_date: str = Field(alias="start-date")
    end_date: str = Field(alias="end-date")
    archived: bool
    created_at: str = Field(alias="created-at")
    updated_at: str = Field(alias="updated-at")
    
    class Config:
        validate_by_name = True

class TeachingSessionData(BaseModel):
    id: str
    type: str = "teaching-sessions"
    attributes: TeachingSessionAttributes

class TeachingSessionJsonApiResponse(BaseModel):
    data: TeachingSessionData

class TeachingSessionListJsonApiResponse(BaseModel):
    data: List[TeachingSessionData]
    links: Optional[Dict[str, str]] = None