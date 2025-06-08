from rest_framework import serializers
from core.models import Collections, Document


class CollectionsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('id', 'name', 'description')
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False}
        }


class CollectionsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Collections
        fields = ('id', 'name', 'description', 'documents')

    def get_documents(self, obj):
        return list(obj.documents.values_list('id', flat=True))


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title')


class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'content')


class DocumentCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    content = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'collections', 'owner', 'file')
        read_only_fields = ('owner',)

    def validate_file(self, value):
        if not value.name.endswith('.txt'):
            raise serializers.ValidationError(
                "Only .txt files are allowed"
            )
        try:
            content = value.read().decode('utf-8')
            value.seek(0)
            return content
        except UnicodeDecodeError:
            raise serializers.ValidationError(
                "File must be a valid UTF-8 text file"
            )

    def create(self, validated_data):
        file_content = validated_data.pop('file', None)
        if file_content:
            validated_data['content'] = file_content
            if not validated_data.get('title'):
                validated_data['title'] = self.context['request'].FILES['file'].name
        return super().create(validated_data)
