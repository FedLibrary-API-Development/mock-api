from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Common base models for shared fields
class DateTimeBase(BaseModel):
    created_at: datetime
    updated_at: datetime

class IDBase(BaseModel):
    id: int

# School models
class SchoolBase(IDBase):
    name: str

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    class Config:
        from_attributes = True

# Unit models
class UnitBase(IDBase):
    code: str
    name: str

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    class Config:
        from_attributes = True

# Unit Offering models
class UnitOfferingBase(IDBase, DateTimeBase):
    unit_id: int
    reading_list_id: int
    source_unit_code: str
    source_unit_name: str
    source_unit_offering: str
    result: str
    list_publication_method: str

class UnitOfferingCreate(UnitOfferingBase):
    pass

class UnitOffering(UnitOfferingBase):
    class Config:
        from_attributes = True

# Reading models
class ReadingSourceDocument(BaseModel):
    title: str
    genre: str
    genre_code: str
    kind: str
    authors: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[str] = None
    edition: Optional[str] = None
    volume: Optional[str] = None
    isbn: Optional[str] = None
    eisbn: Optional[str] = None
    issn: Optional[str] = None
    eissn: Optional[str] = None

class ReadingBase(IDBase, DateTimeBase):
    source_document_title: str
    source_document_genre: str
    source_document_genre_code: str
    source_document_kind: str
    source_document_authors: Optional[str] = None
    source_document_publisher: Optional[str] = None
    source_document_publication_year: Optional[str] = None
    source_document_edition: Optional[str] = None
    source_document_volume: Optional[str] = None
    source_document_isbn: Optional[str] = None
    source_document_eisbn: Optional[str] = None
    source_document_issn: Optional[str] = None
    source_document_eissn: Optional[str] = None
    reading_title: str
    genre: str
    genre_code: str
    kind: str
    article_number: Optional[str] = None
    date: Optional[datetime] = None
    date_issued: Optional[datetime] = None
    date_accessed: Optional[datetime] = None
    authors: str
    pages: Optional[str] = None
    reading_url: Optional[str] = None
    count_kind: Optional[str] = None

class ReadingCreate(ReadingBase):
    pass

class Reading(ReadingBase):
    class Config:
        from_attributes = True

# Reading List models
class ReadingListBase(IDBase, DateTimeBase):
    unit_id: int
    teaching_session_id: int
    name: str
    duration: str
    start_date: str
    end_date: str
    hidden: bool
    usage_count: int
    item_count: int
    approved_item_count: int
    deleted: bool

class ReadingListCreate(ReadingListBase):
    pass

class ReadingList(ReadingListBase):
    class Config:
        from_attributes = True

# Reading List Usage models
class ReadingListUsageBase(IDBase, DateTimeBase):
    list_id: int
    integration_user_id: int
    item_usage_count: int

class ReadingListUsageCreate(ReadingListUsageBase):
    pass

class ReadingListUsage(ReadingListUsageBase):
    class Config:
        from_attributes = True

# Reading List Item models
class ReadingListItemBase(IDBase, DateTimeBase):
    list_id: int
    reading_id: int
    status: str
    hidden: bool
    reading_utilisations_count: int
    reading_importance: str
    usage_count: int

class ReadingListItemCreate(ReadingListItemBase):
    pass

class ReadingListItem(ReadingListItemBase):
    class Config:
        from_attributes = True

# Reading List Item Usage models
class ReadingListItemUsageBase(IDBase, DateTimeBase):
    item_id: int
    list_usage_id: int
    integration_user_id: int
    utilisation_count: int

class ReadingListItemUsageCreate(ReadingListItemUsageBase):
    pass

class ReadingListItemUsage(ReadingListItemUsageBase):
    class Config:
        from_attributes = True

# Reading Utilisation models
class ReadingUtilisationBase(IDBase, DateTimeBase):
    integration_user_id: int
    item_id: int
    item_usage_id: int

class ReadingUtilisationCreate(ReadingUtilisationBase):
    pass

class ReadingUtilisation(ReadingUtilisationBase):
    class Config:
        from_attributes = True

# Integration User models
class IntegrationUserBase(IDBase, DateTimeBase):
    identifier: str
    roles: str
    first_name: str
    last_name: str
    email: EmailStr
    lti_consumer_user_id: str
    lti_lis_person_sourcedid: str

class IntegrationUserCreate(IntegrationUserBase):
    pass

class IntegrationUser(IntegrationUserBase):
    class Config:
        from_attributes = True

# Teaching Session models
class TeachingSessionBase(IDBase, DateTimeBase):
    name: str
    start_date: str
    end_date: str
    archived: bool

class TeachingSessionCreate(TeachingSessionBase):
    pass

class TeachingSession(TeachingSessionBase):
    class Config:
        from_attributes = True

# User models (for authentication)
class UserBase(IDBase, DateTimeBase):
    first_name: str
    last_name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    class Config:
        from_attributes = True

# Response models for collections
class PaginatedResponse(BaseModel):
    items: List[Any]
    count: int

class SchoolListResponse(PaginatedResponse):
    items: List[School]

class UnitListResponse(PaginatedResponse):
    items: List[Unit]

class UnitOfferingListResponse(PaginatedResponse):
    items: List[UnitOffering]

class ReadingListResponse(PaginatedResponse):
    items: List[Reading]

class ReadingListListResponse(PaginatedResponse):
    items: List[ReadingList]

class ReadingListUsageListResponse(PaginatedResponse):
    items: List[ReadingListUsage]

class ReadingListItemListResponse(PaginatedResponse):
    items: List[ReadingListItem]

class ReadingListItemUsageListResponse(PaginatedResponse):
    items: List[ReadingListItemUsage]

class ReadingUtilisationListResponse(PaginatedResponse):
    items: List[ReadingUtilisation]

class IntegrationUserListResponse(PaginatedResponse):
    items: List[IntegrationUser]

class TeachingSessionListResponse(PaginatedResponse):
    items: List[TeachingSession]