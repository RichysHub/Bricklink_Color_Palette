from bricklink_api.auth import oauth
from bricklink_api.color import get_color_list
from bricklink_api.catalog_item import get_known_colors, get_price_guide, NewOrUsed, VATSetting, Type

from decouple import config

BRICKLINK_CONSUMER_KEY = config('BRICKLINK_CONSUMER_KEY')
BRICKLINK_CONSUMER_SECRET = config('BRICKLINK_CONSUMER_SECRET')

BRICKLINK_TOKEN_VALUE = config('BRICKLINK_TOKEN_VALUE')
BRICKLINK_TOKEN_SECRET = config('BRICKLINK_TOKEN_SECRET')

auth = oauth(BRICKLINK_CONSUMER_KEY,
             BRICKLINK_CONSUMER_SECRET,
             BRICKLINK_TOKEN_VALUE,
             BRICKLINK_TOKEN_SECRET)

all_colors = get_color_list(auth=auth)['data']
print(all_colors)

# Bricklink's API currently has no methods for obtaining full part indexes
# As such, an exhaustive search is not possible

# Define candidate parts to search within

# candidate_parts = ['3005', '3024', '54200', '98138', '4073', '3070b', '3003', '3022', '3068b', '3001', '3020']
candidate_parts = ['3005']
desired_quality = NewOrUsed.NEW
vat = VATSetting.Y

# list of parts
# for each part, dict of color: price
# can then extract some optimised lists for:
# cheapest collection of parts to get all colors
# collection of most colors in a single part, then cheapest
# for each color, dict of parts: price

color_prices = {color['color_id']: {} for color in all_colors}
part_prices = {part: {} for part in candidate_parts}

for part in candidate_parts:
    known_colors = get_known_colors(Type.PART, part, auth=auth)['data']
    for color in known_colors:
        color_id = color['color_id']
        price_guide = get_price_guide(Type.PART, part, color_id, new_or_used=desired_quality, vat=vat, auth=auth)['data']
        price = price_guide['avg_price']
        color_prices[color_id].update({part: price})
        part_prices[part].update({color_id: price})

print(color_prices)
print(part_prices)







