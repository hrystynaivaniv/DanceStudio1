class Repository:
    model = None

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def add(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def update(self, pk, **kwargs):
        obj = self.get_by_id(pk)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.save()
        return obj

    def delete(self, pk):
        obj = self.get_by_id(pk)
        if obj:
            obj.delete()
            return True
        return False
