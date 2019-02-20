doku
====

**doku** is a cli tool to read and manipulate
documents in DokuWiki via its XMLRPC endpoint.

Install
~~~~~~~

::

   pip install doku

   # or as a user
   pip install --user doku

Configuration
~~~~~~~~~~~~~

Enable XML RPC on your DokuWiki instance:
Admin > Configuration Settings > Authentication

Create a new file: $HOME/.doku.ini

::
   [connection]
   domain = domain.name.tld
   username = your-username
   password = your-password
   ssl = true
   path = /


Example usage:
~~~~~~~~~~~~~~

::

   ❯ doku list
   [2019-01-06 09:29:03] playground:playground
   [2019-01-06 09:18:47] wiki:dokuwiki
   [2019-01-06 09:18:47] wiki:syntax
   [2019-01-06 09:18:47] wiki:welcome

   doku list --namespace :playground
   [2019-01-06 09:29:03] playground:playground

   ❯ doku edit wiki:welcome
   # this will open your $EDITOR
   # with the full content of the wiki page
   Document saved.

   ❯ doku cat playground:playground
   ====== PlayGround ======

   ❯ doku --help
   Usage: doku [OPTIONS] COMMAND [ARGS]...

   Options:
     --help  Show this message and exit.

   Commands:
     cat
     edit
     list
     search
