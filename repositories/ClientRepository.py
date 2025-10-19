from core.models import Client
from .Repository import Repository

class ClientRepository(Repository):
    model = Client

    def get_by_name(self, name, surname):
        try:
            return self.model.objects.get(name=name, surname=surname)
        except self.model.DoesNotExist:
            return None

