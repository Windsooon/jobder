import stripe
from django.http import HttpResponse
from django.db import transaction
from jobs.set_logging import setup_logging
from .const import STRIPE_API_KEY, PLAN_ID
from .models import Customer

init_logging = setup_logging()
logger = init_logging.getLogger(__name__)
stripe.api_key = STRIPE_API_KEY


def subscription(user, customer, post_id):
    '''
    Customer subscribe a plan
    '''
    try:
        customer_id = customer['id']
        customer_data = customer['sources']['data'][0]
        response = stripe.Subscription.create(
            customer=customer_id,
            items=[
              {
                "plan": PLAN_ID,
              },
            ],
            metadata={'post_id': post_id},
        )
    except stripe.error.CardError as e:
        logger.error(
            'Subscription Card failed. customer_id is {0}'.
            format(customer_id))
        logger.error(e)
        return HttpResponse(
            'Something wrong with your card. Please check your input.',
            status=400)
    except stripe.error.AuthenticationError as e:
        logger.error(
            'Subscription Auth failed. customer_id is {0}'
            .format(customer_id))
        logger.error(e)
        return HttpResponse(
            'Something wrong with stripe authentication.', status=400)
    except stripe.error.InvalidRequestError as e:
        logger.error(
            'Subscription failed. customer_id is {0}'.format(customer_id))
        logger.error(e)
        return HttpResponse(
            'Something wrong with subscription.' +
            'Please email contact@osjobs.net', status=400)
    except Exception as e:
        logger.error(e)
        return HttpResponse(
            'Unknown issue. Please email contact@osjobs.net', status=400)
    else:
        with transaction.atomic():
            obj, created = Customer.objects.update_or_create(
                post_id=post_id,
                defaults={
                    'cus_id': customer['id'],
                    'sub_id': response['id'],
                    'settings_id': user.settings.user_id,
                    'stripe_name': customer_data['name'],
                    'stripe_email': customer['email'],
                    'stripe_zip': customer_data['address_zip'],
                    'stripe_last4': str(customer_data['last4']),
                    'stripe_exp_month': customer_data['exp_month'],
                    'stripe_exp_year': customer_data['exp_year']})
        return HttpResponse(
            'Succeed, thank you for using Open Source Jobs.', status=200)


def create_customer_and_subscribe(user, data):
    '''
    Create customer from user submit data
    '''
    # import pdb; pdb.set_trace()
    try:
        customer = stripe.Customer.create(
            description='Customer for ' + data['card']['name'],
            email=data['email'],
            source=data['token'],
        )
    except stripe.error.CardError as e:
        logger.error(
            'Customer create failed. Card id {0} from {1} may have problem.'
            .format(data['card']['id'], data['card']['name']))
        logger.error(e)
        return HttpResponse(
            'Something wrong with your card. Please try another card.',
            status=400)
    except stripe.error.AuthenticationError as e:
        logger.error(e)
        return HttpResponse(
            'Something wrong with stripe authentication.', status=400)
    except stripe.error.InvalidRequestError as e:
        logger.error(e)
        return HttpResponse(
            'Something wrong with stripe request.', status=400)
    return subscription(user, customer, data['post_id'])


def update_card(id, token, email):
    cu = stripe.Customer.retrieve(id)
    cu.source = token
    cu.email = email
    return cu.save()
