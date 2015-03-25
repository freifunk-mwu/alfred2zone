
**zone_from_alfred**

It is self contained, completely configured through the ``defaults.yaml`` / ``config.yaml``

It requires Google's `ipaddress` module. I won't ship it here.

Please install directly from `their git repo <https://code.google.com/p/ipaddress-py/source/checkout>`_::

    pip3 install git+https://code.google.com/p/ipaddress-py/

|

In general, run::

    python3 zone_from_alfred.py

to generate all specified zonefiles at once.

Do not run as root, and make sure current user may write to the zonefiles.
