#!/bin/sh
#
# Push docs to GitHub
#
# Run:
#
# sh scripts/publish-docs.sh
#
# CSS issues: https://github.com/blog/572-bypassing-jekyll-on-github-pages
#

cd docs
make html
cd ..
rm -rf dist/gh-pages
mkdir dist/gh-pages
cd dist
# Need to have gh-pages initialized first http://help.github.com/pages/
git clone -b gh-pages git@github.com:miohtama/vvv.git gh-pages
cd gh-pages
cp -r ../../docs/build/html/* .
# CSS issues: https://github.com/blog/572-bypassing-jekyll-on-github-pages
touch .nojekyll
git add -A
git commit -m "Updated gh-pages with new docs"
git push origin gh-pages
cd ..
cd ..
