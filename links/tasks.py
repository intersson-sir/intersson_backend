"""
Celery tasks for the links app.
"""
import logging
import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import NegativeLink

logger = logging.getLogger(__name__)


@shared_task
def check_urls_availability():
    """
    Periodic task to check URL availability for all active links.
    
    This task checks if URLs are still accessible (HTTP status check).
    If a URL returns 404 or similar error, it can optionally update the status.
    
    This task is controlled by the ENABLE_URL_CHECK_TASK setting.
    """
    if not settings.ENABLE_URL_CHECK_TASK:
        logger.info("URL check task is disabled via settings")
        return {
            'status': 'disabled',
            'message': 'URL check task is disabled in settings'
        }
    
    logger.info("Starting URL availability check task")
    
    # Get all links that are active or in_work
    links_to_check = NegativeLink.objects.filter(
        status__in=['active', 'in_work']
    )
    
    total_checked = 0
    unavailable_count = 0
    error_count = 0
    
    for link in links_to_check:
        try:
            total_checked += 1
            
            # Perform HEAD request to check availability
            response = requests.head(
                link.url,
                timeout=10,
                allow_redirects=True,
                headers={'User-Agent': 'Phil-CRM-Bot/1.0'}
            )
            
            # If URL returns 404, 410 (Gone), or 403, consider it potentially removed
            if response.status_code in [404, 410, 403]:
                logger.info(
                    f"URL {link.url} returned {response.status_code}. "
                    f"Adding note to link {link.id}"
                )
                
                # Add note instead of auto-updating status
                # This allows manual review before marking as removed
                current_notes = link.notes or ""
                new_note = (
                    f"\n[{timezone.now().isoformat()}] "
                    f"Automated check: URL returned HTTP {response.status_code}"
                )
                link.notes = current_notes + new_note
                link.save()
                
                unavailable_count += 1
            
            elif response.status_code >= 200 and response.status_code < 400:
                logger.debug(f"URL {link.url} is accessible (HTTP {response.status_code})")
            
        except requests.RequestException as e:
            error_count += 1
            logger.warning(f"Error checking URL {link.url}: {str(e)}")
            
            # Add error note
            current_notes = link.notes or ""
            new_note = (
                f"\n[{timezone.now().isoformat()}] "
                f"Automated check failed: {str(e)[:100]}"
            )
            link.notes = current_notes + new_note
            link.save()
    
    result = {
        'status': 'completed',
        'total_checked': total_checked,
        'unavailable': unavailable_count,
        'errors': error_count,
        'timestamp': timezone.now().isoformat()
    }
    
    logger.info(
        f"URL check task completed. "
        f"Checked: {total_checked}, Unavailable: {unavailable_count}, Errors: {error_count}"
    )
    
    return result


@shared_task
def check_single_url(link_id):
    """
    Check availability of a single URL.
    
    Args:
        link_id: UUID of the NegativeLink to check
    
    Returns:
        dict: Result of the check
    """
    try:
        link = NegativeLink.objects.get(id=link_id)
    except NegativeLink.DoesNotExist:
        logger.error(f"Link with ID {link_id} not found")
        return {'status': 'error', 'message': 'Link not found'}
    
    logger.info(f"Checking single URL: {link.url}")
    
    try:
        response = requests.head(
            link.url,
            timeout=10,
            allow_redirects=True,
            headers={'User-Agent': 'Phil-CRM-Bot/1.0'}
        )
        
        result = {
            'status': 'success',
            'link_id': str(link_id),
            'url': link.url,
            'http_status': response.status_code,
            'accessible': response.status_code >= 200 and response.status_code < 400
        }
        
        logger.info(f"URL check result: {result}")
        return result
        
    except requests.RequestException as e:
        logger.error(f"Error checking URL {link.url}: {str(e)}")
        return {
            'status': 'error',
            'link_id': str(link_id),
            'url': link.url,
            'error': str(e)
        }


@shared_task
def clear_old_notes():
    """
    Optional task to clean up very old automated notes from links.
    
    This can be used to keep the notes field from growing too large.
    """
    logger.info("Starting old notes cleanup task")
    
    # This is a placeholder - implement based on your needs
    # For example, you could truncate notes older than 90 days
    
    return {'status': 'completed', 'message': 'Notes cleanup not implemented yet'}
