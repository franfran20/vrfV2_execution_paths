import pytest
from brownie import Wei, accounts

sub_id = 1
amount = Wei("1 ether")
request_id = 1
base_fee = Wei("0.25 ether")
gas_price_link = Wei("1 gwei")

@pytest.fixture
def do_something(VRFCoordinatorV2Mock, DoSomething):
    vrf_mock = VRFCoordinatorV2Mock.deploy(base_fee, gas_price_link,{"from": accounts[0]})
    vrf_mock.createSubscription({"from": accounts[0]})
    vrf_mock.fundSubscription(sub_id, amount, {"from": accounts[0]})
    Do_Something = DoSomething.deploy(sub_id, vrf_mock.address, {"from": accounts[0]})
    return Do_Something

def test_update_variabale_a(do_something, VRFCoordinatorV2Mock):
    do_something.updateVariableA()
    #mock chainlink VRF, P.S I like to tweak the mock to be able to be flexible with my random numbers
    #Just My personal preference
    VRFCoordinatorV2Mock[-1].fulfillRandomWords(request_id, do_something.address, [890])
    assert do_something.variableA() == 890
    assert do_something.variableB() == 0

def test_update_variabale_b(do_something, VRFCoordinatorV2Mock):
    do_something.updateVariableB()
    #mock chainlink VRF, P.S I like to tweak the mock to be able to be flexible with my random numbers
    #Just My personal preference
    VRFCoordinatorV2Mock[-1].fulfillRandomWords(request_id, do_something.address, [234])
    assert do_something.variableA() == 0
    assert do_something.variableB() == 234

def test_update_variable_a_and_b(do_something, VRFCoordinatorV2Mock):
    do_something.updateVariableA()
    VRFCoordinatorV2Mock[-1].fulfillRandomWords(request_id, do_something.address, [234])
    do_something.updateVariableB()
    VRFCoordinatorV2Mock[-1].fulfillRandomWords(request_id + 1, do_something.address, [467])
    #mock chainlink VRF, P.S I like to tweak the mock to be able to be flexible with my random numbers
    #Just My personal preference
    assert do_something.variableA() == 234
    assert do_something.variableB() == 467
