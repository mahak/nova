Nova Style Commandments
=======================

- Step 1: Read the OpenStack Style Commandments
  https://docs.openstack.org/hacking/latest/
- Step 2: Read on

Nova Specific Commandments
---------------------------

- [N307] ``nova.db`` imports are not allowed in ``nova/virt/*``
- [N309] no db session in public API methods (disabled)
  This enforces a guideline defined in ``oslo.db.sqlalchemy.session``
- [N310] timeutils.utcnow() wrapper must be used instead of direct calls to
  datetime.datetime.utcnow() to make it easy to override its return value in tests
- [N311] importing code from other virt drivers forbidden
  Code that needs to be shared between virt drivers should be moved
  into a common module
- [N312] using config vars from other virt drivers forbidden
  Config parameters that need to be shared between virt drivers
  should be moved into a common module
- [N313] capitalize help string
  Config parameter help strings should have a capitalized first letter
- [N316] Change assertTrue(isinstance(A, B)) by optimal assert like
  assertIsInstance(A, B).
- [N317] Change assertEqual(type(A), B) by optimal assert like
  assertIsInstance(A, B)
- [N319] Validate that logs are not translated.
- [N320] Setting CONF.* attributes directly in tests is forbidden. Use
  self.flags(option=value) instead.
- [N322] Method's default argument shouldn't be mutable
- [N323] Ensure that the _() function is explicitly imported to ensure proper translations.
- [N324] Ensure that jsonutils.%(fun)s must be used instead of json.%(fun)s
- [N326] Translated messages cannot be concatenated.  String should be included in translated message.
- [N332] Check that the api_version decorator is the first decorator on a method
- [N334] Change assertTrue/False(A in/not in B, message) to the more specific
  assertIn/NotIn(A, B, message)
- [N335] Check for usage of deprecated assertRaisesRegexp
- [N336] Must use a dict comprehension instead of a dict constructor with a sequence of key-value pairs.
- [N337] Don't import translation in tests
- [N338] Change assertEqual(A in B, True), assertEqual(True, A in B),
  assertEqual(A in B, False) or assertEqual(False, A in B) to the more specific
  assertIn/NotIn(A, B)
- [N339] Check common raise_feature_not_supported() is used for v2.1 HTTPNotImplemented response.
- [N340] Check nova.utils.spawn() is used instead of greenthread.spawn() and eventlet.spawn()
- [N341] contextlib.nested is deprecated
- [N342] Config options should be in the central location ``nova/conf/``
- [N343] Check for common double word typos
- [N348] Deprecated library function os.popen()
- [N349] Check for closures in tests which are not used
- [N350] Policy registration should be in the central location ``nova/policies/``
- [N351] Do not use the oslo_policy.policy.Enforcer.enforce() method.
- [N352] LOG.warn is deprecated. Enforce use of LOG.warning.
- [N353] Validate that context objects is not passed in logging calls.
- [N355] Enforce use of assertTrue/assertFalse
- [N356] Enforce use of assertIs/assertIsNot
- [N357] Use oslo_utils.uuidutils or uuidsentinel(in case of test cases) to
  generate UUID instead of uuid4().
- [N358] Return must always be followed by a space when returning a value.
- [N359] Check for redundant import aliases.
- [N360] Yield must always be followed by a space when yielding a value.
- [N361] Check for usage of deprecated assertRegexpMatches and
  assertNotRegexpMatches
- [N362] Imports for privsep modules should be specific. Use "import nova.privsep.path",
  not "from nova.privsep import path". This ensures callers know that the method they're
  calling is using privilege escalation.
- [N363] Disallow ``(not_a_tuple)`` because you meant ``(a_tuple_of_one,)``.
- [N364] Check non-existent mock assertion methods and attributes.
- [N365] Check misuse of assertTrue/assertIsNone.
- [N366] The assert_has_calls is a method rather than a variable.
- [N367] Disallow aliasing the mock.Mock and similar classes in tests.
- [N368] Reject if the mock.Mock class is used as a replacement value instead of and
  instance of a mock.Mock during patching in tests.
- [N369] oslo_concurrency.lockutils.ReaderWriterLock() or
  fasteners.ReaderWriterLock() does not function correctly
  with eventlet patched code. Use nova.utils.ReaderWriterLock() instead.
- [N370] Don't use or import six
- [N371] You must explicitly import python's mock: ``from unittest import mock``
- [N372] Don't use the setDaemon method. Use the daemon attribute instead.
- [N373] Don't use eventlet specific concurrency primitives. Use the one
  from stdlib instead. E.g. eventlet.sleep => time.sleep

Creating Unit Tests
-------------------
For every new feature, unit tests should be created that both test and
(implicitly) document the usage of said feature. If submitting a patch for a
bug that had no unit test, a new passing unit test should be added. If a
submitted bug fix does have a unit test, be sure to add a new one that fails
without the patch and passes with the patch.

For more information on creating unit tests and utilizing the testing
infrastructure in OpenStack Nova, please read ``nova/tests/unit/README.rst``.


Running Tests
-------------
The testing system is based on a combination of tox and stestr. The canonical
approach to running tests is to simply run the command ``tox``. This will
create virtual environments, populate them with dependencies and run all of
the tests that OpenStack CI systems run. Behind the scenes, tox is running
``stestr run``, but is set up such that you can supply any additional
stestr arguments that are needed to tox. For example, you can run:
``tox -- --analyze-isolation`` to cause tox to tell stestr to add
--analyze-isolation to its argument list.

Python packages may also have dependencies that are outside of tox's ability
to install. Please refer to `Development Quickstart`_ for
a list of those packages on Ubuntu, Fedora and Mac OS X.

To run a single or restricted set of tests, pass a regex that matches
the class name containing the tests as an extra ``tox`` argument;
e.g. ``tox -- TestWSGIServer`` (note the double-hypen) will test all
WSGI server tests from ``nova/tests/unit/test_wsgi.py``; ``--
TestWSGIServer.test_uri_length_limit`` would run just that test, and
``-- TestWSGIServer|TestWSGIServerWithSSL`` would run tests from both
classes.

It is also possible to run the tests inside of a virtual environment
you have created, or it is possible that you have all of the dependencies
installed locally already. In this case, you can interact with the stestr
command directly. Running ``stestr run`` will run the entire test suite.
``stestr run --concurrency=1`` will run tests serially (by default, stestr runs
tests in parallel). More information about stestr can be found at:
http://stestr.readthedocs.io/

Since when testing locally, running the entire test suite on a regular
basis is prohibitively expensive, the ``tools/run-tests-for-diff.sh``
script is provided as a convenient way to run selected tests using
output from ``git diff``.  For example, this allows running only the
test files changed/added in the working tree::

    tools/run-tests-for-diff.sh

However since it passes its arguments directly to ``git diff``, tests
can be selected in lots of other interesting ways, e.g. it can run all
tests affected by a single commit at the tip of a given branch::

    tools/run-tests-for-diff.sh mybranch^!

or all those affected by a range of commits, e.g. a branch containing
a whole patch series for a blueprint::

    tools/run-tests-for-diff.sh gerrit/master..bp/my-blueprint

It supports the same ``-HEAD`` invocation syntax as ``flake8wrap.sh``
(as used by the ``fast8`` tox environment)::

    tools/run-tests-for-diff.sh -HEAD

By default tests log at ``INFO`` level. It is possible to make them
log at ``DEBUG`` level by exporting the ``OS_DEBUG`` environment
variable to ``True``.

.. _Development Quickstart: https://docs.openstack.org/nova/latest/contributor/development-environment.html

Building Docs
-------------
Normal Sphinx docs can be built via the setuptools ``build_sphinx`` command. To
do this via ``tox``, simply run ``tox -e docs``,
which will cause a virtualenv with all of the needed dependencies to be
created and then inside of the virtualenv, the docs will be created and
put into doc/build/html.

Building a PDF of the Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you'd like a PDF of the documentation, you'll need LaTeX and ImageMagick
installed, and additionally some fonts. On Ubuntu systems, you can get what you
need with::

    apt-get install texlive-full imagemagick

Then you can use the ``build_latex_pdf.sh`` script in tools/ to take care
of both the sphinx latex generation and the latex compilation. For example::

    tools/build_latex_pdf.sh

The script must be run from the root of the Nova repository and it'll copy the
output pdf to Nova.pdf in that directory.
