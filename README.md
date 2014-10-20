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
