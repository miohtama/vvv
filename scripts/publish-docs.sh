#!/bin/sh
#
# Push docs to GitHub
#
# Run:
#
# sh scripts/publish-docs.sh
#

cd docs ; make html
rm -rf dist/gh-pages
mkdir dist/gh-pages
cd dist
# Need to have gh-pages initialized first http://help.github.com/pages/
git clone -b gh-pages git@github.com:miohtama/vvv.git gh-pages
cp -r ../../docs/build/html .
git add -A
git commit -m "Updated gh-pages with new docs"
git push