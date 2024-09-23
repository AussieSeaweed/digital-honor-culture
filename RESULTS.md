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
  - Experiment 1: [See map](https://www.270towin.com/maps/eKQBG)
    - Southern states are in [US census region 3 (Division 5, 6, and 7)](https://hcup-us.ahrq.gov/figures/nis_figure2_2021.jsp), excluding DC.
    - Northern states are all the rest except DC (and we assume also except Hawaii and Alaska).
  - Experiment 2: [See map](https://www.270towin.com/maps/8jrkQ)
    - Southern states are states with Southernness index >25 (same as Exp. 1 except Maryland & Delaware but with Arizona and New Mexico) plus Missouri and Nevada.
    - Northern states are all the rest except DC (and we assume also except Hawaii and Alaska).
  - Experiment 3: [See map](https://www.270towin.com/maps/07BZO)
    - Southern states are states with Southernness index >25 (same as Exp. 1 except Maryland & Delaware but with Arizona and New Mexico) plus Missouri, Nevada, Kansas, Colorado, Maryland.
    - Northern states are all the rest except DC (and we assume also except Hawaii and Alaska).
- A user is associated with a state by being a member of the state-related subreddit (e.g. r/Texas).

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

## Summary

- Experiment 1: Southern states are in US census region 3, excluding DC.
  - Northerner if the user joined more Northern-state-related subreddits than Southern-state-related subreddits (and vice versa) -- mutually exclusive.
    - North:	AGG	7.43%	(25553)	RESP	46.30%	(7038)	RET	19.65%	(4551)
    - South:	AGG	7.60%	(12085)	RESP	46.23%	(3180)	RET	19.24%	(2041)
  - Northerner if the user joined at least one Northern-state-related subreddit (and vice versa) -- not mutually exclusive.
    - North:	AGG	7.58%	(28966)	RESP	46.45%	(8064)	RET	19.46%	(5226)
    - South:	AGG	7.84%	(16690)	RESP	46.53%	(4577)	RET	19.39%	(2971)
  - Northerner if the user joined only one Northern-state-related subreddit and zero Southern-state-related subreddit (and vice versa) -- mutually exclusive.
    - North:	AGG	7.20%	(20281)	RESP	45.74%	(5375)	RET	19.28%	(3414)
    - South:	AGG	7.45%	(10627)	RESP	46.25%	(2739)	RET	19.41%	(1754)
  - Northerner if the user joined only Northern-state-related subreddits and zero Southern-state-related subreddit (and vice versa) -- mutually exclusive.
    - North:	AGG	7.37%	(23805)	RESP	46.26%	(6486)	RET	19.50%	(4171)
    - South:	AGG	7.53%	(11529)	RESP	46.15%	(2999)	RET	19.43%	(1916)
- Experiment 2: Southern states have Southernness index >25 plus Missouri and Nevada.
  - Northerner if the user joined more Northern-state-related subreddits than Southern-state-related subreddits (and vice versa) -- mutually exclusive.
    - North:	AGG	7.37%	(25236) RESP	46.18%	(6948) RET	19.64%	(4477)
    - South:	AGG	7.63%	(12283) RESP	46.41%	(3217) RET	19.10%	(2075)
  - Northerner if the user joined at least one Northern-state-related subreddit (and vice versa) -- not mutually exclusive.
    - North:	AGG	7.57%	(28823) RESP	46.31%	(8046) RET	19.53%	(5201)
    - South:	AGG	7.93%	(16963) RESP	46.60%	(4660) RET	19.54%	(3036)
  - Northerner if the user joined only one Northern-state-related subreddit and zero Southern-state-related subreddit (and vice versa) -- mutually exclusive.
    - North:	AGG	7.16%	(20148) RESP	45.63%	(5355) RET	19.25%	(3393)
    - South:	AGG	7.52%	(10760) RESP	46.46%	(2759) RET	19.46%	(1775)
  - Northerner if the user joined only Northern-state-related subreddits and zero Southern-state-related subreddit (and vice versa) -- mutually exclusive.
    - North:	AGG	7.31%	(23532) RESP	46.20%	(6403) RET	19.39%	(4106)
    - South:	AGG	7.57%	(11672) RESP	46.53%	(3017) RET	19.25%	(1941)
- Experiment 3: Southern states have Southernness index >25 plus Missouri, Nevada, Kansas, Colorado, Maryland.
  - Northerner if the user joined more Northern-state-related subreddits than Southern-state-related subreddits (and vice versa) -- mutually exclusive.
    - North:	AGG	7.36%	(22188) RESP	45.87%	(6094) RET	19.63%	(3924)
    - South:	AGG	7.56%	(15165) RESP	46.53%	(4021) RET	19.22%	(2592)
  - Northerner if the user joined at least one Northern-state-related subreddit (and vice versa) -- not mutually exclusive.
    - North:	AGG	7.61%	(26177) RESP	46.34%	(7312) RET	19.49%	(4736)
    - South:	AGG	7.82%	(19847) RESP	46.85%	(5474) RET	19.52%	(3563)
  - Northerner if the user joined only one Northern-state-related subreddit and zero Southern-state-related subreddit (and vice versa) -- mutually exclusive.
    - North:	AGG	7.18%	(17960) RESP	45.45%	(4772) RET	19.28%	(3021)
    - South:	AGG	7.44%	(12948) RESP	46.56%	(3342) RET	19.38%	(2147)
  - Northerner if the user joined only Northern-state-related subreddits and zero Southern-state-related subreddit (and vice versa) -- mutually exclusive.
    - North:	AGG	7.32%	(20648) RESP	45.90%	(5589) RET	19.38%	(3579)
    - South:	AGG	7.49%	(14318) RESP	46.43%	(3751) RET	19.38%	(2406)
