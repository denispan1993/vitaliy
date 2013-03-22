AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.twitter.TwitterBackend',
    # 'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    # 'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.browserid.BrowserIDBackend',
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',
    # 'social_auth.backends.contrib.disqus.DisqusBackend',
    # 'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    # 'social_auth.backends.contrib.orkut.OrkutBackend',
    # 'social_auth.backends.contrib.foursquare.FoursquareBackend',
    # 'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.yandex.YandexOAuth2Backend',
    'social_auth.backends.contrib.yandex.YandexBackend',
    'social_auth.backends.contrib.yandex.YaruBackend',
    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiAppBackend',
    'social_auth.backends.contrib.vkontakte.VKontakteOAuth2Backend',
    'social_auth.backends.contrib.vkontakte.VKontakteBackend',
    # 'social_auth.backends.contrib.live.LiveBackend',
    # 'social_auth.backends.contrib.skyrock.SkyrockBackend',
    # 'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    # 'social_auth.backends.contrib.readability.ReadabilityBackend',
    # 'social_auth.backends.OpenIDBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'social_auth.context_processors.social_auth_by_type_backends',
)

TWITTER_CONSUMER_KEY              = ''
TWITTER_CONSUMER_SECRET           = ''
FACEBOOK_APP_ID                   = ''
FACEBOOK_API_SECRET               = ''
LINKEDIN_CONSUMER_KEY             = ''
LINKEDIN_CONSUMER_SECRET          = ''
SKYROCK_CONSUMER_KEY              = ''
SKYROCK_CONSUMER_SECRET           = ''
ORKUT_CONSUMER_KEY                = ''
ORKUT_CONSUMER_SECRET             = ''
#OAuth2
GOOGLE_OAUTH2_CLIENT_ID = '442207703537.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'R6RYIo1b6w8oQvtR-duuGRPo'
GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
#
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = True
SOCIAL_AUTH_DEFAULT_USERNAME      = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
LOGIN_ERROR_URL                   = '/login/error/'
#OpenAPI
VKONTAKTE_APP_ID = '' # '3474809'
VKONTAKTE_APP_SECRET = '' # 'BapEJeIg9oRgfXRQABor'
# Usage for applications auth: {'key': application_key, 'user_mode': 0 (default) | 1 (check) | 2 (online check) }
# 0 means is_app_user request parameter is ignored, 1 - must be = 1, 2 - checked via VK API request (useful when user
# connects to your application on app page and you reload the iframe)
VKONTAKTE_APP_AUTH                = None
ODNOKLASSNIKI_OAUTH2_CLIENT_KEY   = '163445760'
ODNOKLASSNIKI_OAUTH2_APP_KEY      = 'CBANPOLKABABABABA'
ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET = '5E0652D81620317290DED086'
MAILRU_OAUTH2_CLIENT_KEY   		  = ''
MAILRU_OAUTH2_APP_KEY      		  = ''
MAILRU_OAUTH2_CLIENT_SECRET       = ''
#SOCIAL_AUTH_USER_MODEL           = 'app.CustomUser'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
GITHUB_APP_ID                     = ''
GITHUB_API_SECRET                 = ''
FOURSQUARE_CONSUMER_KEY           = ''
FOURSQUARE_CONSUMER_SECRET        = ''
DOUBAN_CONSUMER_KEY               = ''
DOUBAN_CONSUMER_SECRET            = ''
YANDEX_OAUTH2_CLIENT_KEY          = '9827973f694743c493d9d3b0ca75ef9a'
YANDEX_OAUTH2_CLIENT_SECRET       = '9fd1bd404b25435b951b95a28ed96ed6'
YANDEX_OAUTH2_API_URL             = 'https://api-yaru.yandex.ru/me/' # http://api.moikrug.ru/v1/my/ for Moi Krug
DAILYMOTION_OAUTH2_KEY            = ''
DAILYMOTION_OAUTH2_SECRET         = ''
SHOPIFY_APP_API_KEY                 = ''
SHOPIFY_SHARED_SECRET             = ''
STOCKTWITS_CONSUMER_KEY           = ''
STOCKTWITS_CONSUMER_SECRET        = ''
READABILITY_CONSUMER_KEY          = ''
READABILITY_CONSUMER_SECRET       = ''

# Backward compatibility
YANDEX_APP_ID = YANDEX_OAUTH2_CLIENT_KEY
YANDEX_API_SECRET = YANDEX_OAUTH2_CLIENT_SECRET

#OAuth2
VK_APP_ID = '3474809'
VK_API_SECRET = 'BapEJeIg9oRgfXRQABor'
#VK_APP_ID = VKONTAKTE_APP_ID
#VK_API_SECRET = VKONTAKTE_APP_SECRET
# VKONTAKTE_APP_AUTH={'key':'iframe_app_secret_key', 'user_mode': 2, 'id':'iframe_app_id'}

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'app.pipeline.redirect_to_form',
    'app.pipeline.username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)
