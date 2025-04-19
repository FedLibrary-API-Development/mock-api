from fastapi import APIRouter, Depends, Query, Path

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    School, Unit, UnitOffering, Reading, ReadingList,
    ReadingListUsage, ReadingListItem, ReadingListItemUsage,
    ReadingUtilisation, IntegrationUser, TeachingSession,
    PaginatedResponse
)

# Helper function for pagination
async def get_paginated_response(
    collection: str,
    skip: int = 0,
    limit: int = 100,
    repo: EReserveRepository = Depends(get_ereserve_repository)
) -> PaginatedResponse:
    result = repo.get_all(collection, skip=skip, limit=limit)
    return PaginatedResponse(items=result["items"], count=result["count"])


# School endpoints
school_router = APIRouter(dependencies=[get_authenticated_user()])

@school_router.get("/schools", response_model=PaginatedResponse, summary="All Schools")
async def all_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all schools'''
    return await get_paginated_response("schools", skip, limit, repo)

@school_router.get("/schools/{school_id}", response_model=School, summary="Find school by ID")
async def get_school(
    school_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("schools", school_id)

# Units endpoints
unit_router = APIRouter(dependencies=[get_authenticated_user()])

@unit_router.get("/units", response_model=PaginatedResponse, summary="All Units")
async def list_units(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("units", skip, limit, repo)

@unit_router.get("/units/{unit_id}", response_model=Unit, summary="Find Unit by ID")
async def get_unit(
    unit_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("units", unit_id)

# Unit Offering endpoints
unit_offering_router = APIRouter(dependencies=[get_authenticated_user()])

@unit_offering_router.get("/unit-offerings", response_model=PaginatedResponse, summary="All unit offerings")
async def list_unit_offerings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("unitOfferings", skip, limit, repo)

@unit_offering_router.get("/unit-offerings/{offering_id}", response_model=UnitOffering, summary="Find Unit Offering by ID")
async def get_unit_offering(
    offering_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("unitOfferings", offering_id)

# Reading endpoints
reading_router = APIRouter(dependencies=[get_authenticated_user()])

@reading_router.get("/readings", response_model=PaginatedResponse, summary="All readings")
async def list_readings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("readings", skip, limit, repo)

@reading_router.get("/readings/{reading_id}", response_model=Reading, summary="Find Reading by ID")
async def get_reading(
    reading_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("readings", reading_id)

# Reading List endpoints
reading_list_router = APIRouter(dependencies=[get_authenticated_user()])

@reading_list_router.get("/reading-lists", response_model=PaginatedResponse, summary="All reading lists")
async def list_reading_lists(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("readingLists", skip, limit, repo)

@reading_list_router.get("/reading-lists/{list_id}", response_model=ReadingList, summary="Find Reading List by ID")
async def get_reading_list(
    list_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("readingLists", list_id)

# Reading List Usage endpoints
reading_list_usage_router = APIRouter(dependencies=[get_authenticated_user()])

@reading_list_usage_router.get("/reading-list-usages", response_model=PaginatedResponse, summary="All reading list usages")
async def list_reading_list_usages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("readingListUsages", skip, limit, repo)

@reading_list_usage_router.get("/reading-list-usages/{usage_id}", response_model=ReadingListUsage, summary="Find Reading List Usage by ID")
async def get_reading_list_usage(
    usage_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("readingListUsages", usage_id)

# Reading List Item endpoints
reading_list_item_router = APIRouter(dependencies=[get_authenticated_user()])

@reading_list_item_router.get("/reading-list-items", response_model=PaginatedResponse, summary="All reading list items")
async def list_reading_list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("readingListItems", skip, limit, repo)

@reading_list_item_router.get("/reading-list-items/{item_id}", response_model=ReadingListItem, summary="Find reading list item by ID")
async def get_reading_list_item(
    item_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("readingListItems", item_id)

# Reading List Item Usage endpoints
reading_list_item_usage_router = APIRouter(dependencies=[get_authenticated_user()])
@reading_list_item_usage_router.get("/reading-list-item-usages", response_model=PaginatedResponse, summary="All reading list item usages")
async def list_reading_list_item_usages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("readingListItemUsages", skip, limit, repo)

@reading_list_item_usage_router.get("/reading-list-item-usages/{usage_id}", response_model=ReadingListItemUsage, summary="Find reading list item usage by ID")
async def get_reading_list_item_usage(
    usage_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("readingListItemUsages", usage_id)

# Reading Utilisation endpoints
reading_utilisation_router = APIRouter(dependencies=[get_authenticated_user()])

@reading_utilisation_router.get("/reading-utilisations", response_model=PaginatedResponse, summary="All reading utilisations")
async def list_reading_utilisations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("readingUtilisations", skip, limit, repo)

@reading_utilisation_router.get("/reading-utilisations/{utilisation_id}", response_model=ReadingUtilisation, summary="Find reading utilisation by ID")
async def get_reading_utilisation(
    utilisation_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("readingUtilisations", utilisation_id)

# Integration User endpoints
integration_user_router = APIRouter(dependencies=[get_authenticated_user()])

@integration_user_router.get("/integration-users", response_model=PaginatedResponse, summary="All integration users")
async def list_integration_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("integrationUsers", skip, limit, repo)

@integration_user_router.get("/integration-users/{user_id}", response_model=IntegrationUser, summary="Find integration user by ID")
async def get_integration_user(
    user_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("integrationUsers", user_id)

# Teaching Session endpoints
teaching_session_router = APIRouter(dependencies=[get_authenticated_user()])

@teaching_session_router.get("/teaching-sessions", response_model=PaginatedResponse, summary="All teaching sessions")
async def list_teaching_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return await get_paginated_response("teachingSessions", skip, limit, repo)

@teaching_session_router.get("/teaching-sessions/{session_id}", response_model=TeachingSession, summary="Find teaching session by ID")
async def get_teaching_session(
    session_id: int = Path(..., gt=0),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    return repo.get_by_id("teachingSessions", session_id)


router = APIRouter(dependencies=[get_authenticated_user()])

router.include_router(school_router, tags=["School"])
router.include_router(unit_router, tags=["Unit"])
router.include_router(unit_offering_router, tags=["UnitOffering"])
router.include_router(reading_router, tags=["Reading"])
router.include_router(reading_list_router, tags=["ReadingList"])
router.include_router(reading_list_usage_router, tags=["ReadingListUsage"])
router.include_router(reading_list_item_router, tags=["ReadingListItem"])
router.include_router(reading_list_item_usage_router, tags=["ReadingListItemUsage"])
router.include_router(reading_utilisation_router, tags=["ReadingUtilization"])
router.include_router(integration_user_router, tags=["IntegrationUser"])
router.include_router(teaching_session_router, tags=["TeachingSession"])