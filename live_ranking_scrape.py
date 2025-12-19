import pandas as pd

def fetch_espn_atp_rankings_to_csv(
    url: str = "https://www.espn.com/tennis/rankings",
    csv_path: str = "origin_espn_atp_rankings.csv",
    top_n: int = 200,
):
    tables = pd.read_html(url)

    ranking_df = None
    for t in tables:
        cols = set(map(str, t.columns))
        if {"RK", "NAME", "POINTS"}.issubset(cols):
            ranking_df = t
            break

    if ranking_df is None:
        raise RuntimeError(
            "Could not find a rankings table with columns RK, NAME, POINTS. "
            "The page structure may have changed."
        )

    ranking_df = ranking_df.copy()
    ranking_df = ranking_df[ranking_df["RK"].astype(str).str.isdigit()]
    ranking_df["RK"] = ranking_df["RK"].astype(int)

    ranking_df["POINTS"] = (
        ranking_df["POINTS"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(int)
    )

    ranking_df = ranking_df.rename(
        columns={
            "RK": "Rank",
            "NAME": "Player",
            "POINTS": "Points",
        }
    )

    ranking_df = ranking_df[["Rank", "Player", "Points"]]
    ranking_df = ranking_df.sort_values("Rank").head(top_n).reset_index(drop=True)
    ranking_df.to_csv(csv_path, index=False)
    print(f"Saved {len(ranking_df)} rows to {csv_path}")


if __name__ == "__main__":
    fetch_espn_atp_rankings_to_csv()

