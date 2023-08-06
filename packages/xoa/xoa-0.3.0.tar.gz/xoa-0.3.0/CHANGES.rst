What's new
##########


Current  (unreleased)
=====================

New features
------------

Documentation
-------------

Deprecations
------------

Breaking changes
----------------

Bug fixes
---------


v0.3.0
======

New features
------------

- Add the :func:`xoa.plot.plot_flow` function [:pull:`9`].
- Improve :func:`xoa.coords.get_depth` so that it can compute
  depth from sigma coordinates or layer thinknesses [:pull:`8`].
- Add the :func:`xoa.dyn.flow2d` function [:pull:`7`].
- Add the :func:`xoa.regrid.extrap1d` function.
- Add the :func:`xoa.filter.erode_coast` function which is specialized version
  of the :func:`xoa.filter.erode_mask` for horizontal data.
- Add the :func:`xoa.coords.get_xdim`, :func:`~xoa.coords.get_ydim`,
  :func:`~xoa.coords.get_zdim`, :func:`~xoa.coords.get_tdim` and
  :func:`~xoa.coords.get_fdim` for quickly finding standard dimensions.

Documentation
-------------

Deprecations
------------

Breaking changes
----------------

Bug fixes
---------

- Fix u and v CF config [:pull:`6`]


0.2.0
=====
