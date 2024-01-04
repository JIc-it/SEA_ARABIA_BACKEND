from import_export import resources, fields
from import_export.widgets import *
from .models import Booking
from local_apps.account.models import User, Guest


class BookingResource(resources.ModelResource):
    user_first_name = fields.Field(
        column_name='first_name',
        attribute='user__first_name',
        widget=ForeignKeyWidget(User, field='first_name'))

    user_last_name = fields.Field(
        column_name='last_name',
        attribute='user__last_name',
        widget=ForeignKeyWidget(User, field='last_name'))

    user_email = fields.Field(
        column_name='user_email',
        attribute='user__email',
        widget=ForeignKeyWidget(User, field='email'))

    user_mobile = fields.Field(
        column_name='user_mobile',
        attribute='user__mobile',
        widget=ForeignKeyWidget(User, field='mobile'))

    guest_first_name = fields.Field(
        column_name='guest_first_name',
        attribute='guest__first_name',
        widget=ForeignKeyWidget(Guest, field='first_name'))

    guest_last_name = fields.Field(
        column_name='guest_last_name',
        attribute='guest__last_name',
        widget=ForeignKeyWidget(Guest, field='last_name'))
    guest_mobile = fields.Field(
        column_name='guest_mobile',
        attribute='guest__mobile',
        widget=ForeignKeyWidget(User, field='mobile'))
    guest_email = fields.Field(
        column_name='guest_email',
        attribute='guest__email',
        widget=ForeignKeyWidget(User, field='email'))

    class Meta:
        model = Booking
        fields = ['id',
                  'user_first_name',
                  'user_last_name',
                  'user_email',
                  'user_mobile',
                  'guest_first_name',
                  'guest_last_name',
                  'guest_email',
                  'guest_mobile',
                  'guest',
                  'offer',
                  'service',
                  'payment',
                  'package',
                  'price',
                  'user_type',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'email',
                  'destination',
                  'booking_for',
                  'booking_item',
                  'starting_point',
                  'start_date',
                  'end_date',
                  'slot_details',
                  'number_of_people',
                  'booking_type',
                  'status',
                  'cancellation_reason',
                  'cancelled_by',
                  'refund_status',
                  'refund_type',
                  'refund_amount',
                  'refund_details',
                  'price_total',
                  'created_at',
                  'updated_at'
                  ]

        export_order = fields
