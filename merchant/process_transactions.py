from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from system_user.models import CustomerInfo
from .serializers import ProcessingTransactionSerializer
from .models import MerchantBuyingRate
from site_transactions.models import GeneralTransaction


class ProcessTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ProcessingTransactionSerializer,
        responses={
            200: OpenApiResponse(description="Transaction Processed"),
            400: OpenApiResponse(description="Unable to process transaction or Invalid transaction")
        }
    )
    def post(self, request):
        serializer = ProcessingTransactionSerializer(data=request.data)
        if serializer.is_valid():
            buyers_quantity = serializer.validated_data['buyers_quantity']
            payment_method = serializer.validated_data['payment_method']
            merchant_id = serializer.validated_data['merchant_id']
            buyers_currency = serializer.validated_data['trading_currency']
            buyers_old_wallet_balance = request.user.wallet_balance

            # Ensure no negative or zero quantity for buyer
            if buyers_quantity <= 0:
                return Response({"message": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Fetch the authenticated user (buyer)
                user = CustomerInfo.objects.get(email=request.user.email)

                # Fetch the merchant and the related MerchantBuyingRate in one query
                merchant = CustomerInfo.objects.prefetch_related(
                    'merchantbuyingrate_set'  # Pre-fetch related MerchantBuyingRate for this merchant
                ).get(pk=merchant_id)

            except CustomerInfo.DoesNotExist:
                return Response({"message": "User or Merchant not found."}, status=status.HTTP_404_NOT_FOUND)

            # Lock both the buyer's and merchant's wallet rows to prevent concurrent access
            with transaction.atomic():  # Start atomic block

                # Lock the buyer and merchant wallets for update
                user = CustomerInfo.objects.select_for_update().get(email=request.user.email)
                merchant = CustomerInfo.objects.select_for_update().get(pk=merchant_id)
                # Now you can access the merchant's buying rates
                get_trading_currency = merchant.merchantbuyingrate_set.filter(currency=buyers_currency).first()
                if not get_trading_currency:
                    return Response({"message": "No buying rate found for this merchant."},
                                    status=status.HTTP_404_NOT_FOUND)

                # Check if buyer's and merchant's wallet balances are valid (non-negative)
                if user.wallet_balance < 0:
                    return Response({"message": "User wallet balance is negative, please contact support."}, status=status.HTTP_400_BAD_REQUEST)
                elif 0 > user.wallet_balance:
                    return Response({"message": "Insufficient Wallet Balance To Process Transaction"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif 0 > buyers_quantity:
                    return Response({"message": "Insufficient Wallet Balance To Process Transaction"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif merchant.wallet_balance < 0:
                    return Response({"message": "Merchant wallet balance is negative, please contact support."}, status=status.HTTP_400_BAD_REQUEST)
                elif 0 > merchant.wallet_balance:
                    return Response({"message": "Merchant wallet balance is negative, please contact support."}, status=status.HTTP_400_BAD_REQUEST)

                # Get the merchant's currency, buying rate, and available quantity for sale
                currency = get_trading_currency.currency
                merchant_buying_rate = get_trading_currency.buying_rate
                quantity_available_for_sale = get_trading_currency.quantity_available_for_sale
                merchant_wallet_balance = merchant.wallet_balance  # Assuming you have this field
                merchant_old_wallet_balance = merchant.wallet_balance
                # Calculate amount to credit buyer's local account
                amount_to_credit_buyers_local_account = 0
                if buyers_quantity <= quantity_available_for_sale:
                    amount_to_credit_buyers_local_account = buyers_quantity * merchant_buying_rate
                else:
                    amount_to_credit_buyers_local_account=quantity_available_for_sale *merchant_buying_rate

                # Check if the buyer has enough funds based on the currency and rate
                if payment_method == 0:
                    # Ensure buyer's wallet has enough balance
                    if user.wallet_balance < buyers_quantity:
                        return Response({"message": "Insufficient Wallet Balance To Process Transaction"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # Ensure merchant has enough balance for transaction
                    if merchant_wallet_balance < amount_to_credit_buyers_local_account:
                        return Response({"message": "Merchant has insufficient wallet balance to complete transaction"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif 0 > amount_to_credit_buyers_local_account:
                        return Response({"message": "Amount Procssed is invalid"},                                        status=status.HTTP_400_BAD_REQUEST)


                    # Check if the merchant has enough quantity available for sale
                    quantity_re_available_for_sale = quantity_available_for_sale
                    if buyers_quantity > quantity_available_for_sale:
                        quantity_available_for_sale = 0
                    else:
                        quantity_available_for_sale -= buyers_quantity

                    # Update the merchant's stock with the new quantity
                    get_trading_currency.quantity_available_for_sale = quantity_available_for_sale
                    get_trading_currency.save()

                    # Debit the buyer's wallet
                    if quantity_available_for_sale == 0:
                        user.wallet_balance -= quantity_re_available_for_sale
                    #Debit the amount if the buyers currency is less than merhcnt avaialable quanityt
                    else:
                        user.wallet_balance -= buyers_quantity
                    user.save()

                    # Debit the merchant's wallet (by the same amount that is credited to the buyer)
                    merchant.wallet_balance -= amount_to_credit_buyers_local_account
                    merchant.save()
                    #Create Transaction History
                    transaction = GeneralTransaction.objects.create(
                        buyer=request.user,
                        merchant=merchant,
                        buyer_currency_exchange=buyers_currency,
                        merchant_currency_exchange=currency,
                        buyer_paid=buyers_quantity,
                        merchant_paid=amount_to_credit_buyers_local_account,
                        buyer_previous_balance=buyers_old_wallet_balance,
                        buyer_new_balance=request.user.wallet_balance,
                        merchant_previous_balance=merchant_old_wallet_balance,
                        merchant_new_balance=merchant.wallet_balance,
                        buyer_payment_type="Wallet Payment",
                        is_transaction_successful=True,  # Set to True if the transaction is successful
                        transaction_response="transaction_response",
                    )


                    # Further logic for creating buyer's local account or processing wallet update
                    # (This part depends on your specific business logic)

                elif payment_method == 1:
                    # ToDo Process card payment (implement card verification or debiting logic here)
                    pass

                # Return a success message
                return Response({"message": "Transaction processed successfully."}, status=status.HTTP_200_OK)

        # If the serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


