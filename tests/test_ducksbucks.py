from ducksy.ducksbucks import format_bets, format_games


def test_format_games():
    games = [{"home": "Boston", "away": "Toronto", "start_time": "7:00 PM"}]
    assert format_games(games) == "Boston VS Toronto @ 7:00 PM"
    assert "no games" in format_games([])


def test_format_bets():
    bets = [
        {
            "challenger": "Player One",
            "challengee": "Player Two",
            "amount": 5,
            "challenger_pick": "Boston",
            "challengee_pick": "Toronto",
        }
    ]
    assert format_bets(bets) == "Player One bet Player Two 5 DucksBucks on Boston to beat Toronto"
    assert format_bets([]) == "No unresolved bets today."
