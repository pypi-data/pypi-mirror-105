#######
USAGE
#######

**************
Instructions
**************

Call ``<menu>``
==================

Call ``menu`` [``dmenu``, ``bemenu``, ``<others>``] from python script as a replacement for input popups.


Basic usage
-------------
- Import in script:

.. code:: python

   # import
   from launcher_menus import menu

   user_letter = menu(command='bemenu', opts=['a', 'b', 'c', 'd'])
   if user_letter is not None:
       # user did not hit <Esc>
       print(user_letter)
   else:
       print("Aborted...")

Results:

::

   a


Fancy usage
---------------------
- User-defined styles

.. code:: python

   # import
   from launcher_menus import LauncherMenu

   mask_color = "#000000"
   password_menu = LauncherMenu(command='bemenu', filter_background=mask_color,
                                filter_foreground=mask_color)
   password = password_menu()
   if password is None:
       # user hit <Esc>
       print("Can't go ahead without password")
   else:
       print(password)  # A bad idea


Results:

::

   Can't go ahead without password

- Pre-defined themes

.. code:: python

   # import
   from launcher_menus.themes import emergency_prompt, password_prompt

*****************
Recommendation
*****************
- Use user-defined configurations
