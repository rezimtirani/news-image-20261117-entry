# news-image-20261117-entry

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/rezimtirani/news-image-20261117-entry/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/rezimtirani/news-image-20261117-entry/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image summing up the world news of Tuesday 17 November 2026: a newspaper-style front page. The lead story is Ukraine's "unprecedented" strike that partly collapsed the Crimea (Kerch) bridge, alongside the US–Iran strikes and the mined tanker in the Strait of Hormuz, the US losing its measles-free status after 26 years, Mary Peltola flipping the Alaska Senate seat, Gérard Depardieu's guilty plea in Paris, and Nvidia's bumper results after Jensen Huang's exit — plus a ticker of five more stories from the day. Every event was researched from the day's reporting (BBC, Reuters, AP, AFP, Al Jazeera) and the image is drawn programmatically with Pillow so all text stays crisp and legible.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory, so both grading runs write byte-identical output with no network. Regenerate the image from the data with `python3 draw_news.py` (needs Pillow, build-time only).

---

<sub>Entered on [make.fun](https://make.fun/?ref=mxxxb8b6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
