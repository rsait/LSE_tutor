# LSE_tutor

The dockerfile lse_tutor.docker defines a container that encapsulates a web app to run the LSE configuration tutor.

To build the image, execute

```bash
docker build -f lse_tutor.docker -t lse_tutor .
```

when located in the main directory of this repository.

To run the container

```bash
docker run -it --rm -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -p 8050:8050 --device /dev/video0 lse_tutor /bin/bash -c 'cat /lse_tutor.readme.txt; cd /lse_tutor; python3 app.py 0.0.0.0'
```

The web server starts and to connect to it go to http://0.0.0.0:8050/ in a tab in your browser.


### Usage

The application is divided in two different functionalities: *LEARN CONFIGURATIONS* and *PRACTICE CONFIGURATIONS WITH SIGNS*.

1. *LEARN CONFIGURATIONS*: 

After choosing which configuration to practice and with which hand, the image and 3d plot of the chosen configuration is displayed as shown in the image below. 

![plot1](/images/app1.png)

You have to try to reproduce the configuration. If you perform it wrongly, a message is displayed indicating that your performance is incorrect and which configuration the system thinks you are performing instead.

A record of the performance is also saved and you can access it by pressing `PERFORMANCE SUMMARY` button. The percentages of the correct and incorrect performances are displayed, along with the ten most confusing configurations. 

![plot2](/images/app2.png)

2. *PRACTICE CONFIGURATIONS WITH SIGNS*

There is also the opportunity to practice the configurations corresponding to different signs. You can choose a category on the first dropdown and a sign corresponding to that category on the second dropdown. When a sign is chosen, the sorted configurations sequence that must be performed for that sign is shown.

![plot3](/images/app3.png)

To indicate which configuration to perform next a red background is set and once it is correctly performed the background is changed to green and the red background is switched to the next one.

![plot4](/images/app4.png)