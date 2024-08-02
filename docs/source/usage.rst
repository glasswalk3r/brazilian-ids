Usage
=====

Installation
------------

To use ``brazilian_ids`` package, first install it using ``pip``:

.. code-block:: console

   (.venv) $ pip install brazilian_ids


Selecting a function
--------------------

Functions are organized per package domain:

- company
- labor dispute
- location
- person
- real state

.. code-block::

   └── functions
      ├── company
      │  └── cnpj
      ├── exceptions
      ├── labor_dispute
      │  └── nupj
      ├── location
      │   ├── cep
      │   └── municipio
      ├── person
      │   ├── cpf
      │   └── pis_pasep
      └── real_state
          ├── cno
          └── sql


See the modules documentation for more details.