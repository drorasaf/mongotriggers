.. mongotriggers documentation master file, created by
   sphinx-quickstart on Tue Apr 11 00:20:12 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mongotriggers's documentation!
=========================================

This package provides a pythonic interface to allow real time updating, when MongoDB is updated,
this update could be up to application layer, or just reside in the backend of the application.

Modern applications are event-driven and not query-driven, therefore whenever there is an update,
the application would like to receive a feedback. This package enables this kind of behaviour.

Index
-----

**Getting Started**

* :doc:`install`
* :doc:`examples`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started

   install.rst
   examples.rst

**API Reference**

* :doc:`mongotriggers`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: API Reference

   mongotriggers.rst

**Help & Reference**

* :doc:`support`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help & reference

   support.rst
