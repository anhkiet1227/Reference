pragma solidity ^0.8.0;

contract CrossChainDataTransferPolkadot {
    address public polkadotBridgeAddress;
    
    event DataTransferred(address indexed fromChain, address indexed toChain, bytes32 indexed id, string data);

    constructor(address _polkadotBridgeAddress) {
        polkadotBridgeAddress = _polkadotBridgeAddress;
    }

    function transferData(bytes32 id, string memory newData) public {
        require(bytes(newData).length > 0, "Data should not be empty");
        Bridge(polkadotBridgeAddress).transferDataToPolkadot(id, newData);
        emit DataTransferred(address(this), polkadotBridgeAddress, id, newData);
    }
}

interface Bridge {
    function transferDataToPolkadot(bytes32 id, string memory data) external;
}
