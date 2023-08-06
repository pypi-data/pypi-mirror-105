# ACME ROFL

ACME Respond Or Forward Listener

This simple listener does two things:

 * Respond to http requests for files in the .well-known directory

 * Forward all other requests via 301 Moved Permanently, redirecting
   to the same URL but using https.

Leave it running.  Run certbot periodically.

## Systemd

There's a systemd service that you might want to enable.  If you
installed this via pip, you'll find
`/usr/local/share/acme-rofl/acme-rofl.service`.  Symlink that wherever
your systemd scripts live.  On Debian that could be one of several
places, and one of them is `/etc/systemd/system`.

Then, tell systemd there's a new script:

    systemctl daemon-reload
