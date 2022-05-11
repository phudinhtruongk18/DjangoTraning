
class OwnerQuerySetMixin():
    user_field = 'owner'
    def get_queryset(self, *args, **kwargs):

        lookup_data = {}
        lookup_data[self.user_field] = self.request.user

        queryset = super().get_queryset(self, *args, **kwargs)
        return queryset.filter(**lookup_data)
