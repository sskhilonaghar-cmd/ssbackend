from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Product, Order, GalleryImage
from .serializers import ProductSerializer, OrderSerializer, GalleryImageSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # allow anyone to post order, then include a whatsapp link in the response
        response = super().create(request, *args, **kwargs)
        try:
            order_id = response.data.get('id')
            order = Order.objects.get(id=order_id)
            from urllib.parse import quote
            msg = quote(f"New order #{order.id}: {order.product.name} x{order.quantity} for {order.customer_name} ({order.phone})\nAddress: {order.address}")
            response.data['whatsapp_url'] = f"https://wa.me/917897391004?text={msg}"
        except Exception:
            pass
        return response

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['pending', 'delivered', 'cancelled']:
            return Response(
                {'error': 'Invalid status. Must be pending, delivered, or cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)


class GalleryImageViewSet(viewsets.ModelViewSet):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer

    def get_permissions(self):
        # public readers only
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # modification endpoints require authenticated staff member
        perm = permissions.IsAuthenticated()
        return [perm]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only staff may upload gallery images.')
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only staff may modify gallery images.')
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only staff may delete gallery images.')
        instance.delete()


@api_view(['POST'])
def admin_login(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # require staff for admin portal
    if not user.is_staff:
        return Response(
            {'error': 'User is not an admin.'},
            status=status.HTTP_403_FORBIDDEN
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'username': user.username,
    })
