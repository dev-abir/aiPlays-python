# AI plays-python

A simple flappy bird game, where the player is AI.

A flock of birds will try to survive in this game (rather environment), the best ones will continue, rest will die. Much like our evolution :)

It uses the concept of Evolutionary artificial neural networks (EANNs), or Evolving Neural Networks. I did this project mainly to get some idea of neural networks, machine learning in a somewhat interesting way. I used [this](https://towardsdatascience.com/evolving-neural-networks-b24517bb3701) article a lot, and also studied some free content whatever I could get on the internet :)

Wrote this a couple of months back, around May and uploading this on November. There are places, where this codebase can be improved.... Suggestions, bug-reports, bug-fixes are always welcome :)

## How to play

Assuming that you have `python` installed properly...

1. Clone this repo or use the code button in github and download the zip ([see this](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository))

2. Create a virtual environment (recommended), so that there will be no conflicts between previously installed packages and the packages we will install now. At first `cd` into the downloaded repo, then issue the command: `python3 -m pip venv`

3. Depending on the OS, the command to activate your virtual environment will be: `.\venv\Scripts\activate.ps1` (issue a PR if something is wrong here) or `source venv\bin\activate`
(On closing the terminal the virtual environment will be gone, you should do step 3 again)

4. To install libraries used in this project, issue the command: `pip install -r requirements.txt`

5. Last step: `python main.py`

6. **Use UP and DOWN arrow to increase the speed of the simulation and vice-versa.**

7. To change settings, like resolution etc, edit the `settings.py` file.
