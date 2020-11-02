# Covid-19 French attestator - October 2020 version

## Work in progress
- Done
  - updated png background
  - updated coordonates of text, checkboxes and small QR code
- To do 
  - Add the new reason checkboxes
  - update QR encoding to match latest model used by govt.


## How to use?

Make sure you have Python 3 installed, with the `reportlab` package available.
`python3 -m pip install reportlab` should do.

Edit the top of the `attestator.py` file to fill in your personal information,
then simply run the script and answer its questions.

## Jupyter version

A jupyter-based GUI is available. Make sure you have jupyter and ipywidgets
installed. `python3 -m pip install jupyter ipywidgets`, then open and run
`attestator-gui.ipynb`.

Alternatively, the GUI can be launched with voila.
`python3 -m pip install voila`, then `voila attestator-gui.ipynb` or execute
`run.sh`.
