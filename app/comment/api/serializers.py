from rest_framework import serializers
from comment.models import Comment
from comment.my_validators import validate_owner

class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='cmt_test_api_sing',
        lookup_field='pk'
    )

    owner = serializers.SerializerMethodField('_owner',validators=[validate_owner],read_only=True)

    class Meta:
        model = Comment
        fields = ('url','owner', 'product', 'content', 'created_at')

    def _owner(self, obj):
        if obj.owner:
            return obj.owner.username
        return None
