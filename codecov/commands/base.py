from django.contrib.auth.models import AnonymousUser

from codecov_auth.models import Owner


class BaseCommand:
    def __init__(self, current_owner: Owner, service: str):
        self.current_owner = current_owner
        self.service = service
        self.executor = None

    def get_interactor(self, InteractorKlass):
        return InteractorKlass(self.current_owner, self.service)

    def get_command(self, namespace):
        """
        Allow a command to call another command
        """
        if not self.executor:
            # local import to avoid circular import; I'm not too happy about
            # this pattern yet
            from .executor import get_executor_from_command

            self.executor = get_executor_from_command(self)
        return self.executor.get_command(namespace)


class BaseInteractor:
    def __init__(self, current_owner: Owner, service: str):
        self.current_owner = current_owner
        self.service = service
        self.current_user = AnonymousUser()
        if self.current_owner:
            self.current_user = self.current_owner.user
