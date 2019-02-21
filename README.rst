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
   
   # upgrade
   pip install --upgrade doku

Configuration
~~~~~~~~~~~~~

Enable XML RPC on your DokuWiki instance:
:code:`Admin > Configuration Settings > Authentication`

Create a new file: :code:`$HOME/.doku.ini`

::

   [connection]
   domain = domain.name.tld
   username = your-username
   password = your-password
   ssl = true
   path = /

   [settings]
   indexpage = root


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

Diary
~~~~~

With :code:`diary` commands, you can use your wiki as a diary (surprise).

The :code:`show` command will show you all your logs (today).

The :code:`log` command will open up your :code:`$EDITOR` and after save+quit,
it will append it for your diary page (today).

When you call log, doku will check all the path back and generates
content for the tree.

For example:

::

   # Today is 2019-02-21 and your index is configured to be 'root'
   doku diary log

   # This will create the following pages if it's not exist
   :diary:2019:02:21
   :diary:2019:02:root
   :diary:2019:root

   # Will regenerate this page
   # if you log an entry in a year previously was not there
   :diary:root


