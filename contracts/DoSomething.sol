// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

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
