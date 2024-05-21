## CP13 Group 1 Frontend

## Procedure for new feature

1. Check you're building with the latest master branch
   > git checkout master && git pull --rebase
2. Create your own feature branch
   > git checkout -b feature/your-feature  
   > git push --set-upstream origin feature/your-feature
3. After development, commit and push your code to **your own feature branch**
   > git checkout feature/your-feature  
   > git commit -m "feature: the changes"  
   > git push
4. Rebase master and raise a pull request to the dev branch.
   > git checkout feature/your-feature  
   > git rebase master  
   > git push --set-upstream origin feature\your-feature
5. After testing and code review, approve the pull request and merge into dev
