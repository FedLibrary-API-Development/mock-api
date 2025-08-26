from fastapi import Request
from app.schemas.ereserve import JsonApiLinks

# Helper function for JSON API pagination
def build_pagination_links(
    request: Request, 
    current_page: int, 
    page_size: int, 
    total_pages: int
) -> JsonApiLinks:
    """Build pagination links for JSON API format"""
    base_url = str(request.url).split('?')[0]
    
    links = JsonApiLinks()
    
    # First page link
    links.first = f"{base_url}?page%5Bnumber%5D=1&page%5Bsize%5D={page_size}"
    
    # Last page link
    links.last = f"{base_url}?page%5Bnumber%5D={total_pages}&page%5Bsize%5D={page_size}"
    
    # Next page link
    if current_page < total_pages:
        links.next = f"{base_url}?page%5Bnumber%5D={current_page + 1}&page%5Bsize%5D={page_size}"
    
    # Previous page link
    if current_page > 1:
        links.prev = f"{base_url}?page%5Bnumber%5D={current_page - 1}&page%5Bsize%5D={page_size}"
    
    return links