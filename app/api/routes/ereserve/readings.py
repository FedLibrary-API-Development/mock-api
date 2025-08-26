from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    ReadingData, ReadingAttributes,
    ReadingListJsonApiResponse, ReadingJsonApiResponse
)
from .common import build_pagination_links

reading_router = APIRouter(
    tags=["Reading"],
    dependencies=[Depends(get_authenticated_user)]
)

@reading_router.get(
    "/readings", 
    response_model=ReadingListJsonApiResponse,
    summary="All Readings",
    responses={
        200: {
            "description": "List of readings",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "readings",
                                "attributes": {
                                    "reading-title": "Maintenance effectiveness and economic models in the terotechnology concept",
                                    "source-document-title": "Maintenance Management International",
                                    "source-document-genre": "Whole Journal",
                                    "source-document-genre-code": "journal",
                                    "source-document-kind": "journal",
                                    "source-document-authors": None,
                                    "source-document-publisher": None,
                                    "source-document-publication-year": "1984",
                                    "source-document-edition": None,
                                    "source-document-volume": "4",
                                    "source-document-isbn": None,
                                    "source-document-eisbn": None,
                                    "source-document-issn": "0167-5389",
                                    "source-document-eissn": None,
                                    "source-document-created-at": "2019-01-16T12:36:42.000Z",
                                    "source-document-updated-at": "2023-11-20T05:17:35.000Z",
                                    "publication-year": "1984",
                                    "volume": "4",
                                    "genre": "Journal Article",
                                    "genre-code": "article-journal",
                                    "kind": "file",
                                    "article-number": "",
                                    "date": None,
                                    "date-accessed": None,
                                    "date-issued": None,
                                    "authors": "Ahlmann, Hans",
                                    "pages": "131-139",
                                    "reading-url": "",
                                    "count-kind": "Paginated",
                                    "created-at": "2019-01-16T12:36:43.000Z",
                                    "updated-at": "2024-10-02T04:39:49.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/readings?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/readings?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/readings?page%5Bnumber%5D=17007&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_readings(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all readings in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("readings", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    reading_data = []
    for reading in result["items"]:
        reading_attributes = ReadingAttributes(
            reading_title=reading["reading_title"],
            source_document_title=reading["source_document_title"],
            source_document_genre=reading["source_document_genre"],
            source_document_genre_code=reading["source_document_genre_code"],
            source_document_kind=reading["source_document_kind"],
            source_document_authors=reading.get("source_document_authors"),
            source_document_publisher=reading.get("source_document_publisher"),
            source_document_publication_year=reading.get("source_document_publication_year"),
            source_document_edition=reading.get("source_document_edition"),
            source_document_volume=reading.get("source_document_volume"),
            source_document_isbn=reading.get("source_document_isbn"),
            source_document_eisbn=reading.get("source_document_eisbn"),
            source_document_issn=reading.get("source_document_issn"),
            source_document_eissn=reading.get("source_document_eissn"),
            source_document_created_at=reading.get("source_document_created_at", ""),
            source_document_updated_at=reading.get("source_document_updated_at", ""),
            publication_year=reading.get("source_document_publication_year"),  # Assuming this maps to source_document_publication_year
            volume=reading.get("source_document_volume"),  # Assuming this maps to source_document_volume
            genre=reading["genre"],
            genre_code=reading["genre_code"],
            kind=reading["kind"],
            article_number=reading.get("article_number", ""),
            date=reading.get("date"),
            date_accessed=reading.get("date_accessed"),
            date_issued=reading.get("date_issued"),
            authors=reading["authors"],
            pages=reading.get("pages"),
            reading_url=reading.get("reading_url", ""),
            count_kind=reading.get("count_kind"),
            created_at=reading.get("created_at", ""),
            updated_at=reading.get("updated_at", "")
        )
        reading_item = ReadingData(
            id=str(reading["id"]),
            attributes=reading_attributes
        )
        reading_data.append(reading_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return ReadingListJsonApiResponse(data=reading_data, links=links.dict(exclude_none=True))

@reading_router.get(
    "/readings/{id}", 
    response_model=ReadingJsonApiResponse,
    summary="Find Reading by ID",
    responses={
        200: {
            "description": "Reading details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "readings",
                            "attributes": {
                                "reading-title": "A diagnostic key for wear debris obtained from oil, grease samples from operating machinery",
                                "source-document-title": "The Bulletin of the Centre for Machine Condition Monitoring",
                                "source-document-genre": "Whole Journal",
                                "source-document-genre-code": "journal",
                                "source-document-kind": "journal",
                                "source-document-authors": None,
                                "source-document-publisher": None,
                                "source-document-publication-year": "1989",
                                "source-document-edition": None,
                                "source-document-volume": "1",
                                "source-document-isbn": None,
                                "source-document-eisbn": None,
                                "source-document-issn": "1037-1222",
                                "source-document-eissn": None,
                                "source-document-created-at": "2019-01-16T12:36:44.000Z",
                                "source-document-updated-at": "2022-07-20T00:18:30.000Z",
                                "publication-year": "1989",
                                "volume": "1",
                                "genre": "Journal Article",
                                "genre-code": "article-journal",
                                "kind": "file",
                                "article-number": "",
                                "date": None,
                                "date-accessed": None,
                                "date-issued": None,
                                "authors": "Anderson, Marion",
                                "pages": "1-15",
                                "reading-url": "",
                                "count-kind": "Paginated",
                                "created-at": "2019-01-16T12:36:44.000Z",
                                "updated-at": "2024-08-09T02:21:15.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Reading not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in readings"
                        }]
                    }
                }
            }
        }
    }
)
async def get_reading(
    id: str = Path(..., description="Reading ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific reading by ID in JSON API format'''
    reading = repo.get_by_id("readings", id)
    
    # Convert to JSON API format
    reading_attributes = ReadingAttributes(
        reading_title=reading["reading_title"],
        source_document_title=reading["source_document_title"],
        source_document_genre=reading["source_document_genre"],
        source_document_genre_code=reading["source_document_genre_code"],
        source_document_kind=reading["source_document_kind"],
        source_document_authors=reading.get("source_document_authors"),
        source_document_publisher=reading.get("source_document_publisher"),
        source_document_publication_year=reading.get("source_document_publication_year"),
        source_document_edition=reading.get("source_document_edition"),
        source_document_volume=reading.get("source_document_volume"),
        source_document_isbn=reading.get("source_document_isbn"),
        source_document_eisbn=reading.get("source_document_eisbn"),
        source_document_issn=reading.get("source_document_issn"),
        source_document_eissn=reading.get("source_document_eissn"),
        source_document_created_at=reading.get("source_document_created_at", ""),
        source_document_updated_at=reading.get("source_document_updated_at", ""),
        publication_year=reading.get("source_document_publication_year"),  # Assuming this maps to source_document_publication_year
        volume=reading.get("source_document_volume"),  # Assuming this maps to source_document_volume
        genre=reading["genre"],
        genre_code=reading["genre_code"],
        kind=reading["kind"],
        article_number=reading.get("article_number", ""),
        date=reading.get("date"),
        date_accessed=reading.get("date_accessed"),
        date_issued=reading.get("date_issued"),
        authors=reading["authors"],
        pages=reading.get("pages"),
        reading_url=reading.get("reading_url", ""),
        count_kind=reading.get("count_kind"),
        created_at=reading.get("created_at", ""),
        updated_at=reading.get("updated_at", "")
    )
    reading_data = ReadingData(
        id=str(reading["id"]),
        attributes=reading_attributes
    )
    
    return ReadingJsonApiResponse(data=reading_data)

router = reading_router