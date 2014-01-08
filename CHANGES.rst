0.3.1 (2014-01-08)
------------------
- Don't pin requirement versions so applications using pyramid_sna
  can decide what version they want.

0.3 (2013-12-30)
----------------
- Add support for Microsoft Live Connect. Contributed by
  Antonio Perez-Aranda Alcaide

0.2 (2013-04-30)
----------------
- Add documentation.

0.1.2 (2013-04-24)
------------------
- Make the library easier to depend on by not pinning the versions
  of all our indirect dependencies.

0.1.1 (2013-04-23)
------------------
- Fix a crash with Facebook auth because its response is not JSON.

0.1 (2013-04-23)
----------------
- Initial release with code from Yith Library Server
- License change with the agreement of original YLS copyright holders
- Make the scope configurable
- Make the [google,facebook]_callback views return the result of
  a configurable callback function.
