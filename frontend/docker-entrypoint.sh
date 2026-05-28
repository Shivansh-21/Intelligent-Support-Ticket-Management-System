#!/bin/sh

set -e

# Replace ${BACKEND_URL} in the nginx template and write final config
envsubst '${BACKEND_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Start nginx in foreground
exec nginx -g 'daemon off;'
