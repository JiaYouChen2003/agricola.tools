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

CARD_INFO_ARR_HAND_NOTHING = [
    ['', 0, 0, 0],
    ['', 0, 0, 0],
    ['', 0, 0, 0],
    [const_agricolatools.CARD_HAND_LABEL, None, None, 0],
    ['', 0, 0, 0]]

CARD_INFO_ARR_HAND_TESTING0 = [
    ['zz_TEST01', 0, 0, 0],
    ['zz_TEST02', 0, 0, 0],
    ['zz_TEST03', 0, 0, 0],
    [const_agricolatools.CARD_HAND_LABEL, None, None, 0],
    ['zz_TEST0', 0, 0, 0]]

CARD_INFO_ARR_HAND_TESTING1 = [
    ['zz_TEST11', 0, 0, 0],
    ['zz_TEST12', 0, 0, 0],
    ['zz_TEST13', 0, 0, 0],
    ['zz_TEST14', 0, 0, 0],
    ['', 0, 0, 0],
    [const_agricolatools.CARD_HAND_LABEL, None, None, 0],
    ['zz_TEST1', 0, 0, 0]]


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


@pytest.mark.analyze
def test_getCardSynergyScore_nothing():
    machine_analyze = AnalyzeMachine()
    card_info_arr = machine_analyze.getCardSynergyScore(CARD_INFO_ARR_HAND_NOTHING)
    
    assert card_info_arr == CARD_INFO_ARR_HAND_NOTHING


@pytest.mark.analyze
def test_getCardSynergyScore_TEST0():
    machine_analyze = AnalyzeMachine()
    card_info_arr = machine_analyze.getCardSynergyScore(CARD_INFO_ARR_HAND_TESTING0)
    
    assert len(card_info_arr) == len(CARD_INFO_ARR_HAND_TESTING0)
    assert len(card_info_arr[0]) == 5
    assert card_info_arr[0][-2] == '1'
    assert card_info_arr[1][-2] == '1'
    assert card_info_arr[2][-2] == '1'


@pytest.mark.analyze
def test_getCardSynergyScore_TEST1():
    machine_analyze = AnalyzeMachine()
    card_info_arr = machine_analyze.getCardSynergyScore(CARD_INFO_ARR_HAND_TESTING1)
    
    assert len(card_info_arr) == len(CARD_INFO_ARR_HAND_TESTING1)
    assert len(card_info_arr[0]) == 5
    assert card_info_arr[0][-2] == '1'
    assert card_info_arr[1][-2] == '1'
    assert card_info_arr[2][-2] == '1'
    assert card_info_arr[3][-2] == '1'
