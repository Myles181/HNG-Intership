from urllib import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, OrganisationSerializer
import random


@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['userId'] = str(random.randint(1000, 9999))
        print(data)

        serializer = UserRegisterSerializer(data=data)
        print(serializer.is_valid())

        if serializer.is_valid():
            try:
                user = serializer.save()
                organisation = Organisation.objects.create(orgId=serializer.data['userId'], name=f"{serializer.data['firstName']}'s Organisation")
                organisation.users.add(user)
                token = RefreshToken.for_user(user)
                user_data = UserSerializer(user).data

                response_data = {
                    "status": "success",
                    "message": "Registration successful",
                    "data": {
                        "accessToken": str(token.access_token),
                        "user": user_data
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"response: {e}")
                response = {
                    "status": "Bad request",
                    "message": f"Registration unsuccessful: {str(e)}",
                    "statusCode": 400
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            errors = [
                {"field": key, "message": value[0]} 
                for key, value in serializer.errors.items()
            ]
            response = {
                "errors": errors
            }
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        response_data = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": str(token.access_token),
                "user": UserSerializer(user).data
            }
        }
        # print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        data = {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            }
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_view(request, id):
    serializer = UserSerializer(request.user)
    response_data = {
        "status": "success",
        "message": "User Detail!",
        "data": serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def organisation_list_create_view(request):
    if request.method == 'GET':
        # Authenticated user can get all organisations they're in
        organisations = request.user.organisations.all()
        response_data = {
            "status": "success",
            "message": "Organisations!",
            "data": {
                "organisations": OrganisationSerializer(organisations, many=True).data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Authenticated user can create organisations
        request.data['orgId'] = User.objects.get(id=request.user.id).userId
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            data = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": {
                    "orgId": serializer.data['orgId'], 
                    "name": serializer.data['name'], 
				    "description": serializer.data['description']
                    }
                }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
                }
            return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organisation_detail_view(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId, users=request.user)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Organisation.DoesNotExist:
        return Response({"status": "Not Found", "message": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_user_to_organisation_view(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
        user_id = request.data.get("userId")
        user = User.objects.get(userId=user_id)
        organisation.users.add(user)
        return Response({"status": "success", "message": "User added to organisation successfully"}, status=status.HTTP_200_OK)
    except Organisation.DoesNotExist:
        return Response({"status": "Bad Request", "message": "Organisation not found"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"status": "Bad Request", "message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

