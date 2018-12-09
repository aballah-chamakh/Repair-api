from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets,permissions,generics,pagination,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Offer,Profile
from accounts.models import User
from .serializers import * #OfferSerializer,ProfileSerializer,UserSerializer
from .permissions import *
from .paginations import OfferPagination
# Create your views here.
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    #permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        query =self.queryset.filter(id=self.request.user.id)
        return query
    @action(methods=['PUT'],detail=True)
    def set_password(self,request,pk):
        user = self.get_object() # to be sure that assigned permissions are checked
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid() :
            old_password = serializer.data.get('old_password')
            if not user.check_password(old_password) :
                return Response({'valid':False,'msg':'invalid old password'},status=status.HTTP_400_BAD_REQUEST)
            else :
                new_password = serializer.data.get('new_password')
                user.set_password(new_password)
                user.save()
                return Response({'valid':True,'msg':'the password updated successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['GET'],detail=True)
    def reset_name(self,request,pk):
        user = self.get_object()
        newName = self.request.GET.get('username')
        user.username = newName
        user.save()
        return Response({'msg':'your name was reseted successfully'},status=status.HTTP_200_OK)

class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permissions = (IsOwnerOrReadOnly,)
    @action(methods=['PUT'],detail=True)
    def reset_image(self, request, pk):
        profile_obj = self.get_object()
        profile_obj.image = request.data.get('image')
        profile_obj.save()
        return Response({'status': 'profile image was updated'},status=status.HTTP_200_OK)
    @action(methods=['PUT'],detail=True)
    def reset_info(self,request,pk):
        profile_obj = self.get_object()
        username = request.data.get('username')
        print(username)
        about = request.data.get('about')
        print(about)
        phone = request.data.get('phone')
        print(phone)
        user_obj = profile_obj.user
        user_obj.username = username
        user_obj.save()
        profile_obj.about = about
        profile_obj.phone = phone
        profile_obj.save()
        print('after update')
        print(user_obj.username)
        print(profile_obj.phone)
        return Response({'msg': 'profile info was updated'},status=status.HTTP_200_OK)



class OfferView(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    #permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = OfferPagination

    def get_queryset(self):
        search = self.request.GET.get('search')
        categorie = self.request.GET.get('cat')
        offers = Offer.objects.all()
        if (categorie is not None):
            if (categorie != 'all categories'):
                offers = Offer.objects.filter(categorie=categorie)
            if (search is not None and search != ''):
                offers = offers.filter(Q(description__icontains=search) |
                               Q(title__icontains=search) |
                               Q(profile__user__username__icontains=search)).distinct()


        return  offers
    def perform_create(self,serializer):
        serializer.save(profile=self.request.user.profile)


    @action(methods=['GET'],detail=True)
    def toogle_like(self,request,pk):
        offer_obj  = self.get_object()
        user_obj = request.user
        if offer_obj.likes.all().count() == 0 :
            if user_obj  :
                    offer_obj.likes.add(user_obj)
                    serializer = SimpleUserSerializer(offer_obj.likes.all(),many=True,context={'request':self.request})
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
        else :
            if user_obj  :
                action = 'add'
                if user_obj in offer_obj.likes.all() :
                    action = 'remove'
                if action == 'add' :
                    offer_obj.likes.add(user_obj)
                    serializer = SimpleUserSerializer(offer_obj.likes.all(),many=True,context={'request':self.request})
                    print(user_obj.username+' like added')
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
                elif action == 'remove':
                    offer_obj.likes.remove(user_obj)
                    serializer = SimpleUserSerializer(offer_obj.likes.all(),many=True,context={'request':self.request})
                    print(user_obj.username+' like removed')
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
            else :
                return Response({'msg':'anonymos user'},status=status.HTTP_400_BAD_REQUEST)





class SimpleProfileView(generics.RetrieveAPIView):
    serializer_class = SimpleProfileSerializer
    queryset = Profile.objects.all()

class UpdatePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdatePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,PasswordOwner)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid() :
            user = self.get_object()
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CommentResponseView(viewsets.ModelViewSet):
    serializer_class = CommentResponseSerializer
    queryset = CommentResponse.objects.all()
    def perform_create(self,serializer):
        print('here')
        comment_id = self.request.GET.get('comment_id')
        comment_obj = Comment.objects.get(id = comment_id)
        user_obj = None
        if self.request.user.is_authenticated :
            user_obj = self.request.user
            print(user_obj.username)
        print(user_obj)
        serializer.save(comment=comment_obj,owner=user_obj)
    @action(methods=['POST'],detail=True)
    def update_res_comment(self,request,pk):
        res_comment_obj = self.get_object()
        content = request.data.get('content')
        res_comment_obj.content = content
        res_comment_obj.save()
        return Response({'msg':'successfully the response comment updated'},status=status.HTTP_200_OK)

    @action(methods=['GET'],detail=True)
    def toogle_like(self,request,pk):
        print(pk)
        res_comment_obj  = CommentResponse.objects.get(id=pk)
        user_obj = request.user
        if res_comment_obj.likes.all().count() == 0 :
            if user_obj  :
                    res_comment_obj.likes.add(user_obj)
                    serializer = SimpleUserSerializer(res_comment_obj.likes.all(),many=True,context={'request':self.request})
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
        else :
            if user_obj  :
                action = 'add'
                if user_obj in res_comment_obj.likes.all() :
                    action = 'remove'
                if action == 'add' :
                    res_comment_obj.likes.add(user_obj)
                    serializer = SimpleUserSerializer(res_comment_obj.likes.all(),many=True,context={'request':self.request})
                    print(user_obj.username+' like added')
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
                elif action == 'remove':
                    res_comment_obj.likes.remove(user_obj)
                    serializer = SimpleUserSerializer(res_comment_obj.likes.all(),many=True,context={'request':self.request})
                    print(user_obj.username+' like removed')
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
            else :
                return Response({'msg':'anonymos user'},status=status.HTTP_400_BAD_REQUEST)

class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    @action(methods=['POST'],detail=True)
    def update_comment(self,request,pk):
        comment_obj = self.get_object()
        content = request.data.get('content')
        comment_obj.content = content
        comment_obj.save()
        return Response({'msg':'successfully the comment updated'},status=status.HTTP_200_OK)
    @action(methods=['GET'],detail=True)
    def toogle_like(self,request,pk):
        comment_obj  = Comment.objects.get(id=pk)
        user_obj = request.user
        if comment_obj.likes.all().count() == 0 :
            if user_obj  :
                    comment_obj.likes.add(user_obj)
                    serializer = SimpleUserSerializer(comment_obj.likes.all(),many=True,context={'request':self.request})
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
        else :
            if user_obj  :
                action = 'add'
                if user_obj in comment_obj.likes.all() :
                    action = 'remove'
                if action == 'add' :
                    comment_obj.likes.add(user_obj)
                    serializer = SimpleUserSerializer(comment_obj.likes.all(),many=True,context={'request':self.request})
                    print(user_obj.username+' like added')
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
                elif action == 'remove':
                    comment_obj.likes.remove(user_obj)
                    serializer = SimpleUserSerializer(comment_obj.likes.all(),many=True,context={'request':self.request})
                    print(user_obj.username+' like removed')
                    return Response({'likes':serializer.data},status=status.HTTP_200_OK)
            else :
                return Response({'msg':'anonymos user'},status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        offer_id = self.request.GET.get('offer_id')
        print(offer_id)
        comments = Comment.objects.all()
        if offer_id is not None :
            offer_obj = Offer.objects.get(id=offer_id)
            comments = comments.filter(product=offer_obj)
        return comments
    def perform_create(self,serializer):
        offer_id = self.request.GET.get('offer_id')
        print(offer_id)
        offer_obj = None
        if offer_id :
            offer_obj = Offer.objects.get(id = offer_id)
        owner = None
        if self.request.user.is_authenticated :
            owner = self.request.user
        serializer.save(owner=owner,product=offer_obj)
