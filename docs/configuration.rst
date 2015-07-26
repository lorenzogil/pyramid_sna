Configuration
-------------

pyramid_sna requires a Pyramid Session Factory since it need to store some information
in the user session during the authentication flow.

Check `pyramid documentation <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/sessions.html>`_
for information about how to setup a Session Factory and some popular examples.

After configuring the session support you need to include pyramid_sna
in your main function:

.. code-block:: py

   def main(global_config, **settings):

       config = Configurator(settings=settings)

       config.include('pyramid_sna')

       return config.make_wsgi_app()

Finally, you need to configure the settings for the social provider you want
to support. Check the next section for specific information about each
provider.
