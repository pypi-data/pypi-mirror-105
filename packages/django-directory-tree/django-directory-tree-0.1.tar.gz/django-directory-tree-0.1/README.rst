# Directory-Tree

Directory Tree is a Django app to see all directory in media folder.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'directory_tree',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('dir_tree/', include('directory_tree.urls')),

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

4. Visit http://127.0.0.1:8000/dir_tree/ to participate in the directory tree.