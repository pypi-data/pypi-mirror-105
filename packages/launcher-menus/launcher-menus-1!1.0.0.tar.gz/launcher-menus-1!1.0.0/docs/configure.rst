####################
USER-CONFIGURATION
####################

Configuration file is in `yaml <https://yaml.org/spec/>`__ format.

|menu|.yml files bear flags corresponding to actions for |menu|,
where |menu| may be dmenu, bemenu, etc

Any file named ``_template.yml`` is ignored.

********************************
Location of configuration files
********************************

Default:
===========

``<installation path>/site-packages/launcher_menus/``\ `menu-cfgs <launcher_menus/menu-cfgs>`__

Custom configuration may be specified at the following locations:

User (XDG_CONFIG_HOME):
========================

This variable is generally set to ``$HOME/.config`` on unix-like
systems. Even if unset, we will still try the ``$HOME/.config``
directory.

``$XFG_CONFIG_HOME/launcher_menus/<menu>.yml``

Local:
==========

``.launcher_menus/<menu>.yml**

.. note::

  - Configuration is loaded in the same order as described above.

.. warning::

  - A later loaded configuration **SHALL** overwrite a previously loaded configuration if defined for the same |menu|.

*********************
Configuration format
*********************

Copy `_template <launcher_menus/menu-cfgs/_template.yml>`__ to
`menu-cfgs <launcher_menus/menu-cfgs>`__/|menu|.yml

.. |menu| replace:: <menu>


Edit fields to provide flags:

-  Example:

   .. code:: yaml

      bottom: -b
      prompt: --prompt

Example:
==========

_template.yml
--------------

.. code:: yaml
  :name: ${HOME}/.config/launcher_menus/_template.yml

  bool:
    bottom: null
    grab: null
    wrap: null
    ifne: null
    ignorecase: null
    nooverlap: null

  input:
    version: null
    lines: null
    monitor: null
    height: null
    prompt: null
    prefix: null
    index: null
    scrollbar: null
    font: null
    title_background: null
    title_foreground: null
    normal_background: null
    normal_foreground: null
    filter_background: null
    filter_foreground: null
    high_background: null
    high_foreground: null
    scroll_background: null
    scroll_foreground: null
    selected_background: null
    selected_foreground: null
    windowid: null
