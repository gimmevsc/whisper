# from celery import shared_task
# from django.utils import timezone
# from .models import User

# @shared_task
# def cleanup_incomplete_registrations():
#     # Define the time threshold for incomplete registrations (e.g., 5 minutes ago)
#     threshold_time = timezone.now() - timezone.timedelta(minutes=1)
#     # Query incomplete registrations older than the threshold time
#     incomplete_registrations = User.objects.filter(created_at__lt=threshold_time)
#     print('sds')
#     # Delete incomplete registrations
#     incomplete_registrations.delete()
