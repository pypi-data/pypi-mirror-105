Zero
====

.. __INCLUDE_0__

.. raw:: html

    <img src="https://raw.githubusercontent.com/Yura52/zero/master/other/logo.png" width="190px" style="text-align:center;display:block;">

Zero is a general-purpose library for PyTorch users. Zero:

- simplifies training loop, reproducibility, models evaluation and other typical Deep Learning tasks
- provides a collection of "building blocks" and leaves code organization to you
- can be used on its own or together with PyTorch frameworks such as
  `Lightning <https://github.com/PytorchLightning/pytorch-lightning>`_,
  `Ignite <https://github.com/pytorch/ignite>`_,
  `Catalyst <https://github.com/catalyst-team/catalyst>`_ and
  `others <https://pytorch.org/ecosystem>`_

**NOTE:** Zero is tested (and battle-tested in research projects), but the interface is
not stable yet, so backward-incompatible changes in future releases are possible.

Overview
--------

- `Website <https://yura52.github.io/zero>`_
- `Code <https://github.com/Yura52/zero>`_
- `Learn Zero <https://yura52.github.io/zero/learn.html>`_
- `Classification task example (MNIST) <https://github.com/Yura52/zero/blob/master/examples/mnist.py>`_
- `The first release announcement <https://github.com/Yura52/zero/issues/21>`_ (Zero itself has changed a lot, but the motivation is still relevant)

.. __INCLUDE_1__

Installation
------------

If you plan to use the GPU version of PyTorch, install it **before** installing Zero
(otherwise, the CPU version will be installed together with Zero).

.. code-block:: bash

    $ pip install libzero

Dependencies
^^^^^^^^^^^^

- Python >= 3.7
- NumPy >= 1.17
- PyTorch >= 1.6 (CPU or CUDA >= 10.1)
- pynvml >= 8.0
- tqdm >= 4.0

How to contribute
-----------------

- See `issues <https://github.com/Yura52/zero/issues>`_, especially with the labels
  `"discussion" <https://github.com/Yura52/zero/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22+label%3Adiscussion>`_
  and `"help wanted" <https://github.com/Yura52/zero/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22>`_
- `Open issues <https://github.com/Yura52/zero/issues/new/choose>`_ with bugs, ideas and
  any other kind of feedback

If your contribution includes pull requests, see `CONTRIBUTING.md <https://github.com/Yura52/zero/blob/master/other/CONTRIBUTING.md>`_

Why "Zero"?
-----------

Zero aims to be `zero-overhead <https://isocpp.org/wiki/faq/big-picture#zero-overhead-principle>`_
in terms of *mental* overhead: solutions, provided by Zero, try to
be as minimal, intuitive and easy to learn, as possible. Well, all these things can be
pretty subjective, so don't take it too seriously :wink:
