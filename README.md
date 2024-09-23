# Digital Honour Culture

Extract speakers from relevant subreddits (for detecting aggressions and US states).

```console
python speakers.py subreddit-changemyview data/speakers-change-my-view.jsonl

python speakers.py subreddit-Alabama data/speakers-alabama.jsonl
python speakers.py subreddit-alaska data/speakers-alaska.jsonl
python speakers.py subreddit-arizona data/speakers-arizona.jsonl
python speakers.py subreddit-Arkansas data/speakers-arkansas.jsonl
python speakers.py subreddit-California data/speakers-california.jsonl
python speakers.py subreddit-Colorado data/speakers-colorado.jsonl
python speakers.py subreddit-Connecticut data/speakers-connecticut.jsonl
python speakers.py subreddit-Delaware data/speakers-delaware.jsonl
python speakers.py subreddit-florida data/speakers-florida.jsonl
python speakers.py subreddit-Georgia data/speakers-georgia.jsonl
python speakers.py subreddit-Hawaii data/speakers-hawaii.jsonl
python speakers.py subreddit-Idaho data/speakers-idaho.jsonl
python speakers.py subreddit-illinois data/speakers-illinois.jsonl
python speakers.py subreddit-Indiana data/speakers-indiana.jsonl
python speakers.py subreddit-Iowa data/speakers-iowa.jsonl
python speakers.py subreddit-kansas data/speakers-kansas.jsonl
python speakers.py subreddit-Kentucky data/speakers-kentucky.jsonl
python speakers.py subreddit-Louisiana data/speakers-louisiana.jsonl
python speakers.py subreddit-Maine data/speakers-maine.jsonl
python speakers.py subreddit-maryland data/speakers-maryland.jsonl
python speakers.py subreddit-massachusetts data/speakers-massachusetts.jsonl
python speakers.py subreddit-Michigan data/speakers-michigan.jsonl
python speakers.py subreddit-minnesota data/speakers-minnesota.jsonl
python speakers.py subreddit-mississippi data/speakers-mississippi.jsonl
python speakers.py subreddit-missouri data/speakers-missouri.jsonl
python speakers.py subreddit-Montana data/speakers-montana.jsonl
python speakers.py subreddit-Nebraska data/speakers-nebraska.jsonl
python speakers.py subreddit-Nevada data/speakers-nevada.jsonl
python speakers.py subreddit-newhampshire data/speakers-new-hampshire.jsonl
python speakers.py subreddit-newjersey data/speakers-new-jersey.jsonl
python speakers.py subreddit-NewMexico data/speakers-new-mexico.jsonl
python speakers.py subreddit-newyork data/speakers-new-york.jsonl
python speakers.py subreddit-NorthCarolina data/speakers-north-carolina.jsonl
python speakers.py subreddit-northdakota data/speakers-north-dakota.jsonl
python speakers.py subreddit-Ohio data/speakers-ohio.jsonl
python speakers.py subreddit-oklahoma data/speakers-oklahoma.jsonl
python speakers.py subreddit-oregon data/speakers-oregon.jsonl
python speakers.py subreddit-Pennsylvania data/speakers-pennsylvania.jsonl
python speakers.py subreddit-RhodeIsland data/speakers-rhode-island.jsonl
python speakers.py subreddit-southcarolina data/speakers-south-carolina.jsonl
python speakers.py subreddit-SouthDakota data/speakers-south-dakota.jsonl
python speakers.py subreddit-Tennessee data/speakers-tennessee.jsonl
python speakers.py subreddit-texas data/speakers-texas.jsonl
python speakers.py subreddit-Utah data/speakers-utah.jsonl
python speakers.py subreddit-vermont data/speakers-vermont.jsonl
python speakers.py subreddit-Virginia data/speakers-virginia.jsonl
python speakers.py subreddit-Washington data/speakers-washington.jsonl
python speakers.py subreddit-WestVirginia data/speakers-west-virginia.jsonl
python speakers.py subreddit-wisconsin data/speakers-wisconsin.jsonl
python speakers.py subreddit-wyoming data/speakers-wyoming.jsonl

python speakers.py subreddit-Appalachia data/speakers-appalachia.jsonl
```

Extract utterances from relevant subreddits (for detecting aggressions and validating performance).

```console
python utterances.py subreddit-changemyview data/utterances-change-my-view.jsonl
python utterances.py conversations-gone-awry-corpus data/utterances-conversations-gone-awry.jsonl
```

Create a fine-tuning dataset (for training and detecting aggression detection). Send over the training and validation sets to OpenAI for fine-tuning.

```console
cat data/utterances-conversations-gone-awry.jsonl | shuf > data/utterances-conversations-gone-awry-shuffled.jsonl
cat data/utterances-conversations-gone-awry-shuffled.jsonl | head -n 24017 > data/utterances-conversations-gone-awry-training.jsonl
cat data/utterances-conversations-gone-awry-shuffled.jsonl | tail -n +24018 > data/utterances-conversations-gone-awry-validation.jsonl
python fine-tune.py data/utterances-conversations-gone-awry-training.jsonl data/fine-tune-conversations-gone-awry-training.jsonl
python fine-tune.py data/utterances-conversations-gone-awry-validation.jsonl data/fine-tune-conversations-gone-awry-validation.jsonl
```

Evaluate the validation set and determine the values in the confusion matrix.

```console
python classify.py data/utterances-conversations-gone-awry-validation.jsonl data/classifications-conversations-gone-awry-validation.jsonl [OpenAI-model] [max-workers]
python confusion.py data/utterances-conversations-gone-awry-validation.jsonl data/classifications-conversations-gone-awry-validation.jsonl data/confusion-conversations-gone-awry-validation.jsonl
```

Collect state membership information and get statistics.

```console
echo 'alabama data/speakers-alabama.jsonl
alaska data/speakers-alaska.jsonl
arizona data/speakers-arizona.jsonl
arkansas data/speakers-arkansas.jsonl
california data/speakers-california.jsonl
colorado data/speakers-colorado.jsonl
connecticut data/speakers-connecticut.jsonl
delaware data/speakers-delaware.jsonl
florida data/speakers-florida.jsonl
georgia data/speakers-georgia.jsonl
hawaii data/speakers-hawaii.jsonl
idaho data/speakers-idaho.jsonl
illinois data/speakers-illinois.jsonl
indiana data/speakers-indiana.jsonl
iowa data/speakers-iowa.jsonl
kansas data/speakers-kansas.jsonl
kentucky data/speakers-kentucky.jsonl
louisiana data/speakers-louisiana.jsonl
maine data/speakers-maine.jsonl
maryland data/speakers-maryland.jsonl
massachusetts data/speakers-massachusetts.jsonl
michigan data/speakers-michigan.jsonl
minnesota data/speakers-minnesota.jsonl
mississippi data/speakers-mississippi.jsonl
missouri data/speakers-missouri.jsonl
montana data/speakers-montana.jsonl
nebraska data/speakers-nebraska.jsonl
nevada data/speakers-nevada.jsonl
new_hampshire data/speakers-new-hampshire.jsonl
new_jersey data/speakers-new-jersey.jsonl
new_mexico data/speakers-new-mexico.jsonl
new_york data/speakers-new-york.jsonl
north_carolina data/speakers-north-carolina.jsonl
north_dakota data/speakers-north-dakota.jsonl
ohio data/speakers-ohio.jsonl
oklahoma data/speakers-oklahoma.jsonl
oregon data/speakers-oregon.jsonl
pennsylvania data/speakers-pennsylvania.jsonl
rhode_island data/speakers-rhode-island.jsonl
south_carolina data/speakers-south-carolina.jsonl
south_dakota data/speakers-south-dakota.jsonl
tennessee data/speakers-tennessee.jsonl
texas data/speakers-texas.jsonl
utah data/speakers-utah.jsonl
vermont data/speakers-vermont.jsonl
virginia data/speakers-virginia.jsonl
washington data/speakers-washington.jsonl
west_virginia data/speakers-west-virginia.jsonl
wisconsin data/speakers-wisconsin.jsonl
wyoming data/speakers-wyoming.jsonl
appalachia data/speakers-appalachia.jsonl' | python us-states.py data/speakers-change-my-view.jsonl data/us-states-change-my-view.jsonl data/us-states-change-my-view-statistics.jsonl
```

Classify personal attacks.

```console
python classify.py data/utterances-change-my-view.jsonl data/classifications-change-my-view.jsonl [OpenAI-model] [max-workers]
```

Fetch metrics: aggression, response, and retaliation rates.

```console
python metrics.py data/classifications-change-my-view.jsonl data/us-states-change-my-view.jsonl data/metrics-change-my-view.jsonl
```

Aggregate metrics.

```console
python aggregate.py data/metrics-change-my-view.jsonl data/aggregates-change-my-view.jsonl
```
