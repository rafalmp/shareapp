ShareApp
========

Securely share files or URLs

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Getting Up and Running Locally With Docker
------------------------------------------
This is the recommended method for running and developing the project locally.
All of the commands below assume you are in the root of the cloned project.
For other options, and more detailed instructions, refer to the `Cookiecutter Django documentation
<https://cookiecutter-django.readthedocs.io/en/latest/index.html>`_.

Prerequisites
^^^^^^^^^^^^^

* Docker_
* `Docker Compose <https://docs.docker.com/compose/install/>`_

.. _Docker: https://docs.docker.com/install/#supported-platforms

Build the Stack
^^^^^^^^^^^^^^^
::

  $ docker-compose -f local.yml build

Run the Stack
^^^^^^^^^^^^^
::

  $ docker-compose -f local.yml up

Execute Management Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  $ docker-compose -f local.yml run --rm django python manage.py migrate
  $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

Emails During Local Development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For your convenience a `MailHog <https://github.com/mailhog/MailHog/>`_ container is provided.
To read mail sent by the application, simply visit http://127.0.0.1:8025 in your browser.


Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form.
  Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your
  MailHog interface (see above) to read the email verification message. Copy the
  link into your browser. Now the user's email should be verified and ready to go.

* To create a **superuser account**, use the **createsuperuser** management command
  mentioned above.
