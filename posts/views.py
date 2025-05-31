from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from geopy.geocoders import Nominatim


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def _process_geolocation(self, location_name, latitude, longitude):
        # Обработка геолокации
        try:
            geolocator = Nominatim(user_agent="social_network")
            
            # Если есть город, получить координаты
            if location_name and (not latitude or not longitude):
                location = geolocator.geocode(location_name)
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    
            # Если есть координаты, получить город
            elif latitude and longitude and not location_name:
                location = geolocator.reverse((latitude, longitude))
                if location:
                    location_name = location.address
                    
        except Exception:
            # если ошибка просто продолжить с теми же данными
            pass
            
        return location_name, latitude, longitude

    def perform_create(self, serializer):
        location_name = self.request.data.get('location_name')
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        
        # координаты --> числа
        if latitude:
            try:
                latitude = float(latitude)
            except (ValueError, TypeError):
                latitude = None
                
        if longitude:
            try:
                longitude = float(longitude)
            except (ValueError, TypeError):
                longitude = None

        # Обработка геолокации
        location_name, latitude, longitude = self._process_geolocation(
            location_name, latitude, longitude
        )

        serializer.save(
            author=self.request.user,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )

    def perform_update(self, serializer):
        location_name = self.request.data.get('location_name')
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        
        # если новых данных нет пользовать те что есть
        instance = serializer.instance
        if location_name is None:
            location_name = instance.location_name
        if latitude is None:
            latitude = instance.latitude
        if longitude is None:
            longitude = instance.longitude
            
        # координаты -> числа
        if latitude:
            try:
                latitude = float(latitude)
            except (ValueError, TypeError):
                latitude = instance.latitude
                
        if longitude:
            try:
                longitude = float(longitude)
            except (ValueError, TypeError):
                longitude = instance.longitude

        # обработка геолокации если данные изменились
        if (location_name != instance.location_name or 
            latitude != instance.latitude or 
            longitude != instance.longitude):
            location_name, latitude, longitude = self._process_geolocation(
                location_name, latitude, longitude
            )

        serializer.save(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Вы уже ставили лайк.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Лайк поставлен.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted:
            return Response({'detail': 'Лайк удалён.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Лайка не было.'}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        
        if not post_id:
            raise serializers.ValidationError({'post': 'Поле post заполнить обязательно.'})
            
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({'post': 'Пост с этим ID не найден.'})
            
        serializer.save(author=self.request.user, post=post)