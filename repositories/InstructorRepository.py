from django.db.models import Count

from core.models import Instructor
from .Repository import Repository

class InstructorRepository(Repository):
    model = Instructor

    def get_top_instructors(self, limit=5):
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 5

        return (
            self.model.objects
            .annotate(class_count=Count('classes'))
            .values('instructor_id', 'name', 'surname', 'class_count')
            .order_by('-class_count')[:limit]
        )