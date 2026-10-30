#!/bin/sh
# Download every card image from Riot's CDN as a resized WebP into raw/<card id>.webp.
# Run from the working directory that holds cards.json:  sh download_images.sh
mkdir -p raw
python3 -I -c "
import json
B='https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data_live/'
for c in json.load(open('cards.json'))['cards']:
    w=586 if c['o']=='l' else 420
    print(f\"{B}{c['img']}?accountingTag=RB&w={w}&fm=webp&q=80 raw/{c['id']}.webp\")
" | xargs -P 16 -n 2 sh -c 'curl -sS --retry 3 --max-time 60 -o "$1" "$0" || echo "FAIL $1"'
