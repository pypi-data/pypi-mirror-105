** beautify the appearance of the application in the terminal. **

what can be done, give the text color, text background, change the font, choose a banner according to the category of your choice.

Method Property
- font
- strings
- textArt
- list_art
- list_font
- decoration
- help_me_bro
- random_font
- url_strings
- list_ascii_art
- list_decoration

** Fonts **

- `list font 1`_
- `list font 2`_

** Art **

- `art list 1`_
- `art list 2`_

** Decoration.**

- `decor list 1`_
- `decor list 2`_

- `category list name`_

** the color of the strings.**

.. code:: python

    from beautify import Beautify
    # Beautify(**kwargs).method_name
    print(Beautify(
        string="Hello World",
        font="scammer",
        color="#eaea",
        bg_color=None).strings)


.. _list font 1: https://github.com/sepandhaghighi/art/blob/master/FontList.ipynb
.. _list font 2: https://www.4r7.ir/FontList.html
.. _art list 1: https://github.com/sepandhaghighi/art/blob/master/ArtList.ipynb
.. _art list 2: https://www.4r7.ir/ArtList.html
.. _decor list 1: https://github.com/sepandhaghighi/art/blob/master/DecorList.ipynb
.. _decor list 2: https://www.4r7.ir/DecorList.html
.. _category list name: https://github.com/ExsoKamabay/terminal-banner/blob/main/category_names_ascii_art