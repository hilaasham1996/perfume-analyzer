#!/bin/bash
# deploy.sh — خودکارساز ساخت ریپو GitHub و push + آماده سازی Render
# قبل از اجرا، مطمئن شو که git و curl و jq نصب هستند
# و در سیستم login شده به GitHub هستی یا یک Personal Access Token داری

# تنظیمات
USERNAME="hilaasham1996"
REPONAME="perfume-analyzer"

echo "==> ساخت ریپوی GitHub به نام $REPONAME ..."
# اگر PAT داری، دستور ساخت ریپو با curl
# export GITHUB_TOKEN=<token> قبل از اجرا
if [ -z "$GITHUB_TOKEN" ]; then
  echo "⚠️ لطفاً یک Personal Access Token در متغیر GITHUB_TOKEN تعریف کن."
  echo "راهنما: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
  exit 1
fi

curl -H "Authorization: token $GITHUB_TOKEN"      -d "{\"name\":\"$REPONAME\",\"private\":false}"      https://api.github.com/user/repos

echo "==> git init و commit اولیه ..."
git init
git add .
git commit -m "Initial commit - Perfume Analyzer by Hila"

git branch -M main
git remote add origin https://github.com/$USERNAME/$REPONAME.git
git push -u origin main

echo "✅ ریپو ساخته و push شد. حالا به Render برو و ریپو را متصل کن."
echo "Render: https://render.com/dashboard/new"
