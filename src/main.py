"""Run and evaluate the music recommender from the command line."""

from pathlib import Path

from .recommender import EXPERIMENT_WEIGHTS, load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    "Edge Case: Sad High-Energy Pop": {"genre": "pop", "mood": "sad", "energy": 0.95},
}


def print_recommendations(label: str, profile: dict, songs: list, weights=None) -> None:
    """Display the top five tracks with scores and explanations."""
    print(f"\nUser profile: {label} | {profile}")
    for rank, (song, score, explanation) in enumerate(
        recommend_songs(profile, songs, k=5, weights=weights), start=1
    ):
        print(f"  {rank}. {song['title']} — {song['artist']} | Score: {score:.2f}")
        print(f"     Because: {explanation}")


def main() -> None:
    """Load the catalog, compare profiles, and run a weight experiment."""
    catalog_path = Path(__file__).resolve().parent.parent / "data" / "songs.csv"
    songs = load_songs(str(catalog_path))
    print(f"Loaded songs: {len(songs)}")

    for label, profile in PROFILES.items():
        print_recommendations(label, profile, songs)

    profile = PROFILES["High-Energy Pop"]
    print("\nEXPERIMENT: Half genre weight (2.0→1.0), double energy weight (1.0→2.0)")
    print_recommendations("High-Energy Pop, altered weights", profile, songs, EXPERIMENT_WEIGHTS)


if __name__ == "__main__":
    main()
