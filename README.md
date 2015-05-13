# Shake Hack

Fall 2014 NuPIC Hackathon

![Earthquakes in California](http://oxtopus.github.io/shakehack/map.jpg "Earthquakes in California")

- Colors map to anomaly score
  - Red: High anomaly score
  - Green: Low anomaly score
- Size of dot maps to magnitude
- 10 years of earthquake data (lat, long, magnitude) for the 1000km radius surrounding the Pinger, In. headquarters in San Jose, CA.
- Used coordinate encoder

[See the video!](https://drive.google.com/a/numenta.com/file/d/0B7hpsypiwZ_UNFRPNUFiaGZGejQ/view?usp=sharing)

## Requirements

- [NuPIC](https://github.com/numenta/nupic)
- [Redis](http://redis.io/) running locally
- Python, and [dependencies](requirements.txt)
- [Google Maps Javascript API Key](https://developers.google.com/maps/documentation/javascript/tutorial#api_key)

## Usage

- Start redis

  ```bash
  $ redis-server
  ```

- Start `run.py`

  ```bash
  $ python run.py
  ```

- Start webapp

  ```bash
  $ cd webapp
  $ API_KEY=<insert API key here> python serve.py
  ```

- Open [http://localhost:8080](http://localhost:8080) in browser

## Usage (Vagrant + CoreOS + Docker)

Download and install Docker client, Virtualbox, and Vagrant, and then:

```
source env.sh
vagrant up
docker build -t shakehack .
docker run --name shakehack-redis -d -p 0.0.0.0:6379:6379 redis
docker run \
  --name shakehack-server \
  --link shakehack-redis:broker \
  -e REDIS_HOST=broker \
  -e API_KEY=$API_KEY \
  -d \
  -p 0.0.0.0:8080:8080 \
  -w /opt/numenta/shakehack/webapp \
  shakehack \
  python serve.py
docker run \
  --link shakehack-redis:broker \
  -e REDIS_HOST=broker \
  shakehack \
  python run.py
```

Redis, the shakehack web service, and the shakehack entry point are now running
in separate containers in a vm.  You should be able to access the web service
in a browser at [http://localhost:8080](http://localhost:8080)

## TODO

This project is a work in progress.  The initial mechanics of running data
through NuPIC and presenting it to the user are there, but there's still much
left to do to add value.  Here's a sampling of some ideas:

- [ ] Create encoding scheme that better represents the magnitude of an
      earthquake event.  Currently using the coordinate encoder as-is, mapping
      magnitude to radius one-to-one, but there's likely a better encoding
      scheme that takes into account the logarithmic scale of the magnitude.
      May also be some benefit to incorporating depth into the model.
- [ ] Make use of anomaly likelihood algorithm to classify events and/or
      incorporate additional traditional statistical models
- [ ] Automated cluster classification
- [ ] Additional user interactivity to explore events and replay periods of
      time
- [ ] Split data into training and test data based on variety of factors
      (bounding box, time, magnitude, etc.), save model on trained data set,
      load and replay new data
- [ ] Add a listener to
      http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php for
      real-time(ish) updates
- [ ] Display only a buffer of recent events rather than all accumulated.
      Maybe make the buffer size dynamic based on moving average.

