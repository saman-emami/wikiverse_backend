from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import GetArticleSerializer, PostArticleSerializer
from articles.models import Article

@api_view(['POST'])
def register(request):
    if User.objects.filter(username=request.data.get('username')).exists():
        return Response({'error' : 'user already exists'})

    user = User.objects.create_user(username=request.data.get('username'), password=request.data.get('password'))

    refresh = RefreshToken.for_user(user)
    refresh['username'] = str(user.username)

    login = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    return Response(login)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def articles(request):
    if Article.objects.filter(title=request.data['title'], language=request.data['language']).exists():
        return Response({'error': 'article already exists'})

    serializer = PostArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article(request, language, slug):
    article = None

    try:
        article = Article.objects.get(slug=slug, language=language)
    except:
         return Response({'error': 404})

    if request.method == 'GET':
        serializer = GetArticleSerializer(article)
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        article_id = article.id
        article.delete()
        return Response('deleted_article_id: ' + str(article_id))
    
    if request.method == 'PUT':
        serializer = PostArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
@api_view(['GET'])
def homepage(request, language):
    recently_added_articles = Article.objects.all().order_by('-created')[:5]
    recently_edited_articles = Article.objects.all().order_by('-updated')[:5]
    user_language_articles = Article.objects.filter(language=language).order_by('-created')[:5]

    recently_added_articles_serializer = GetArticleSerializer(recently_added_articles, many=True)
    recently_edited_articles_serializer = GetArticleSerializer(recently_edited_articles, many=True)
    user_language_articles_serializer = GetArticleSerializer(user_language_articles, many=True)

    response = {
        'recentlyAdded' : recently_added_articles_serializer.data,
        'recentlyEdited': recently_edited_articles_serializer.data, 
        'userLanguageArticles': user_language_articles_serializer.data
    }

    return Response(response)

@api_view(['GET'])
def search(request, search_input):
    articles = Article.objects.filter(Q(title__icontains=search_input))
    serializer = GetArticleSerializer(articles, many=True)

    return Response(serializer.data)
