from django.conf import settings

# Environment (sandbox, sandbox-beta, live)
PAYPALCART_ENVIRONMENT   = getattr(settings, 'PAYPALCART_ENVIRONMENT',   'sandbox')

# API Details (Use the default SDK credentials)
PAYPALCART_API_USER      = getattr(settings, 'PAYPALCART_API_USER',      'sdk-three_api1.sdk.com')
PAYPALCART_API_PASSWORD  = getattr(settings, 'PAYPALCART_API_PASSWORD',  'QFZCWN5HZM8VBG7Q')
PAYPALCART_API_SIGNATURE = getattr(settings, 'PAYPALCART_API_SIGNATURE', 'A-IzJhZZjhg29XQ2qnhapuwxIDzyAZQ92FRP5dqBzVesOkzbdUONzmOU')