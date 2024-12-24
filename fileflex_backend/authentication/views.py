from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from supabase_py import supabase

@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Please provide email and password'}, status=400)
    
    try:
        user = supabaseClient.auth.sign_up(email=email, password=password)
        return Response({'user': user}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = supabaseClient.auth.sign_in(email=email, password=password)
        return Response({'user': user})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        user = request.user
        if user:
            data = {
                'id': user.id,
                'email': user.email,
            }
            return Response(data)
        else:
            return Response({'error': 'User not found'}, status=404)
    elif request.method == 'PUT':
        user = request.user
        if user:
            email = request.data.get('email')
            
            if email and email != user.email:
                try:
                    user.email = email
                    user.save()
                    return Response({'message': 'Profile updated successfully', 'user': {'id': user.id, 'email': user.email}})
                except Exception as e:
                    return Response({'error': str(e)}, status=400)
            else:
                return Response({'message': 'No changes to update'})
        else:
            return Response({'error': 'User not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        supabaseClient.auth.sign_out()
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)