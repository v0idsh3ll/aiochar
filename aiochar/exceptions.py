class BaseAiocharException(Exception):
    pass

class InvalidKey(BaseAiocharException):
    def __init__(self):
        super().__init__("API key is missing or invalid.")

class NotFoundPost(BaseAiocharException):
    def __init__(self):
        super().__init__("Post not found.")

class NoEnoughData(BaseAiocharException):
    def __init__(self):
        super().__init__("Not enough data. Check that you provided all needed data.")

class APIError(BaseAiocharException):
    def __init__(self, *args):
        super().__init__(*args)

class CharBadRequest(BaseAiocharException):
    pass

class InvalidSort(BaseAiocharException):
    def __init__(self):
        super().__init__("Invalid sort. Available: 'latest' (by default), 'popular', 'likes'")

class InvalidTimeFrame(BaseAiocharException):
    def __init__(self):
        super().__init__("Invalid timeframe. Available: '24h', '1w', '1m', '1y', 'all'. Only with 'likes' sort.")

class InvalidCountryCode(BaseAiocharException):
    def __init__(self):
        super().__init__("Wrong country_code. All codes: ('AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW').")

class InvalidPostContent(BaseAiocharException):
    def __init__(self):
        super().__init__("Wrong post content. Check that length of content you provided is less than 1025 symbols.")

class InvalidPollContent(BaseAiocharException):
    def __init__(self):
        super().__init__("Wrong poll content. Check that length of content you provided is less than 201 symbols.")

class InvalidPollOptions(BaseAiocharException):
    def __init__(self):
        super().__init__("Wrong quantity of polls. Please check it is less than 5.")

class InvalidPostFormat(BaseAiocharException):
    def __init__(self):
        super().__init__("Wrong post. You must provide at least one of content or poll_options")

class InvalidCategory(BaseAiocharException):
    def __init__(self):
        super().__init__("Wrong category. Available are: 'posts','likes','reposts','followers','mutes','followed_tags','muted_tags'")