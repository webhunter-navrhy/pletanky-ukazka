#!/bin/sh
# cache busting: ?v=<hash> u CSS/JS
cd "$(dirname "$0")"
C=$(shasum style.css | cut -c1-8); J=$(shasum main.js | cut -c1-8)
for f in index.html kategorie.html produkt.html srovnani.html; do
  sed -i '' -E "s/style\.css\?v=[^\"]*/style.css?v=$C/; s/main\.js\?v=[^\"]*/main.js?v=$J/" $f
done
echo "css $C js $J"
