Changelog
===================

0.4.3 (2012-10-14)
------------------

- Better instructions for running demo [miohtama]

- Handle missing options file more gracefully [miohtama]

- Added ZPT validator [matejc]

- Fixes for RST validator [matejc]

- Ghetto CI runs on Python 2.7 [miohtama]

0.4.2 (2012-06-30)
------------------

- Windows compatibility confirmed [jsalonen]

- Fixed more issues with bad command line options [miohtama]

0.4.1 (2012-06-27)
------------------

- Handle empty / missing config files more gracefully [miohtama]

0.4.0 (2012-06-26)
------------------

- Python 2.7 compatibility added [miohtama]

- Refactored text plug-ins to silently ignore bad encoding [miohtama]

- Intelligent git pre-commit hook; check only changed files [miohtama]

- vvv-add-js-globals helper command added to add jslint global statements
  to multiple Javascript files once [miohtama]

- Evil spacebar buster added [miohtama]

- ``jshint`` now properly reads config files (was non-std parsing by Node.js argument library) [miohtama]

- Reorganized docs to have Tools section [miohtama]

0.2.4 - 0.2.5
---------------

- Depend on docutils as RST validator soft-depends on it, but cannot install docutils in host environment [miohtama]

0.2.3 - 0.2.4
---------------

- Correctly pick up RST validator script from path if not under virtualenv [miohtama]

0.2.2 - 0.2.3
---------------

- More git hook silent install corner case fixes

0.2.1 - 0.2.2
---------------

- Smarter way to detect vvv command location when installing a precommit hook [miohtama]

- Integration documentation updates [miohtama]

0.2 - 0.2.1
---------------

- Fixed changelog formatting now that PyPi README page is intact again

0.1.1 - 0.2
---------------

- ``pylint-command`` option added [miohtama]

- Ghetto-CI continuous integration script [miohtama]

- Configuration file reader refactored to something more beautiful [miohtama]

- Now you can VVV individual files [miohtama]

- VVV can walk up in the directory tree to find validation-options.yaml file [miohtama]

- Set ``zip_safe = False`` on the egg just in case [miohtama]

0.1 - 0.1.1
--------------

- Added Github links to README [miohtama]

0.1
----

- Initial release