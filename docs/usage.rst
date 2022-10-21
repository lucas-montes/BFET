Using BFET with Django
======================

Two of the modules more usefull for Django are DjangoTestingModel and DataCreator.


DataCreator
===========

.. DataCreator:

``DataCreator`` - Use different modules included with python like datetime to create values 
--------------------------------------------------------------------------

#. Import from the bfet library DataCreator:

    .. code-block:: console

        from bfet import DataCreator


#. Once imported you can use the different methods of DataCreator to cerate values:

    .. code-block:: console

        string = DataCreator.create_random_string()
        dict = DataCreator.create_random_json()
        email_string = DataCreator.create_random_email()
        datetime = DataCreator.create_random_datetime()


DjangoTestingModel
==================

.. DjangoTestingModel:

``DjangoTestingModel`` - Is based on the Django _default_manager's methods create, bulk_create and get_or_create
--------------------------------------------------------------------------

To use this with your project you need to follow these steps:

#. Import from the bfet library DjangoTestingModel:

    .. code-block:: console

        from bfet import DjangoTestingModel

#. Once imported you can start to create models for testing:

    .. code-block:: console

        from foo.models import BarModel


        bar_model = DjangoTestingModel.create(BarModel)

You can either include manually the fields with the values or let bfet create the values randomly.
Under the hood DjangoTestingModel uses DataCreator to populate the values for the fields.