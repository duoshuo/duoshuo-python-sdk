from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError

from duoshuo.utils import sync_user

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Tell me wha\'s data you want synchronization (user/article/comment)')
        if args[0] == 'user':
            sync_user()
#        for poll_id in args:
#            try:
#                poll = Poll.objects.get(pk=int(poll_id))
#            except Poll.DoesNotExist:
#                raise CommandError('Poll "%s" does not exist' % poll_id)
#
#            poll.opened = False
#            poll.save()
