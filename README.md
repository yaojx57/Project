# Demo of how to use the MSBG hearing loss moodel

## Install

Run the following to install the clarity code from GitHub into a Python virtual environment

```bash
git clone git@github.com:claritychallenge/clarity.git
python -m venv env
source env/bin/activate
python -m pip install -e clarity
```

## Running the code

Run the code with

```bash
python run_msbg.py speech.wav output.wav
```

You can simulate different degrees of hearing impairment by adjusting the audiogram level values in the source code.

This is just a minimal demo. You will need to extend it if you want to, say, process all of the files in a directory, or to read the audiogram parameters from a file.
