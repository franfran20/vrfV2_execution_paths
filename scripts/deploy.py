from brownie import DoSomething, Wei, accounts, config, network

sub_id = 938
vrf_coordinator = config["networks"][network.show_active()]["vrf_coordinator"]

def main():
    account = accounts.load("francis-test")
    do_something = DoSomething.deploy(sub_id, vrf_coordinator, {"from": account, "priority_fee": Wei("100 gwei")}  )
    verify(do_something.address)
    
def verify(addr):
    do_something = DoSomething.at(addr)
    DoSomething.publish_source(do_something)