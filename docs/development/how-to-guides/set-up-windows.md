# Setting up on Windows

1. Download Windows Terminal [Windows Terminal installation | Microsoft Learn] (https://learn.microsoft.com/en-us/windows/terminal/install)

2. Install Ubuntu on windows
   `wsl –install`

3. From Terminal, run:

   ```
   sudo apt update (install latest updates)

   sudo apt install python3.10

   sudo apt install python3-pip

   sudo apt-get install sqlite3
   ```

4. Clone the required Projects, example:
   `git clone https://github.com/digital-land/central-activities-zone-collection`

5. Go into the cloned directory -> cd central-activities-zone-collection

6. Creating a virtual environment:

- To create a new python environment, type:

  `python3 -m venv --prompt . .venv --clear --upgrade-deps`

-To activate the environment, type:

    `source .venv/bin/activate`

7. To install the make package, enter:

    `sudo apt install make`

8. Updating the collection:
    ```
    make makerules

    make init

    make collect

    make 
    ```

## Setting Up `digital_land_postgres` and `digital_land.info` Projects Locally

### 1. Clone the Projects

git clone https://github.com/digital-land/digital-land.info.git  
git clone https://github.com/digital-land/digital-land-postgres.git

### 2. Go into the cloned directory

cd digital-land-postgres

### 3. Install PostgreSQL and PostGIS on WSL

sudo apt-get install postgresql  
sudo apt install postgis postgresql-14-postgis-3

### 4. Set Password for `postgres` User

sudo passwd postgres

### 5. Using `psql`

- Start the PostgreSQL service:

  sudo service postgresql start

- Connect to PostgreSQL:

  sudo -u postgres psql

### 6. Create a Virtual Environment

Follow your standard procedure for creating a virtual environment.

### 7. Load Data

- Copy the example `.env` file:

  cp task/.env.example task/.env

- (Optional) Open VS Code from terminal:

  code .

### 8. Install Python Dependencies

cd task  
pip install -r requirements.txt

### 9. Run the Local Loader Script

./load_local.sh

> **Note:**  
> If this doesn’t work:  
> - Run `source .env`  
> - Then `./load_local.sh` again  
> - If `S3_KEY` is still empty, add `export` before each variable in the `.env` file and repeat the steps.

### 10. Switch to the `digital-land.info` Project

cd ../digital-land.info

### 11. Set Up Virtual Environment and Env File

- Create a virtual environment as above  
- Copy the example `.env` file:

  cp .env.example .env

### 12. Install Frontend and Backend Dependencies

make init

> You may need `npm`, `node`, etc. If there are errors, install dependencies as instructed.

### 13. Create Database

- Run `psql` (as in Step 5), then:

  create database digital_land;

### 14. Run Database Migrations

python -m alembic upgrade head

### 15. Update `.env` in `digital-land-postgres`

Edit `.env` and set:

for e.g. 
export S3_OBJECT_ARN=arn:aws:s3:::digital-land-production-collection-dataset/central-activities-zone-collection/dataset/central-activities-zone.sqlite3

### 16. Run Local Loader Script Again

./load_local.sh

> This loads data into the `entity` table.

### 17. Start the Server from `digital-land.info`

make server

The application should now be up and running.
