# Setting up DLUCH locally on Windows Machine

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

    make (?)
    ```