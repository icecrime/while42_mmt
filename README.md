Metrics Meta Talk
=================

Demo sources and presentation file for a talk given at [While 42](http://www.while42.org)
Paris on July 8th, 2014.

Concept
-------

This is an experiment about giving a talk on metrics by demoing live data of
the ongoing talk itself (how meta is that?).

<p align="center">
  <img src="https://github.com/icecrime/while42_mmt/blob/master/resources/xzibit.jpg?raw=true"/>
</p>

It currently catches:

- Sound data: per second RMS / min / max from a microphone
- Twitter data: speaker follower count, conference hashtag
- Apple Keynote events: slide changes are pushed to be used as annotations in
the graphs.

Usage
-----

- Build the Docker image:
      `docker build -t icecrime/while42_mmt docker`
- Run a Docker container:
      `docker run --rm -ti -p 8080:80 -p 8125:8125/udp icecrime/while42_mmt`
- Start the feeding process:
      `python feeder/main.py`
