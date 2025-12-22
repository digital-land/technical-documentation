---
title: Setting up a Mac for use on our project
---

This tutorial aims to walk you through a lot of the base level requirements you need to work on the majority of our code base. Our codebase spans a lot and this attempts to just install the essential parts that are generally needed. There may be app specific requirements on top of this but this is a good place to start when joining the project.

This is aimed at beginners so may be more detailed than needed for experienced devs. It can still act as a list of things to get set up. Our How-to guides might be more useful to install the bits that you need.

Contents:

* Creating a .zshrc file
* Install Homebrew 
* Install Make
* Install sqlite3
* Install Python (and understand venvs)
* Set up SSH for Github

### Create .zshrc file

Before we start installing software it's very useful to create a .zshrc file. Because Macs now use zsh terminals as the default we need to create a .zshrc file and NOT a .bashrc or .bash_profile. 

These files are run before you open each terminal so they can be used to configure the environment of the terminals you open.

To create the .zshrc file you can run

```
touch ~/.zshrc
```

The ~ above automatically locates to your user file and means you don't need to type the absolute path every time.

Further on in this tutorial you'll be asked to add lines to your .zshrc file for various reasons. There are two main methods.

First of all you can open the file and edit as a normal text file. This is easiest by running the below command as . files are hidden from a lot of file explorers such as Finder.

```
open -e ~/.zshrc
```

This will open a text editor window and allow you to edit the file in the GUI. This is great if you don't want to use a command line editor.

Next if you just need to add a line to the end of the file and don't want to open it you can run the following command to add text to a new line. 

```
echo 'alias hellp="echo hello"' >> ~/.zshrc
```

After changing the .zshrc file you'll either need to restart your terminal or you can source it using the below command

```
source ~/.zshrc
```

### Install Homebrew

When installing the majority of software on Mac, Homebrew is a very nice to use piece of software. For Mac it mimics the capability of package managers in Linux allowing us to easily install software on the command line. 

It has some limitations when it comes to the versions of certain software and there may be better programs out there to use. This is worth keeping in mind and perhaps updating the parts of this guide that use brew in the future. For now it is usable and gets us what we need.

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installing Homebrew it should be updated

```sh
brew update
```

### Install Make

Make is used through our code base to quickly and easily run data processing tasks or set up application specific environments. Macs come with version 3.81 of make already installed however we need more recent versions above 4.x.x. There's a mixture of reasons Apple does this (licensing, backwards compatibility, etc.).

To install make we can use brew:

```
brew install make
```

Because there is already a version of make on your computer this version of make is available under gmake instead. You can see this by comparing the versions of make and gmake

```
make --version
```

and 

```
gmake --version
```

In our scripts we generally only call make so this can be problematic. When you installed make using brew it will have printed a statement giving you a piece of script to add to your .zshrc. For me this was `PATH="/usr/local/opt/make/libexec/gnubin:$PATH"` but it may be different depending on the Mac you have. It's worth checking against the output returned when installing make. To add this to your .zshrc you can run

```sh
echo 'PATH="/usr/local/opt/make/libexec/gnubin:$PATH"' >> ~/.zshrc
```

### Install sqlite3
3.43.2 2023-10-10 13:08:14 1b37c146ee9ebb7acd0160c0ab1fd11017a419fa8a3187386ed8cb32b709aapl (64-bit)
Mac already has a version of sqlite installed, unfortunately we can't rely on this as it doesn't allow for extensions. We use spatialite with our coding which is an extension for Geospatial querying.

Luckily for us it's very easy to install with Homebrew just run

```sh
brew install sqlite3
```

> Tip: Do this before installing Python so that Python allows extensions with sqlite as otherwise even if sqlite3 allows them Python may not.

### Install Python & Understand Virtual Environments

The majority of our code base is Python. Therefore we recommend everyone installs it at some point and understands how to create a virtual environment as it's often a dependency of the repo.

#### Installing Python 3.9
To install Python 3.9 specifically, run:

```sh
brew install python@3.9
```

After installation, verify the installation:

```sh
python3.9 --version
```

Notice how the version number is required, this is how Homebrew installs different versions.

> Tip: It's easy to remove Python versions using brew by running `brew uninstall python3.9`. If you've installed Python prior to installing a newer version of sqlite you may need to do this and re-install after installing sqlite

#### Installing Other Python Versions
Homebrew allows installing multiple Python versions. This is useful when working across different repos that use different Python versions. To install other versions, use:

```sh
brew install python@3.10   # Install Python 3.10
brew install python@3.8    # Install Python 3.8
```

To use different versions just call them by version

```sh
python3.10 --version
python3.9 --version
```

#### Using Virtual Environments
A **virtual environment** (often called venv) isolates dependencies for different Python projects, preventing conflicts between package versions. They can be made and destroyed very quickly and all our repos which use Python expect you to be able to make them

##### Creating a Virtual Environment
To create a virtual environment using Python 3.9:

```sh
python3.9 -m venv --prompt . .venv --clear --upgrade-deps
```

Arguments:

* `--prompt` - allows you to change the name of the virtual environment once you've loaded into it (the name that appears in brackets on the command line)
* `--clear` - if a venv already exists then it is emptied and reset but the folder is not deleted
* `--upgrade-deps` - updates pip and setup tools when a venv is created

##### Activating a Virtual Environment
Run the following command to activate the environment once it has been created:

```sh
source .venv/bin/activate
```

Once activated, you should see the environment name in your shell prompt, indicating that the virtual environment is in use.

##### Deactivating the Virtual Environment
To exit the virtual environment once it's been activated, run:

```sh
deactivate
```

##### Aliases for Creating Virtual Environments
You'll need to be able to quickly create and activate venvs in this project. To simplify virtual environment creation, add these aliases to your `.zshrc` file:

```sh
alias workon='source .venv/bin/activate'
alias mkvirtualenv3.9='python3.9 -m venv --prompt . .venv --clear && workon'
alias mkvirtualenv3.10='python3.10 -m venv --prompt . .venv --clear --upgrade-deps && workon'
```

Now you can create a new virtual environment with:

```sh
mkvirtualenv3.9
```

or activate an already created venv using

```sh
workon
```

You see in the aliases above that workon is used in the mkvirtualenv aliases to automatically activate a venv after creating one

> Tip: If you're using more versions of Python the aliases above can easily be edited to different versions by simply changing the version of Python which is being called

### Set up SSH for Github

Our code base is all contained within Github and is publicly available. If you want to start downloading and looking at the code without pushing any changes then you won't need to set this up.

When making changes to code if you've downloaded via https it will require you to enter your Github user details each time. While this is doable it can slow development down so we advise using ssh when working on our code base to make changes to Github repositories.

This requires some additional set up and there are a couple of extra steps on Mac compared to Linux.

There are a number of guides on the internet for this that may be better kept than this page don't be scared to use them:

* https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent
* https://medium.com/codex/git-authentication-on-macos-setting-up-ssh-to-connect-to-your-github-account-d7f5df029320
* https://swiftlogic.io/posts/connecting-to-gitHub-with-ssh/

This is aimed at the Mac machines provided to us rather than the general cases above

#### Check that you have git installed

On Mac this generally comes bundled with Xcode, it mmay be that this is aready installed but often it may not be or an update caused it to be removed.

you can check if github is installed by checking the version

```sh
git --version
```


if you get a version numberr then git is installed. this looks like this (it may be a more recent version)

```sh
git version 2.39.1
```

however you may get an error like the foowing

```sh
xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
```

if this appears you can install xcode by running

```sh
xcode-select --install
```

A window will pop up and guide your though the installation

#### Create a Github account and have it added to the digital land organisation

Before we do anything you need to have a github account to add the ssh key to. Github accounts are free and you can set this up yourself.

you're welcome to use a github acount that you already have to keep track of the projects your working on but you MUST remmove any  personal access tokens.

Otherwise we suggest creating an account with the communities email address provided to you.

Once it's created reach out to the infastructure team who can get you added to the organisation with the correctt privalages. It will be good to innclude the team lead from the team your joining in this message so any questions can be asked/answered by them.

#### Generate an SSH key

It's expected that there are no ssh keys already on your computer but this can be checked using the following command

```
ls -al ~/.ssh
```

Given that we're assuming it's a fresh laptop we expect the following error to be raised

```
No such file or directory
```

If it does bring up a list of keys:

```
id_rsa
id_rsa.pub
id_ed25519
id_ed25519.pub
```

If you have keys then you've likely done this before. You're welcome to use one of your other keys especially if it's for other MHCG projects but we advise creating a new key for this particular project.

To generate an ssh key use the below command, replacing your email with that on your Github account

```
ssh-keygen -t ed25519 -C "your_email@example.com"
```

You will be prompted to enter a file to save the key under press enter to use the default name

```
> Enter a file in which to save the key (/Users/YOU/.ssh/<id_ALGORITHM>): [Press enter]
```

As there are no keys we can use the default name, if you wanted to use a different name you can replace `<id_ALGORITHM>` with the name of your key

Next you'll be asked to use a passphrase for your ssh key, leave blank by hitting enter twice. Passphrases can be set up and added to your keychain but extra configuration is needed.

This should produce an output similar to:

```
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/yourusername/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /Users/yourusername/.ssh/id_rsa
Your public key has been saved in /Users/yourusername/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:AbCdEfGhIjKlMnOpQrStUvWxYz1234567890 your_email@example.com
The key's randomart image is:
+---[RSA 4096]----+
|    .+o**o+      |
|   . +oE+oo      |
|    o   o +      |
|   o o   + o     |
|  . + = S .      |
|   o o X .       |
|    + X O        |
|     = O .       |
|      .o.        |
+----[SHA256]-----+
```

#### Add the ssh key to the ssh agent 

This is a Mac specific step that needs to be done so that when ssh is used it is able to find your ssh key.

Start the ssh agent in the background

```
exec ssh-agent zsh
```

Then run 

```
ssh-add ~/.ssh/id_ed25519
```

The output should indicate that the key has been added to the agent

#### Add your SSH Key to your Github Account

The final step is to take the public key and add it to your Github account. This can be done by copying the key to your clipboard. The below command does this for you

```
pbcopy < ~/.ssh/id_ed25519.pub
```

Now it needs to be added to your Github account:

* Log into Github
* On the top right click on your profile picture
* In the menu that comes up click on settings
* On the left go to SSH and GPG keys
* Give it a name so you recognize which computer it's from
* Leave the key type as authentication key
* Use command + v to copy the key into the box
* Click the add ssh key

Now you should see that the ssh key has been added to your Github account.
You're all set! Test the key by cloning a Github repository and pushing a test branch to one.