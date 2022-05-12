# LSE_tutor

The dockerfile lse_tutor.docker defines a container that encapsulates a web app to run the LSE configuration tutor.

To build the image, execute

docker build -f lse_tutor.docker -t lse_tutor .

when located in the main directory of this repository.

To run the container

docker run -it --rm -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -p 8050:8050 --device /dev/video0 lse_tutor /bin/bash -c 'cat /lse_tutor.readme.txt; cd /lse_tutor; python3 app.py 0.0.0.0'

The web server starts and to connect to it go to http://0.0.0.0:8050/ in a tab in your browser.
