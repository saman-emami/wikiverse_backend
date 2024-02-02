from rest_framework import serializers
from articles.models import Translations, Article
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TransltionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['slug', 'language']

class GetArticleSerializer(serializers.ModelSerializer):
    translations = serializers.SerializerMethodField('get_translations')

    class Meta:
        model = Article
        fields = ['id', 'translation_parent', 'translations', 'language', 'title', 'body', 'slug', 'created', 'updated']

    def get_translations(self, instance):
        translation_objects = instance.translation_parent.translation_objects
        return TransltionsSerializer(translation_objects, many=True).data
    
class PostArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['translation_parent', 'language', 'title', 'body', 'slug']

    def create(self, validated_data):
        if 'translation_parent' in validated_data:
            translation_parent = validated_data.pop('translation_parent')
        else:
            translation_parent = Translations.objects.create()
        article = Article.objects.create(translation_parent=translation_parent , **validated_data)
       
        return article

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token