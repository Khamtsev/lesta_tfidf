from rest_framework import serializers
from core.models import Collections, Document


class WordStatisticsSerializer(serializers.Serializer): 
    """Сериализатор для статистики по слову."""
    word = serializers.CharField()
    tf = serializers.FloatField()
    idf = serializers.FloatField()


class StatisticsSerializer(serializers.Serializer):
    """Сериализатор для статистики по документу."""
    statistics = WordStatisticsSerializer(many=True)


class CollectionStatisticsSerializer(serializers.Serializer):
    """Сериализатор для статистики по коллекции."""
    collection_id = serializers.IntegerField()
    collection_name = serializers.CharField()
    statistics = WordStatisticsSerializer(many=True)


class CollectionsCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания коллекции."""
    class Meta:
        model = Collections
        fields = ('id', 'name', 'description')
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False}
        }


class CollectionsSerializer(serializers.ModelSerializer):
    """Сериализатор для списка коллекций."""
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Collections
        fields = ('id', 'name', 'description', 'documents')

    def get_documents(self, obj):
        return list(obj.documents.values_list('id', flat=True))


class DocumentListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка документов."""
    class Meta:
        model = Document
        fields = ('id', 'title')


class DocumentDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального отображения документа."""
    class Meta:
        model = Document
        fields = ('id', 'title', 'content')


class DocumentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания документа."""
    file = serializers.FileField(
        required=True,
        write_only=True,
        help_text='Текстовый файл для загрузки'
    )
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'title', 'file')
        read_only_fields = ('id', 'title')

    def validate_file(self, value):
        """Проверяет файл на соответствие требованиям."""
        if not value.name.endswith('.txt'):
            raise serializers.ValidationError(
                'Файл должен быть в формате .txt'
            )
        return value

    def create(self, validated_data):
        """Создает новый документ."""
        file = validated_data['file']
        content = file.read().decode('utf-8')
        title = file.name.rsplit('.', 1)[0]
        return Document.objects.create(
            title=title,
            content=content,
            owner=self.context['request'].user
        )
