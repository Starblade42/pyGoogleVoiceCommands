pyGoogleVoiceCommands
=====================

A python program that uses pygooglevoice to receive SMS commands and carry out command line actions in Unix (probably works in Windows though). pyGoogleVoiceCommands requires pygooglevoice to run, and you have to set it up and add the settings to the config file which contains the login information to your Google Voice account in ~/.gvoice

Don't forget to set up pyGoogleVoice using:
> python setup.py install

Relies on https://code.google.com/r/kkleidal-pygooglevoiceupdate/source/browse

Which is a patch to fix an authentication problem with pygooglevoice. The patch changes just a couple of lines which had bad static values. You can find the original project here:

https://code.google.com/p/pygooglevoice/
