infoauth
========

A small but handy module and script to load/save tokens from/to disk.

It does:

- Save tokens in a file in disk, pickled and zipped

- Change the file to read-only, and only by yourself

- Load the tokens from disk

In which case this module is useful? Say you have a script or program that
needs to use some secret tokens (mail auth, twitter tokens, DB connection info,
etc...), but you don't want to include those tokens in the code, because it is
public, so with this module you do::

    tokens = infoauth.load(os.path.expanduser("~/.my-tokens"))

Note that the file will remain only readable by yourself, and not in the
project directory (so you don't have the risk of sharing it by accident).

**WARNING**: it does NOT protect your secrets with any key or anything, this
module does NOT secure your secrets in any way. Yes, the tokens are scrambled
(because pickled and zipped) and other people may not be able to access them
easily (readable only by you), but no further protection is implemented. Use
at your own risk.


How to use it from a Python program?
------------------------------------

Load your tokens::

    import infoauth
    auth = infoauth.load(os.path.expanduser("~/.my-mail-auth"))
    # ...
    mail.auth(auth['user'], auth['password'])

Dump some secrets::

    import infoauth
    secrets = {'some-stuff': 'foo', 'code': 67}
    infoauth.dump(secrets, os.path.expanduser("~/.secrets"))

Note that as storing the secret tokens is normally done once, it's surely
handier to do it from the command line, as shown in the next section.


How to use it from the command line?
------------------------------------

Show the tokens::

    $ infoauth show ~/.my-mail-auth
    password: ...
    user: ...

Create a file with your secrets::

    $ infoauth create ~/.secrets some-stuff=foo code=67

Note that creating the file from the command line has the limitation of all
values stored being strings (if you want to store other data types, as
integers, lists or any custom objects, you would need to use the
programmatically way of dumping your secrets to disk, as shown in the previous
section).
