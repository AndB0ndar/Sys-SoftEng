# Web Queue

Project for the subject of system and software engineering of the RTU MIRIE

# Running

To run the program, you need to build and run *docker-compose*
```
docker-compose build
docker-compose up
```

And the site will be launched at http://0.0.0.0:8000/

# Create documentation

To generate documentation, go to the appropriate directory:

```
cd web_queue/docs/
```

## html

To generate HTML documentation, run the command:

```
make html
```

As a result, html documentation will be created in the ***build/html*** directory.
You can open the file *index.html* to view it.

## pdf

To generate PDF documentation, run the command:

```
make latexpdf
```

As a result, pdf documentation will be created in the ***build/latex*** directory.
You can open the file *webqueue.pdf* to view it.

**NOTE**: To create PDF documentation you will need to install the appropriate latex packages.
For example (on Ubuntu):
```
sudo apt-get install texlive‑latex‑recommended texlive‑fonts‑recommended texlive‑latex‑extra latexmk
```
