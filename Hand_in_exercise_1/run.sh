#!/bin/bash

echo "Program Started!"

echo "Creating a plotting directory if there isn't one."
if [ ! -d "plots" ]; then
  echo "Directory does not exist create it!"
  mkdir plots
fi

echo "Running Prob.1 a) ..."
python3 poisson.py

echo "Running Prob.1 b) ..."
python3 random_generator.py

echo "Running Prob.2 a) ..."
python3 integration.py

echo "Running Prob.2 b) ..."
python3 interpolation.py

echo "Running Prob.2 c) ..."
python3 differentiation.py

echo "Running Prob.2 d) ..."
python3 sampling.py

echo "Running Prob.2 e) ..."
python3 log_hist.py

echo "Running Prob.2 f) ..."
python3 root_finding.py

echo "Running Prob.2 g) ..."
python3 sorting.py

echo "Running Prob.2 h) ..."
python3 trilinear_interp.py

# code that makes a movie of the movie frames
#ffmpeg -framerate 25 -pattern_type glob -i "plots/snap*.png" -s:v 640x480 -c:v libx264 -profile:v high -level 4.0 -crf 10 -tune animation -preset slow -pix_fmt yuv420p -r 25 -threads 0 -f mp4 sinemovie.mp4

echo "Generating the pdf"

pdflatex nur_handin1.tex
bibtex nur_handin1.aux
pdflatex nur_handin1.tex
pdflatex nur_handin1.tex
