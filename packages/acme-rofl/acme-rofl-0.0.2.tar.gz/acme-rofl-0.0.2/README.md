# ACME ROFL

ACME Respond Or Forward Listener

This simple listener does two things:

 * Respond to http requests for files in the .well-known directory

 * Forward all other requests via 301 Moved Permanently, redirecting
   to the same URL but using https.

Leave it running.  Run certbot periodically.
