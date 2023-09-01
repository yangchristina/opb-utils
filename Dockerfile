FROM prairielearn/grader-r

# Install R packages
RUN Rscript -e "install.packages('openintro')"
