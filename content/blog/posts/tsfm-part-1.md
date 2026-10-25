---
date: 2026-10-25
draft: true
authors:
  - yacine
categories:
  - machine-learning
tags:
  - time-series-foundation-models
  - forecasting
---

# Time series foundation models, part 1: how they work

TODO(author): one or two sentences that make a reader want to continue. This text
is the excerpt shown on the blog index, and everything above the marker below is
included in it.

<!-- more -->

## The problem they solve

TODO(author): what forecasting looked like before, and why one model for many series.

A forecasting model maps a history to a future window:

\[
\hat{y}_{t+1:t+H} = f_\theta(y_{1:t})
\]

## How they work

TODO(author): tokenisation or patching, pretraining data, architecture, zero-shot use.

```python
# TODO(author): replace with a real zero-shot forecasting snippet.
forecast = model.predict(history, horizon=24)
```

## The main models and the ecosystem

TODO(author): the main models, where to find them, how they compare.

## Next in the series

Part 2 (best practices for practitioners) is coming soon.
