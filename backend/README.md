# CP13 - Web App Backend

## Git Branches

There will four types of branches.

1. master/main (PRODUCTION)

- Main Branch: Ensure the code in this branch is stable and ready to deliver
- Do not push to this branch

2. feature/\*

- Personal development branch. All new features should be developed based on master/main and checked out to a new feature branch
- The name of the branch should be based on the content being built
- Do not merge into the master branch

3. dev (DEVELOPMENT)

- You need to raise a pull request from the feature branch to the dev branch for code review
- After the development of a sprint is complete. Before merging from dev to master, rebase master and confirm the diff from master.

4. hotfix/\*

- For online problems in dev or master branches.
- One hotfix branch should only fix one problem.
- Merge into dev branch after the repair is complete.

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

## Setting up local environment

### Handling Package Dependency

Run the following command to run the virtual environment locally.

> virtualenv .venv && source .venv/bin/activate && pip install -r requirements.txt

Run the following command to update the virtual environment

> pip freeze > requirements.txt

Please see for further info  
https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository

### Setting up a local postgreSQL server

Within django_core/settings.py under DATABASES you will need to configure a local postgre server and connect it accordingly.

## Testing instructions

In order to run the tests:

1. ensure you are in the directory of the project containing 'manage.py'
2. run the command:
   > python manage.py test name_of_app/
3. output will be displayed showing the number of tests run, any failures, and any errors

To generate a coverage report:  
The python library coverage.py is currently being used.

1. ensure you are in the directory of the project containing 'manage.py'
2. run the command:
   > coverage run --source='.' manage.py test name_of_app/
3. to see the report in the terminal, run:
   > coverage report  
   > the report will be printed to the command line
4. to see an HTML version of the report, run:
   > coverage html  
   > this will create an htmlcov/ folder in your directory. Open this in your browser to view the coverage report.
