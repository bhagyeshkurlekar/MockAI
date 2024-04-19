from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer, ConversationSerializer
from .models import CanvasUser, Conversation
from .utils import user_detail
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
import openai
import base64

openai_api_key = 'your-api-key'
openai.api_key = openai_api_key


def ask_openai(applicant_request=None, applicant_diagram=None):
    if applicant_diagram is not None and applicant_request is not None:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What'\''s in this image? and tell me if this text links with the image " + str(
                            applicant_request)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(applicant_diagram.read()).decode('utf-8')}", "detail":  "high"
                        }
                    }
                ]
            }
        ]
    elif applicant_diagram is not None and applicant_request is None:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What'\''s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{base64.b64encode(applicant_diagram.read()).decode('utf-8')}", "detail": "high"
                        }
                    }
                ]
            }
        ]

    elif applicant_diagram is None and applicant_request is not None:
        messages = [
              {
                "role": "system",
                "content": "You are a helpful assistant."
              },
              {
                "role": "user",
                "content": str(applicant_request)
              }
        ]
    else:
        return "Invalid"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=300
    )

    print(response)
    answer = response.choices[0].message.content.strip()
    return answer


class RegisterViewset(viewsets.ModelViewSet):
    queryset = CanvasUser.objects.all()
    serializer_class = RegisterSerializer

    def post_register(self, request):
        email = request.data.get("email")
        queryset = CanvasUser.objects.filter(email=email)
        if queryset is not None and len(queryset) > 0:
            return Response(status=status.HTTP_409_CONFLICT, data={"User already registered."})

        ser = RegisterSerializer(
            data=request.data, context={'request': request}
        )
        if ser.is_valid():
            try:
                user = ser.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                response = user_detail(user)
                return Response(response, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(
                    {'reason': "Invalid Login"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
        return Response(
            {'reason': ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginViewset(viewsets.ModelViewSet):
    queryset = CanvasUser.objects.all()
    serializer_class = LoginSerializer

    def post_login(self, request):
        ser = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if ser.is_valid(raise_exception=True):
            user = ser.validated_data['user']
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                response = user_detail(user)
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"Login Failed! Please Try again"})


class ConversationViewset(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def post_question(self, request):
        queryset = Conversation.objects.all()
        data = request.data

        if "applicant_diagram" in data and "applicant_request" in data:
            ai_response = ask_openai(applicant_request=data["applicant_request"], applicant_diagram=data["applicant_diagram"])
        elif "applicant_diagram" not in data and "applicant_request" in data:
            ai_response = ask_openai(applicant_request=data["applicant_request"])
        elif "applicant_request" not in data and "applicant_diagram" in data:
            ai_response = ask_openai(applicant_diagram=data["applicant_diagram"])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer_data = {
            "applicant": request.user.id,
            "applicant_request": data["applicant_request"] if "applicant_request" in data else None,
            "ai_response": ai_response,
            "applicant_diagram": data["applicant_diagram"] if "applicant_diagram" in data else None,
            "applicant_audio": data["applicant_audio"] if "applicant_audio" in data else None
        }
        print(serializer_data)
        serializer = ConversationSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_conversation(self, request):
        queryset = Conversation.objects.filter(applicant_id=request.user.id)
        serializer = ConversationSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)






