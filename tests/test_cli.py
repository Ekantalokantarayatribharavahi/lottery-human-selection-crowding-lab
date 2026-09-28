from lottery_human_selection_crowding.cli import main

def test_cli_score(capsys):
    import sys
    sys.argv=["crowding","score","--game","lotto","--combination","7,18,29,34,41,52"]
    assert main()==0
    assert "lottery draw probability" in capsys.readouterr().out
