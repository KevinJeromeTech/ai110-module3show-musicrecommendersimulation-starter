# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name
**VibeFinder 1.0** — Explainable CLI-first Music Recommender Simulation.

## 2. Intended Use
This is a classroom demonstration for ranking tracks in a fictional catalog using explicit user preferences. It is not a trained predictive model, production music service, or system for inferring sensitive traits.

## 3. How the Model Works
A genre match earns 2 points; a mood match earns 1. Energy similarity earns up to 1 point based on the distance between the song's energy and the user's target. The top five scores are displayed with reasons. The object-oriented interface can add an optional acousticness bonus up to 0.5. Scores are not probabilities.

## 4. Data
The catalog contains **18 fictional songs**, including 10 starter records and 8 new records representing afrobeats, R&B, hip-hop, classical, folk, EDM, Latin, and funk. Fields include title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. Values are synthetic, not measured from audio or user history.

## 5. Strengths
The approach is deterministic, simple, and explainable. The Chill Lofi profile ranks Library Rain first (4.00); the Intense Rock profile ranks Storm Runner first (3.99). These fit the labeled profiles.

## 6. Limitations and Bias
The catalog is too small to represent musical tastes fairly: three songs are lofi but only one is rock. Exact label comparisons consider pop and indie pop unrelated. Giving a strong bonus to favorite genre causes Gym Hero, a pop/intense track, to rank second even for the Happy Pop profile. This design can create filter bubbles by rewarding familiar genres over discoveries. It lacks actual listening feedback, cultural context, and verified ground truth.

## 7. Evaluation
Four profiles were run against the catalog, and the top five results were recorded in the README. The baseline weights were genre=2, mood=1, energy=1. The experiment changed weights to genre=1, mood=1, energy=2. In the high-energy pop list, Gym Hero fell from second (2.87) to fifth (2.74), showing that its high rank depended on the genre bonus.

### Pairwise comparisons
- **Pop vs. Lofi:** Sunrise City (3.98) leads Happy Pop, while Library Rain (4.00) leads Chill Lofi; mood, genre, and target energy differ.
- **Pop vs. Rock:** Sunrise City (3.98) leads Pop, while Storm Runner (3.99) leads Intense Rock, even though both want high energy.
- **Lofi vs. Rock:** Library Rain's lower energy suits Lofi, while Storm Runner's higher energy suits Rock.
- **Sad High-Energy Pop edge case:** No catalog song has the mood sad, but Gym Hero (2.98) still ranks first because genre and energy match. This is a surprising mismatch in emotional intent.

**Automated verification:** Eight local pytest tests passed for CSV loading, scoring, ranking, the OOP interface, the experiment, and invalid input. No real listener feedback was available; we can observe changed rankings but not conclude which is more accurate.

## 8. Future Work
1. Collect opt-in likes, skips, and ratings as ground truth.
2. Add diversity-aware reranking for repeated genres and artists.
3. Add fuzzy genre matches and appropriately scaled audio features.

## 9. Personal Reflection
**Draft; revise with your own experience before submitting.** I learned how strongly the weights of simple recommendation features affect the final ranking. An AI assistant helped develop scoring logic and test cases, but automated tests and manual result inspection were needed to check that the logic was actually correct. It was surprising that an intense song could rank so highly for someone asking for happy music. Next, I would add real user feedback and recommend more diverse genres.
