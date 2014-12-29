cd webapp
git add .
git commit -am 'Update'
git push origin master
git branch gh-pages
git push -f origin gh-pages:gh-pages
git branch -D gh-pages
cd ..