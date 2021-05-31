. .env
nvm use 10
if [ -d "./_book" ]; then
    rm -rf ./_book
fi
gitbook build
cd _book
git init
git remote add github git@github.com:bamboosjtu/notes.git
git checkout -b gh-pages
git add .
git commit -m 'latest'
git push -u github gh-pages