.. bootpeg documentation master file, created by
   sphinx-quickstart on Tue Mar 30 17:33:14 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`bootpeg` – the bootstrapping PEG parser
========================================

.. image:: https://readthedocs.org/projects/bootpeg/badge/?version=latest
    :target: https://bootpeg.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/bootpeg.svg
    :alt: Available on PyPI
    :target: https://pypi.python.org/pypi/bootpeg/

.. toctree::
   :maxdepth: 1
   :caption: Usage and Guides
   :hidden:

   source/getting_started
   source/parse_actions
   source/peg_precedence
   source/glossary

.. toctree::
   :maxdepth: 1
   :caption: Builtin Meta Grammars
   :hidden:

   source/grammar_bpeg
   source/grammar_peg

.. toctree::
   :maxdepth: 1
   :caption: Development
   :hidden:

   contributing

`bootpeg` is a PEG parser for creating parsers – including itself.
By default, it supports a modified EBNF with actions akin to `PEP 617`_.

.. code-block:: python3

   >>> # recreate the bootpeg parser from itself
   >>> from bootpeg.api import import_parser, PikaActions
   >>> from bootpeg.grammars import bpeg
   >>> parse_bpeg = bpeg.parse
   >>> for _ in range(5):
   ...     parse_bpeg = import_parser(
   ...         bpeg.__name__, actions=PikaActions, dialect=parse_bpeg
   ...     )

Unlike most other Python PEG parsers which are top-down parsers,
`bootpeg` provides a bottom-up `Pika parser`_:
it handles left-recursive grammars natively,
allows recovering partial parse results,
and is guaranteed to run in linear time.
Like any PEG parser, `bootpeg` automatically
creates unambiguous grammars,
supports infinite lookahead,
and allows to express grammars comfortably.

* Native support for left-recursion and left-associativity.
* Builtin error reporting covering multiple failures.
* Automatic parser generation from a multitude of meta-grammars.

This makes it straightforward to implement your own custom grammars without
worrying about their implementation.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`PEP 617`: https://www.python.org/dev/peps/pep-0617/
.. _`Pika parser`: https://arxiv.org/abs/2005.06444
