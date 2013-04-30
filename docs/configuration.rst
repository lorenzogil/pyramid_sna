Configuration
-------------

pyramid_sna depends on pyramid_beaker since it need to store some information
in the user session during the authentication flow. A very simple session
configuration looks like this:

.. code-block:: ini

   # Sessions
   session.type = file
   session.data_dir = %(here)s/sessions/data
   session.lock_dir = %(here)s/sessions/lock
   session.cookie_on_exception = true

Check `pyramid_beaker documentation <http://docs.pylonsproject.org/projects/pyramid_beaker/en/latest/>`_
for other more advanced options.

After configuring the session support you need to include both pyramid_beaker
and pyramid_sna in your main function:

.. code-block:: py

   def main(global_config, **settings):

       config = Configurator(settings=settings)

       config.include('pyramid_beaker')
       config.include('pyramid_sna')

       return config.make_wsgi_app()

Finally, you need to configure the settings for the social provider you want
to support. Check the next section for specific information about each
provider.
