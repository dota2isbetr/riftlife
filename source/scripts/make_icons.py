"""Pack the rendered 16/32/48 px PNGs into favicon.ico and write the web manifest. Run after make_icons.js."""
import json, shutil
from PIL import Image
imgs = [Image.open(f'source/icons/png-{s}.png').convert('RGBA') for s in (16, 32, 48)]
imgs[2].save('favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:2])
shutil.copy('source/icons/favicon.svg', 'favicon.svg')
json.dump({
    'name': 'RIFTLIFE', 'short_name': 'RIFTLIFE', 'start_url': './', 'display': 'standalone',
    'background_color': '#EDF1F2', 'theme_color': '#0D141B',
    'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
              {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}],
}, open('site.webmanifest', 'w'), indent=1)
print('favicon.ico, favicon.svg, site.webmanifest written')
