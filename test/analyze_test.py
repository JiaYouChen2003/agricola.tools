import pytest

from raw_asset.python_files import *

CARD_INFO_ARR_NOTHING_TESTING = [
    [None, None, None, 1],
    [None, None, None, 2],
    [None, None, None, 3]]

CARD_INFO_ARR_EXAMPLE_TESTING = [
    ['test_player1', None, None, 1],
    ['test1', 1, 0, 1],
    ['test2', 2, 0, 1],
    ['test3', 3, 0, 1],
    ['test_player2', None, None, 2],
    ['test4', 4, 0, 2],
    ['test5', 5, 0, 2]]


@pytest.mark.analyze
def test_getCardRankMean_nothingAllPlayer_meanZero():
    machine_analyze = AnalyzeMachine()
    mean = machine_analyze.getCardRankMean(CARD_INFO_ARR_NOTHING_TESTING, player_num=0)
    
    assert mean == 0


@pytest.mark.analyze
def test_getCardRankMean_nothingPlayerOne_meanZero():
    machine_analyze = AnalyzeMachine()
    mean = machine_analyze.getCardRankMean(CARD_INFO_ARR_NOTHING_TESTING, player_num=1)
    
    assert mean == 0


@pytest.mark.analyze
def test_getCardRankMean_exampleAllPlayer_meanThree():
    machine_analyze = AnalyzeMachine()
    mean = machine_analyze.getCardRankMean(CARD_INFO_ARR_EXAMPLE_TESTING, player_num=0)
    
    assert mean == 3


@pytest.mark.analyze
def test_getCardRankMean_examplePlayerOne_meanTwo():
    machine_analyze = AnalyzeMachine()
    mean = machine_analyze.getCardRankMean(CARD_INFO_ARR_EXAMPLE_TESTING, player_num=1)
    
    assert mean == 2


@pytest.mark.analyze
def test_getCardRankMean_examplePlayerTwo_meanFour():
    machine_analyze = AnalyzeMachine()
    mean = machine_analyze.getCardRankMean(CARD_INFO_ARR_EXAMPLE_TESTING, player_num=2)
    
    assert mean == 4
