pragma solidity ^0.6.4;
pragma experimental ABIEncoderV2;

import './GridConnexions.sol';



contract Communications {

    address public Administrator;
    Connexions maps;

    constructor(address addr) public {
        maps = Connexions(addr);
        Administrator = msg.sender;
    }
    
    event NewTrade(
        address indexed _from,
        address indexed to,
        uint indexed iteration,
        string[] amount
        );


    function passingValues(address _sender, address _to, uint _iteration, string[] memory _value) public {
        require(maps.connections(_sender,_to),"Connection Not Established");
          emit NewTrade(_sender, _to, _iteration, _value);
    }

    function checkingstate(address _sender, address _to) view public returns(bool){
       return maps.connections(_sender,_to);
    }

}