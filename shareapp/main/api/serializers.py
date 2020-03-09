from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from shareapp.main.models import SharedItem, Retrieval


class FileWithoutPathField(serializers.FileField):
    def to_representation(self, value):
        if value:
            return value.name.rsplit("/")[-1]
        return super().to_representation(value)


class SharedItemSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field=SharedItem.id, read_only=True)
    file = FileWithoutPathField(required=False)

    def create(self, validated_data):
        if validated_data.get("url") and validated_data.get("file"):
            raise serializers.ValidationError(
                detail="Submit either 'file' or 'url', not both."
            )
        return super().create(validated_data)

    class Meta:
        model = SharedItem
        fields = ["id", "password", "url", "file", "expires", "views"]
        read_only_fields = ["expires", "views", "password"]


class RetrievalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retrieval
        fields = "__all__"
