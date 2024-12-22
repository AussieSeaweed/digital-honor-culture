# Results

## Personal Attack Detection

- ConvoKit's ``conversations-gone-awry-corpus`` contains human-annotated field ``comment_has_personal_attack`` that denotes whether the utterance (i.e. post) contains a personal attack or not.
- Utterances were shuffled and then performed 80/20 train-validation-split.
- OpenAI fine-tuning.
  - Hyperparameters:
    - Base model: gpt-4o-mini-2024-07-18
    - Epochs: 1
    - Batch size: 16
    - LR multiplier: 1.8
    - Seed: 2054542473
  - Training data:
    - Trained tokens: 3088540
    - Training loss: 0.0000
- Validation
  - Accuracy: 98.75%
  - Precision: 89.31%
  - Recall: 93.69%
  - F1-score: 91.45%
  - Confusion matrix values:
    - Total: 6004
    - Actual positive: 428
    - Actual negative: 5576
    - Predicted positive: 449
    - Predicted negative: 5555
    - True positive: 401
    - False positive: 48
    - True negative: 5528
    - False negative: 27

## US State Classification

- Southern and Northern states defined as in Nisbett & Cohen (1996).
  - Southern states are in [US census region 3 (Division 5, 6, and 7)](https://hcup-us.ahrq.gov/figures/nis_figure2_2021.jsp), excluding DC.
  - Northern states are all the rest except DC (and we assume also except Hawaii and Alaska).
- A user is associated with a state by being a member of the state-related subreddit (e.g. r/Texas).
  - We filter for users who are only a member of a single state-related subreddit.

## Metrics

- Aggression
  - Rate: (# their posts with personal attacks) / (# their posts)
  - Count: # users with at least 1 post.
- Response
  - Rate: (# their responses to personally-attacking replies to their posts) / (# personally-attacking replies to their posts)
  - Count: # users with at least 1 personally-attacking reply to their post.
- Retaliation
  - Rate: (# their personally-attacking responses to personally-attacking replies to their posts) / (# their responses to personally-attacking replies to their posts)
  - Count: # users with at least 1 response to personally-attacking replies to their posts.
