# Set up our main application and load data into it

This is a good exercise for new developers joining the project. You are likely to be asked to develop the Planning Data Platform (main) application, so this tutorial will help you get familiar and will also give you insight into how data is loaded into the platform's database.

1. Clone the projects:  

```
git clone https://github.com/digital-land/digital-land.info.git 

git clone https://github.com/digital-land/digital-land-postgres.git 
```

2. Go into the cloned directory -> cd  digital-land-postgres 

3. Download postgres on wsl: 

    sudo apt-get install postgresql 

To get postgis extension: `sudo apt install postgis postgresql-14-postgis-3 `

4. Try setting the password for postgres user: sudo passwd postgres 

5. Using psql:  

    - To start the service, type: sudo service postgresql start 

    - To connect to postgres, type: sudo -u postgres psql 

6. Create virtual environment as mentioned above 

7. To load data:  

    Copy the file task/.env.example to task/.env 

    Note: To open visual studio code through terminal : code . 

 

8. install requirements
    -`cd tasks`

    - `pip install -r requirements.txt`

9. Run: ./load_local.sh 

    Note: If this doesn’t work, run `source .env` and then `./load_local.sh` again. If still S3_KEY is empty, add export in front of variables in .env file and repeat steps. 

10. Exit out and go to cd digital-land/digital-land.info 

11. Create a virtualenv as defined above, then copy .env.example to .env 

12. To install dependencies, run: make init 

For make init to run, you might need npm, node, etc installed. 
Follow the errors and install as instructed.  

13. Follow step 5 to run psql and then run: create database digital_land 

14. Run DB migration script: python -m alembic upgrade head 

15. In digital-land-postgres, Update the S3_KEY in the .env file to S3_KEY=entity-builder/dataset/entity.sqlite3 

16. Then, Run `./load_local.sh` again (loaded data in entity table at this step)  

17. In digital_land-info, Run: `make server `

The application should be up and running. 