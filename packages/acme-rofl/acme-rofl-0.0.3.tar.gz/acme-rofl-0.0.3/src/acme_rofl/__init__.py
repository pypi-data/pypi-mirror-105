#!/usr/bin/env python3

"""ACME Respond Or Forward Listener forwards all port 80 connections to 443 except for requests to .well-known

This is not a proxy.  Leave it running and it takes over your port 80,
responding to ACME challenges and forwarding all other requests to
443.

If your site is devoted to https, you hopefully don't have a ton of
legacy http links out there on the web pointing at your site.  But
even if you do, this is built on twisted, and it goes brrr.

"""
import os
import click
import sys
from twisted.internet import reactor
from twisted.web import server, resource

class Simple(resource.Resource):
    isLeaf = True
    def __init__(self, root):
        resource.Resource.__init__(self)
        self.webroot = root

    def render_GET(self, request):

        # Handle acme challenge
        if request.uri.startswith(b"/.well-known"):
            path = self.webroot + request.uri.decode("utf-8")
            print(f"Request: {path}")

            # If it's not there, say so
            if not os.path.exists(path):
                request.setResponseCode(404)
                request.setHeader('Content-Type', 'text/plain; charset=utf-8')
                return b"Not found"

            try:
                with open(path, 'rb') as fh:
                    return fh.read()
            except:
                # We're just going to 500 on any error getting the file contents
                request.setResponseCode(500)
                request.setHeader('Content-Type', 'text/plain; charset=utf-8')
                return b"Error"

        # Redirect all other requests permanently
        url = request.URLPath()
        url.scheme = 'https'
        url.path=request.uri
        request.setResponseCode(301)
        request.setHeader('Location', str(url))
        return b""

    def render_POST(self, request):
        self.render_GET(request)


@click.command()
@click.option("--root", default="/var/www/acme", help="Path to the html webroot")
def run(root):
    "Run the ACME ROFL respond or forward listener"

    if not os.path.exists(root):
        sys.exit(f"{root} does not exist")

    server_root = Simple(root)
    site = server.Site(server_root)
    reactor.listenTCP(80, site)
    reactor.run()

if __name__ == "__main__":
    run()
