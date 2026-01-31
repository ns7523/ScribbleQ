hwte.utils
===========

This module regroups non-core features that are complementary to the rest of the package.

.. currentmodule:: hwte.utils


Visualization
-------------
Easy-to-use functions to make sense of your model's predictions.

.. currentmodule:: hwte.utils.visualization

.. autofunction:: visualize_page

Reconstitution
---------------

.. currentmodule:: hwte.utils.reconstitution

.. autofunction:: synthesize_page


.. _metrics:

Task evaluation
---------------
Implementations of task-specific metrics to easily assess your model performances.

.. currentmodule:: hwte.utils.metrics

.. autoclass:: TextMatch

   .. automethod:: update
   .. automethod:: summary

.. autoclass:: LocalizationConfusion

   .. automethod:: update
   .. automethod:: summary

.. autoclass:: OCRMetric

   .. automethod:: update
   .. automethod:: summary

.. autoclass:: DetectionMetric

   .. automethod:: update
   .. automethod:: summary
