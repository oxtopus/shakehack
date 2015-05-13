import csv
from collections import deque, namedtuple
import datetime
import json
import os
import numpy
import redis

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.algorithms.anomaly_likelihood import AnomalyLikelihood
import model_params


WINDOWSIZE = 30 # Number of samples over which to calculate average

earthquakes = deque()

# Need statistics to recompute coords
with open("usgs.csv") as inp:
  csvin = csv.reader(inp)

  Earthquake = namedtuple("Earthquake", next(csvin))

  minLatitude = float("inf")
  maxLatitude = float("-inf")
  minLongitude = float("inf")
  maxLongitude = float("-inf")

  for line in csvin:
    earthquake = Earthquake._make(line)

    # Buffer earthquake events for processing
    earthquakes.append(earthquake)

    lat = float(earthquake.latitude)
    lng = float(earthquake.longitude)

    if float(earthquake.latitude) > maxLatitude:
      maxLatitude = lat

    if float(earthquake.latitude) < minLatitude:
      minLatitude = lat

    if float(earthquake.longitude) > maxLongitude:
      maxLongitude = lng

    if float(earthquake.longitude) < minLongitude:
      minLongitude = lng

  inp.seek(0)
  next(inp)

# Create Model
model = ModelFactory.create(model_params.MODEL_PARAMS)
model.enableInference({"predictedField": "event"})

anomalyLikelihood = AnomalyLikelihood()

scores=deque(numpy.ones(WINDOWSIZE), maxlen=WINDOWSIZE)
likelihoodScores=deque(maxlen=100)

r = redis.Redis(host=os.environ.get("REDIS_HOST", "127.0.0.1"),
                port=int(os.environ.get("REDIS_PORT", 6379)),
                db=int(os.environ.get("REDIS_DB", 0)))

for n, earthquake in enumerate(reversed(earthquakes)):

  x = int(10000 * abs(float(earthquake.longitude) - minLongitude))
  y = int(10000 * abs(float(earthquake.latitude) - minLatitude))

  try:
    event = (numpy.array([x, y]), int(10*float(earthquake.mag)))
    modelInput = {}
    modelInput["event"] = event
    modelInput["timestamp"] = (
      datetime.datetime.strptime(earthquake.time, "%Y-%m-%dT%H:%M:%S.%fZ"))

    result = model.run(modelInput)
    anomalyScore = result.inferences["anomalyScore"]
    scores.append(anomalyScore)
    likelihoodScores.append([modelInput["timestamp"],
                             modelInput["event"],
                             anomalyScore])

    likelihood = anomalyLikelihood.anomalyProbability(
      event[0] + numpy.array([event[1]]),
      anomalyScore,
      modelInput["timestamp"])

    data = {"lat": earthquake.latitude,
            "lng": earthquake.longitude,
            "score": anomalyScore,
            "mag": earthquake.mag,
            "mean": (numpy.mean(scores), WINDOWSIZE),
            "timestamp": earthquake.time,
            "likelihood": likelihood}

    r.publish("nupic", json.dumps(data))
    print data

  except ValueError:
    pass
