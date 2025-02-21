from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import User, Post, Follow
from .serializers import UserSerializer, PostSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken




@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':  
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response({'error': 'Todos os campos são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"message": "E-mail já existe."}, status=status.HTTP_400_BAD_REQUEST)
                
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Nome de usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password) 
        if user:
            return Response({'message': 'Usuário criado com sucesso!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Erro ao criar o usuário.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh)
        })
        
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)    
  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.user.is_authenticated:  
        try:                
            request.user.auth_token.delete()
            logout(request)
            return Response({"detail": "Logged out successfully."}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
    else:
        return Response({"detail": "User is not authenticated."}, status=401)    
  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    try:       
        user = request.user        
       
        serializer = UserSerializer(user)
       
        return Response(serializer.data, status=status.HTTP_200_OK)    
    except Exception as e:       
        return Response({
            "detail": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    if request.method == 'GET':
        
        try:            
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:    
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':           
        serializer = PostSerializer(data=request.data)      
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    if request.method == 'GET':
        
        try:            
            queryset = Post.objects.all().order_by('-created_at')
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:    
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
        
    # Pega os dados do corpo da requisição
    follower_id = request.data.get('follower')
    following_id = request.data.get('following')
    

    # Valida se os dados foram fornecidos
    if not follower_id or not following_id:
        raise ValidationError("Os IDs de 'follower' e 'following' são obrigatórios.")   

    # Verifica se o usuário está tentando seguir a si mesmo
    if follower_id == following_id:
        return Response({"detail": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

    # Busca as instâncias de usuário a partir dos IDs fornecidos
    try:
        follower = User.objects.get(id=follower_id)
        following = User.objects.get(id=following_id)
    except User.DoesNotExist:
        return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    
    # Verifica se o relacionamento já existe
    follow_exists = Follow.objects.filter(follower=follower, following=following).exists()

    if follow_exists:
        return Response({"detail": "Você já está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

    # Cria o relacionamento de seguir
    Follow.objects.create(follower=follower, following=following)

    # Retorna uma resposta positiva
    return Response({"detail": f"Você começou a seguir {following.username} com sucesso!"}, status=status.HTTP_201_CREATED)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
     
    # Pega os dados de 'follower' e 'following' do corpo da requisição
    follower_id = request.data.get('follower')
    following_id = request.data.get('following')
    
     # Valida se os dados foram fornecidos
    if not follower_id or not following_id:
        return Response({"detail": "Os IDs de 'follower' e 'following' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica se o relacionamento existe
    follow_exists = Follow.objects.filter(follower=follower_id, following=following_id).exists()
    
    if not follow_exists:
        return Response({"detail": "Você não está seguindo esse usuário."}, status=status.HTTP_400_BAD_REQUEST)

    # Deleta o relacionamento de seguir
    Follow.objects.filter(follower=follower_id, following=following_id).delete()
    
    following = User.objects.get(id=following_id)

    # Retorna uma resposta positiva
    return Response({"detail": f"Você deixou de seguir {following.username}. "}, status=status.HTTP_200_OK)
    
