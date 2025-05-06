from django.core.management.base import BaseCommand
from django.utils import timezone
from dns_updater.models import DNSRecord
from dns_updater.services import LinodeAPIService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates DNS records with current IP address'

    def handle(self, *args, **options):
        try:
            linode_service = LinodeAPIService()
            current_ip = linode_service.get_current_ip()
            
            for record in DNSRecord.objects.filter(enabled=True):
                try:
                    if record.current_value != current_ip:
                        linode_service.update_domain_record(
                            record.domain.domain_id,
                            record.record_id,
                            current_ip
                        )
                        record.current_value = current_ip
                        record.save()
                        logger.info(f"Updated {record} to {current_ip}")
                except Exception as e:
                    logger.error(f"Failed to update {record}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error in update_dns command: {str(e)}") 