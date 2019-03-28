from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth import authenticate

from .models import Poll, Choice
from .serializers import PollsSerializer, ChoiceSerializer, VoteSerializer, UserSerilaizer

# using APIVIEW
# class PollsList(APIView):
#     def get(self,request):
#         polls = Poll.objects.all()
#         data = PollsSerializer(polls, many=True).data
#         return Response(data, status=status.HTTP_200_OK)



# class PollsDetail(APIView):
#     def get(self,request, pk):
#         polls = get_object_or_404(Poll, pk=pk)
#         data = PollsSerializer(polls).data
#         return Response(data,status=status.HTTP_200_OK)

#using generics

# class PollsList(generics.ListCreateAPIView):
#     queryset= Poll.objects.all()
#     serializer_class = PollsSerializer

# class PollsDetail(generics.RetrieveDestroyAPIView):
#     queryset= Poll.objects.all()
#     serializer_class = PollsSerializer

class PollsViewset(viewsets.ModelViewSet):
    queryset= Poll.objects.all()
    serializer_class = PollsSerializer

    def destroy(self, request,):
        instance =  self.get_object()
        user_id =  request.user.id
        created_by = self.get_object().created_by.id
        if  user_id == created_by  :
            instance.delete()
            return Response({"message":"Successfully deleted","success":True},status=status.HTTP_200_OK)
        else:
            return Response({"error":True,"message":"you cannot delete this poll"},status=status.HTTP_403_FORBIDDEN)



class ChoicesList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self,request, *args, **kwargs):
        instance =  self.get_object()
        if instance.poll.created_by.id == request.user.id:
            data ={
                'choice_text':request.data.get('choice_text'),
                'poll':self.kwargs.get('pk')
            }
            serializer= ChoiceSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('No permission to create choices', status=status.HTTP_201_CREATED)

class CreateVote(APIView):
    def post(self, request, pk ,choice_pk):
        data = {
            'voted_by':request.data.get('voted_by'),'poll':pk,'choice':choice_pk
        }
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUser(generics.CreateAPIView):
    authentication_classes =()
    permission_classes = ()
    serializer_class = UserSerilaizer

class LoginView(APIView):
    authentication_classes =()
    permission_classes = ()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token":user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)

