flake8-efm
==========

A plugin for flake8 to print output in a format compatible with Vim's
errorformat (efm).

Designed for efm-langserver_, but should work on any tool that expects a
similar format.

The exact format is ``%f:%l:%c:%t:%m``.

.. _efm-langserver: https://github.com/mattn/efm-langserver/

Details
-------

The default error format of flake8 shows an error code and a message, but
there's no obvious way to determine if something is an error or a warning. This
is especially true for third-party codes.

This plugin explicitly prints the error level in the output. There's support
for _some_ third-party plugins, and patches for others are most welcome.
