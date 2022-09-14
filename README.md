## Intro
This was the original idea of processing VRF responses through different execution paths which I made a contribution to that eventually got merged. Check out the official docs [here](https://docs.chain.link/docs/vrf/v2/best-practices/#processing-vrf-responses-through-different-execution-paths).

## ChainlinkVRF v2: Processing Different Functions ChainlinkVRF requests

Okay, so now you're here. I'm assuming you have some experience with working with chainlink VRF. So let's grind on. I was working with chainlink VRF for a hackathon and wanted to have a specific function make their own request but at the same time the callback action through our `fulfillRanomWords` should depend on whichever function made the request. Hold Up! Francis, What are you saying?😕

Okay lets make sense of this.
When working with chainlink VRFv2, to my knowledge your contract can only have one`fulfillRandomWords` function that it inherits and overrides from `VRFConsumerBaseV2` contract. I personally like to think of the `fulfillRanomWords` function as the entry for the chainlink node to feed our contract the `requestId` and the random number we requested. So when one function makes a request by calling the `requestRandomWords` we make a request for our `fulfillRandomWords` function to be fed with the two parameters, requestId and randomNumber for us to manipulate however we wish.
So yeah! back to the main thing, what if there was a way for us to say...

Hey! `fulfillRandomWords` function, if **fucntionA** made the request do logic A, if **functionB** called made the request do logic B.
Well this isn't really complex at all. Yep! but i didn't find this in the docs and decided to make an article on it which you're reading right now.
Lets go through this contract to help you grasp what we're really trying to do.

```solidity
contract DoSomething is VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface COORDINATOR;
    //STORAGE VARIABLES
    uint256 public variableA;
    uint256 public variableB;
    bytes32 public UPDATE_VARIABLE_A_ID = keccak256("updateVariableA");
    bytes32 public UPDATE_VARIABLE_B_ID = keccak256("updateVariableB");

    //VRF RELATED VARIABLES
    uint64 s_subscriptionId;
    address vrfCoordinator;
    bytes32 keyHash =
        0x4b09e658ed251bcafeebbc69400383d49f344ace09b9576fe248bb02c003fe9f;
    uint32 callBackGasLimit = 120000;
    uint16 requestConfirmations = 3;
    uint32 numWords = 1;

    mapping(uint256 => bytes32) public requestIdToFunctionId;

    constructor(uint64 subscriptionId, address _vrfCoordinator)
        VRFConsumerBaseV2(_vrfCoordinator)
    {
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        s_subscriptionId = subscriptionId;
    }

    function updateVariableA() public {
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callBackGasLimit,
            numWords
        );
        requestIdToFunctionId[requestId] = UPDATE_VARIABLE_A_ID;
    }

    function updateVariableB() public {
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callBackGasLimit,
            numWords
        );
        requestIdToFunctionId[requestId] = UPDATE_VARIABLE_B_ID;
    }

    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords)
        internal
        override
    {
        if (requestIdToFunctionId[requestId] == UPDATE_VARIABLE_A_ID) {
            variableA = randomWords[0];
        }
        if (requestIdToFunctionId[requestId] == UPDATE_VARIABLE_B_ID) {
            variableB = randomWords[0];
        }
    }
}
```

### Breaking the contract down...

I'm not going to go to deep into the VRF related variables as it was a prerequisite to the article. Only the things that are quite different from making a regular request i'll be going through. If you don't understand it challenge yourself, read the docs, watch youtube videos and ask questions in the right places like [Stack Exchange Ethereum.](https://ethereum.stackexchange.com/)

#### Lets start with the storage variables.

```solidity
    //STORAGE VARIABLES
    uint256 public variableA;
    uint256 public variableB;
    bytes32 public UPDATE_VARIABLE_A_ID = keccak256("updateVariableA");
    bytes32 public UPDATE_VARIABLE_B_ID = keccak256("updateVariableB");

    mapping(uint256 => bytes32) public requestIdToFunctionId;
```

- Storage variables `variableA` and `variableB` are numbers we'd be using to test handling different request for different functions.
- The `UPDATE_VARIABLE_A_ID ` and `UPDATE_VARIABLE_B_ID ` is the unique hash for each function name (updateVariableA and updateVariableB respectively).
- With these hashes we can assign the functions in our contract an ID.
- We'll need these function Id's and you'd see why soon.
- The `requestIdToFunctionId` is a mapping from uint256 to bytes32 which i'll explain as we progress why its there.

#### The Functions

```solidity
function updateVariableA() public {
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callBackGasLimit,
            numWords
        );
        requestIdToFunctionId[requestId] = UPDATE_VARIABLE_A_ID;
    }

function updateVariableB() public {
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callBackGasLimit,
            numWords
        );
        requestIdToFunctionId[requestId] = UPDATE_VARIABLE_B_ID;
    }
```

- Here comes the juicy part! We have two different functions that make their own requests via the `COORDINATOR` which returns to us a unique `requestId`.
- You can see that these functions use the mapping from up above to assign a unique request id gotten from making the request, a function Id. This way our `requestId` has a girlfriend which is the function Id, allowing us to use their relationship for a greater cause.

#### The `fulfillRandomWords` function

- Now here's the thing, when each function makes its own request. The logic that'll be done will be based off whatever is in the `fulfillRandomWords` function. How can we tell the `fulfillRandomWords` function that hey it was `updateVariableA` and not `updateVariableB` that made the request?
- You guessed it. Our function Id's and our mapping of `requestIdToFunctionId`!
- So in our `fulfilRandomWords`, we know that we're getting a unique requestId that is different for each request made.
- Meaning we could use `if` statements to check with the ** unique request Id** which function made the request and then appropriately execute the logic for that particular function. It'll look something like this..

```solidity
function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords)
        internal
        override
    {
        if (requestIdToFunctionId[requestId] == UPDATE_VARIABLE_A_ID) {
            variableA = randomWords[0];
        }
        if (requestIdToFunctionId[requestId] == UPDATE_VARIABLE_B_ID) {
            variableB = randomWords[0];
        }
    }
```

- So we're basically setting the storage variableA to the random number if its the updatevariableA that made the request and the same thing with variable B
- Sweet! If you made it here and understood this you've learnt something really cool. Go out there and integrate this with something more challenging or even just deploy a contract and test it out. Then tag me on twitter about what you've learnt or what you're going to build with this. Let's go!

## Reach Out To Me

- You could give me a follow on twitter. Here's my twitter [handle](https://twitter.com/FranFran_E).
