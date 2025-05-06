from django.core.management.base import BaseCommand
from django.utils import timezone
from dns_updater.models import DNSRecord, UpdateLog
from dns_updater.services import LinodeAPIService
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update DNS records that need to be updated'

    def handle(self, *args, **options):
        linode_service = LinodeAPIService()
        
        try:
            current_ip = linode_service.get_current_ip()
            logger.info(f"Current IP address: {current_ip}")
        except Exception as e:
            logger.error(f"Failed to get current IP address: {e}")
            return

        # Get records that need to be updated
        records = DNSRecord.objects.filter(
            enabled=True,
            last_updated__lte=timezone.now() - timedelta(seconds=300)  # Default to 5 minutes
        ).select_related('domain')

        for record in records:
            if record.current_value == current_ip:
                logger.debug(f"Record {record} already has correct IP")
                continue

            try:
                # Update the record in Linode
                linode_service.update_domain_record(
                    domain_id=record.domain.domain_id,
                    record_id=record.record_id,
                    target=current_ip
                )

                # Log the update
                UpdateLog.objects.create(
                    record=record,
                    old_value=record.current_value,
                    new_value=current_ip,
                    success=True
                )

                # Update the record's current value
                record.current_value = current_ip
                record.save()

                logger.info(f"Successfully updated {record} to {current_ip}")

            except Exception as e:
                error_msg = str(e)
                logger.error(f"Failed to update {record}: {error_msg}")
                
                # Log the failed update
                UpdateLog.objects.create(
                    record=record,
                    old_value=record.current_value,
                    new_value=current_ip,
                    success=False,
                    error_message=error_msg
                ) 