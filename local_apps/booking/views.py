import requests
import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, Count, Sum, IntegerField, When
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import requests
from . serializers import *
from .filters import *
from .resources import *
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

today = datetime.now().date()

# vendor Side List


# @method_decorator(cache_page(60 * 15), name='dispatch')
class AdminBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "booking_id",
        "service__name",
        "user__first_name",
        "user__last_name"
    ]
    filterset_class = BookingFilter

# Individual Booking For Admin CMS


class AdminIndividualBookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'


# @method_decorator(cache_page(60 * 15), name='dispatch')
class VendorBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "booking_id",
        "service__name",
        "user__first_name",
        "user__last_name"
    ]
    filterset_class = BookingFilter

    def get_queryset(self):
        try:
            return Booking.objects.filter(service__company__user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(cache_page(60 * 15), name='dispatch')
class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.all()
        try:
            return Booking.objects.filter(user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()  # saving the booking instance
        return instance

    def create(self, request, *args, **kwargs):
        ''' Overriding the create method for payment initialization'''
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            booking_instance = self.perform_create(serializer)

            # payment initialization

            api_key = settings.TAP_API_KEY
            base_url = settings.TAP_BASE_URL
            secret_key = settings.TAP_SECRET_KEY

            total_amount = getattr(booking_instance, "price_total", 0)
            user_first_name = getattr(
                booking_instance.user, "first_name", "No First Name")
            user_last_name = getattr(
                booking_instance.user, "last_name", "No Last Name")
            user_email = getattr(booking_instance.user,
                                 "email", "default_email")
            user_mobile = getattr(booking_instance.user, "mobile", 0000000000)

            url = base_url + "authorize/"
            total_amount = booking_instance.price_total
            payload = {
                "amount": total_amount,
                "currency": "KWD",
                "metadata": {
                    "udf1": "Sea Arabia TXN ID",
                    "udf2": "Service Name",
                    "udf3": "Service Category",
                },
                "customer": {
                    "first_name": user_first_name,
                    "middle_name": "",
                    "last_name": user_last_name,
                    "email": user_email,
                    "phone": {
                        "country_code": "+965",
                        "number": user_mobile
                    }
                },
                "merchant": {"id": "1234"},
                "source": {"id": "src_all"},
                "redirect": {"url": "http://your_website.com/redirecturl"}
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": "Bearer "+secret_key
            }

            response = requests.post(url, json=payload, headers=headers)

            authorize_response = response.json()

            # get the url for checkout from the json response

            payment_url = authorize_response.get("transaction")['url']
            tap_id = authorize_response.get("id", None)
            payment_status = authorize_response.get("status", None)

            payment_instance = Payment.objects.create(tap_pay_id=tap_id,
                                                      initial_response=authorize_response, amount=total_amount, status=payment_status)

            booking_instance.payment = payment_instance
            booking_instance.save()

            serializer = BookingSerializer(booking_instance)
            serialized_data = dict(serializer.data)
            serialized_data['payment_url'] = payment_url
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class BookingView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class BookingStatusUpdate(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    queryset = Booking.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            booking_status = request.data.get('status', None)
            allowed_statuses = [data[0] for data in Booking.BOOKING_STATUS]
            if booking_status not in allowed_statuses:
                raise serializers.ValidationError(
                    f"Invalid booking status. Allowed statuses are: {', '.join(allowed_statuses)}")
            booking_id = kwargs.get('pk', None)
            booking_instance = get_object_or_404(Booking, id=booking_id)
            if booking_status:
                booking_instance.status = booking_status if booking_status else None
                booking_instance.save()
            return Response({"message": f"Booking status changes : {booking_instance.status}"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error : {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class AdminBookingCardCount(APIView):
    """ Booking card count for admin cms """

    def get(self, request):
        """ fetching the count of all booking """
        try:

            booking_count = Booking.objects.all().aggregate(
                total_booking=Count("pk"),
                today_booking=Coalesce(Sum(
                    Case(When(created_at=today, then=1), default=0, output_field=IntegerField())), 0),
                total_confirmed_booking=Coalesce(Sum(
                    Case(When(status="Successful", then=1), default=0, output_field=IntegerField())), 0),
                total_cancelled_booking=Coalesce(Sum(
                    Case(When(status="Cancelled", then=1), default=0, output_field=IntegerField())), 0),
            )

            return Response(booking_count, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error:{str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ExportBooking(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Booking.objects.all()
        resource = BookingResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings_list.csv"'
        return response


class BookingCancellation(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            booking_id = kwargs.get('pk', None)
            cancellation_reason = request.data.get('cancellation_reason')
            booking_instance = Booking.objects.get(
                id=booking_id) if Booking.objects.filter(id=booking_id).exists() else None

            if booking_instance and booking_instance.status != 'Cancelled':
                booking_instance.cancelled_by = self.request.user
                booking_instance.status = 'Cancelled'
                booking_instance.cancellation_reason = cancellation_reason
                booking_instance.refund_status = 'Pending'
                booking_instance.save()
            else:
                return Response({"error": "Booking is al@method_decorator(cache_page(60 * 15), name='dispatch') ready cancelled."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"Booking Status": booking_instance.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InitializeRefund(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            booking_id = kwargs.get('pk', None)
            refund_amount = request.data.get('refund_amount')
            refund_details = request.data.get('refund_details')
            refund_type = request.data.get('refund_type')
            booking_instance = Booking.objects.get(
                id=booking_id) if Booking.objects.filter(id=booking_id).exists() else None

            if booking_instance and booking_instance.refund_status == 'Pending':
                # Store logged-in user details in JSON format
                user_details = {
                    "user_id": str(self.request.user.id),
                    "username": self.request.user.username,
                    "account_id":self.request.user.account_id,
                    "email": self.request.user.email,
                    "mobile":self.request.user.mobile,
                    "role":self.request.user.role,

                    # Add more user details as needed
                }

                booking_instance.refunded_by = user_details
                booking_instance.is_refunded = True
                booking_instance.refund_status = 'Completed'
                booking_instance.refund_details = refund_details
                booking_instance.refund_amount = refund_amount
                booking_instance.refund_type = refund_type
                booking_instance.save()
            else:
                return Response({"error": "Refund is Alredy Processed."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"Booking Status": booking_instance.refund_status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

# class InitializeRefund(generics.UpdateAPIView):
#     serializer_class = BookingStatusSerializer
#     queryset = Booking.objects.all()
#     permission_classes = [IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         try:
            
#             refund_amount = request.data.get('refund_amount')
#             refund_details = request.data.get('refund_details')
#             refund_type = request.data.get('refund_type')
#             booking_instance = self.get_object()

#             if booking_instance.refund_status == 'Pending':
#                 booking_instance.refunded_by = self.request.user
#                 booking_instance.is_refunded = True
#                 booking_instance.refund_status = 'Completed'
#                 booking_instance.refund_details = refund_details
#                 booking_instance.refund_amount = refund_amount
#                 booking_instance.refund_type = refund_type
#                 booking_instance.save()
#             else:
#                 return Response({"error": "Booking is already refunded."}, status=status.HTTP_400_BAD_REQUEST)

#             return Response({"Booking Refund Status": booking_instance.refund_status}, status=status.HTTP_200_OK)
#         except Booking.DoesNotExist:
#             return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class PaymentFinalization(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            payment_id = request.data.get("payment_id")
            if payment_id:
                url = "https://api.tap.company/v2/authorize/"+payment_id

                headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer "+settings.TAP_SECRET_KEY
                }
                response = requests.get(url, headers=headers)
                final_response = response.json()
                #! remove the redirect and post url from the response to avoid any security issues
                del final_response['redirect']
                # del final_response['post']

                # ? updating the payement status and booking status
                payment_status = final_response.get("status", None)
                payment_instance = Payment.objects.get(tap_pay_id=payment_id)
                payment_instance.status = payment_status
                payment_instance.confirmation_response = final_response
                payment_instance.save()
                return Response(final_response, status=status.HTTP_200_OK)
            else:
                return Response("Payment Id Required", status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(f'Error {str(e)}', status=status.HTTP_400_BAD_REQUEST)


class VendorBookingCardCount(APIView):
    def get(self, request):
        """ passing the vendor id retrive the count of booking associated with the vendor only  """

        try:
            vendor_id = request.query_params.get('id', None)
            if vendor_id:
                booking_count = Booking.objects.filter(service__company__user=vendor_id).aggregate(
                    total_booking=Count("pk"),
                    today_booking=Coalesce(Sum(
                        Case(When(created_at=today, then=1), default=0, output_field=IntegerField())), 0),
                    total_confirmed_booking=Coalesce(Sum(
                        Case(When(status="Successful", then=1), default=0, output_field=IntegerField())), 0),
                    total_cancelled_booking=Coalesce(Sum(
                        Case(When(status="Cancelled", then=1), default=0, output_field=IntegerField())), 0),
                )
                return Response(booking_count, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)
