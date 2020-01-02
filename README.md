# Cookie Clicker by Team POGGERS

**Roster/Roles**
- Kelvin Ng: Project Manager
- Tanzim Elahi
  - Backend (database) or frontend (templates, routes, styling with Bootstrap) [pick one]
- Kevin Li
  - Interfacing with the API to retrieve the necessary data
  - Backend (database) or frontend (templates, routes, styling with Bootstrap) [pick one]
- Justin Shaw
  - JavaScript necessary for clicking the cookie and purchasing perks
  
## Website Description
Leaderboard data is fetched from the [speedrun.com REST API](https://docs.google.com/document/d/1Hk-0V1E2hvxjx1BrCcwk33yCHaMnbO_hza4GzxjVcZM).

This website is a recreation of [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) with the skills we've learned over the course of this semester. Clicks will function as the currency of this game. Currency may be used to purchase perks such as autoclickers. An account will be required so that progress can be saved. There will also be a leaderboards page so that you can compare your ability with others. One section is for comparing stats with other users of the website, and another will be for comparing with top players, whose data will be sourced from the speedrun.com API.

## Instructions for running this project

**Dependencies**

You must install the pip modules listed in the /doc/requirements.txt file. To do so, install them in a Terminal with:
```bash
pip install -r <location of requirements.txt file>
```

The -r flag is necessary to distinguish it from a typical pip install. Without the -r, pip will look for a package online called "requirements.txt". That is obviously not desirable. 

Note that on certain systems (like the school computers), the pip command may be restricted. To get around this, create a virtual environment with:
```bash
python3 -m venv <name_of_venv>
```
*Note that if your system only has Python 3 installed, just remove the 3 from the above command.*

To activate the virtual environment, cd into the directory you created the environment in, and run the "activate" file. Now, you should be able to pip install the requirements. To deactivate the environment, run the "deactivate" file.  

**Run the program**

After installing the required dependencies, all you need to do to run the program is to type into a terminal session: 
```bash
python3 app.py
```
*Again, remove the 3 after the "python" if necessary.*
