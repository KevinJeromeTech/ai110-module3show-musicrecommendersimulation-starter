# 🎵 Music Recommender Simulation — VibeFinder 1.0

## Project Summary

VibeFinder 1.0 is a CLI-first content-based music recommendation simulator. It reads a fictional catalog of 18 songs, compares song attributes with a user's preferences, and ranks the top five with scores and explanations. This is a transparent, rule-based simulation, not a trained predictive machine learning model.

## How The System Works

Real-world platforms use collaborative filtering (patterns of many listeners) and content-based filtering (metadata and audio features), informed by likes, skips, playlists, and listening time. This project intentionally uses **content-based filtering** only.

- **Song attributes:** ID, title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness.
- **User profile:** favorite genre, favorite mood, target energy, and optional preference for acoustic tracks.
- **Algorithm recipe:** +2.0 points for exact genre match, +1.0 for exact mood match, and energy similarity points calculated as `1 - abs(song_energy - target_energy)`. Optional class-based acoustic bonus is at most 0.5.
- **Ranking:** score every song, sort descending by score (breaking ties by title), then return the top K with reasons.

For the default CLI, the maximum score is **4.0**. A song's score expresses fit to rules, not a probability of liking it. A **scoring rule** judges one song; a **ranking rule** sorts all judged songs.

```text
CSV catalog + user preferences
             ↓
  Load and cast numeric fields
             ↓
   Score each song + reasons
             ↓
    Sort by descending score
             ↓
      Display Top 5 songs
```

## Getting Started

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.main
python -m pytest -q
```

## Sample Recommendation Output

The following terminal output was generated from the 18-song dataset and covers all four profiles and a weight experiment:

```text
Loaded songs: 18

User profile: High-Energy Pop | {"genre":"pop","mood":"happy","energy":0.8}
  1. Sunrise City — Neon Echo | Score: 3.98
     Because: genre match (+2.00), mood match (+1.00), energy similarity (+0.98)
  2. Gym Hero — Max Pulse | Score: 2.87
     Because: genre match (+2.00), energy similarity (+0.87)
  3. Golden Coastline — Sunbird Collective | Score: 1.98
     Because: mood match (+1.00), energy similarity (+0.98)
  4. Summer Calle — Mar Sol | Score: 1.97
     Because: mood match (+1.00), energy similarity (+0.97)
  5. Rooftop Lights — Indigo Parade | Score: 1.96
     Because: mood match (+1.00), energy similarity (+0.96)

User profile: Chill Lofi | {"genre":"lofi","mood":"chill","energy":0.35}
  1. Library Rain — Paper Lanterns | Score: 4.00
     Because: genre match (+2.00), mood match (+1.00), energy similarity (+1.00)
  2. Midnight Coding — LoRoom | Score: 3.93
     Because: genre match (+2.00), mood match (+1.00), energy similarity (+0.93)
  3. Focus Flow — LoRoom | Score: 2.95
     Because: genre match (+2.00), energy similarity (+0.95)
  4. Spacewalk Thoughts — Orbit Bloom | Score: 1.93
     Because: mood match (+1.00), energy similarity (+0.93)
  5. Coffee Shop Stories — Slow Stereo | Score: 0.98
     Because: energy similarity (+0.98)

User profile: Intense Rock | {"genre":"rock","mood":"intense","energy":0.9}
  1. Storm Runner — Voltline | Score: 3.99
     Because: genre match (+2.00), mood match (+1.00), energy similarity (+0.99)
  2. Gym Hero — Max Pulse | Score: 1.97
     Because: mood match (+1.00), energy similarity (+0.97)
  3. Voltage Bloom — Club Circuit | Score: 0.94
     Because: energy similarity (+0.94)
  4. Summer Calle — Mar Sol | Score: 0.93
     Because: energy similarity (+0.93)
  5. Sunrise City — Neon Echo | Score: 0.92
     Because: energy similarity (+0.92)

User profile: Edge Case: Sad High-Energy Pop | {"genre":"pop","mood":"sad","energy":0.95}
  1. Gym Hero — Max Pulse | Score: 2.98
     Because: genre match (+2.00), energy similarity (+0.98)
  2. Sunrise City — Neon Echo | Score: 2.87
     Because: genre match (+2.00), energy similarity (+0.87)
  3. Voltage Bloom — Club Circuit | Score: 0.99
     Because: energy similarity (+0.99)
  4. Storm Runner — Voltline | Score: 0.96
     Because: energy similarity (+0.96)
  5. Summer Calle — Mar Sol | Score: 0.88
     Because: energy similarity (+0.88)

EXPERIMENT: Half genre weight (2.0→1.0), double energy weight (1.0→2.0)

User profile: High-Energy Pop, altered weights | {"genre":"pop","mood":"happy","energy":0.8}
  1. Sunrise City — Neon Echo | Score: 3.96
     Because: genre match (+1.00), mood match (+1.00), energy similarity (+1.96)
  2. Golden Coastline — Sunbird Collective | Score: 2.96
     Because: mood match (+1.00), energy similarity (+1.96)
  3. Summer Calle — Mar Sol | Score: 2.94
     Because: mood match (+1.00), energy similarity (+1.94)
  4. Rooftop Lights — Indigo Parade | Score: 2.92
     Because: mood match (+1.00), energy similarity (+1.92)
  5. Gym Hero — Max Pulse | Score: 2.74
     Because: genre match (+1.00), energy similarity (+1.74)
```

## Experiments You Tried

**Baseline:** genre=2, mood=1, energy=1. The Happy Pop listener saw Sunrise City (3.98) first and Gym Hero (2.87) second. Gym Hero is intense rather than happy, yet the genre bonus placed it ahead of happier cross-genre tracks.

**Changed weights:** genre=1, mood=1, energy=2 (same 4-point maximum). Sunrise City remained first (3.96), Golden Coastline rose to second (2.96), and Gym Hero dropped to fifth (2.74). This demonstrates sensitivity to weights, not objectively better accuracy—there are no actual user preference labels or ground truth.

**Profiles:** High-Energy Pop, Chill Lofi, Intense Rock, and a contradictory Sad High-Energy Pop edge case each produced different lists.

## Limitations and Risks

This tiny synthetic dataset has uneven genre representation, including three lofi songs and only one rock song. Exact labels fail to connect related genres (pop versus indie pop). Giving genre a large bonus can cause a filter bubble and overlook songs of different genres with suitable mood and energy. The simulation does not learn from listening history, understand lyrics, balance artist diversity, or evaluate against listener ratings.

## Reflection

Building this recommender helped me see how a music platform can turn simple song features into a ranked list without training a machine-learning model. The scoring rule is straightforward, but its weights matter: the baseline placed Gym Hero second for a Happy Pop listener even though the track is labeled intense. When I shifted weight away from genre and toward energy, the ranking changed. That made me more aware that a recommendation can look reasonable while still reflecting the assumptions and biases built into its rules.

I used AI assistance to plan and implement the Python scoring functions, add explanations, and structure the evaluation. I also had to troubleshoot practical problems in my development environment, including Python commands, module imports, and a circular import, and I used the automated tests to check the implementation. The biggest lesson for me was that generating code is only part of engineering; I still need to understand the logic, verify the output, and consider what the system misses. If I continued the project, I would add real listener feedback and a diversity-aware ranking step.

More detail: [Model Card](model_card.md).
