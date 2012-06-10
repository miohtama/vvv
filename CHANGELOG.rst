Changelog
===================

0.2.5 - 0.3.0
------------------

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