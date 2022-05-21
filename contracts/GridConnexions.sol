// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

contract Connexions {
    address public Administrator;

    //établir le propriétaire de contrat 
    constructor() public {
        Administrator = msg.sender; 

    }
    event gridconnectionEvent(
        address _from,
        address _to,
        bool _status);


    struct SmartMeter {
        uint256 IDMeter;
        string Name;
        address DcAdd;
    }
    struct Nan1Block{
        uint256[] ListMeter;
        string dateUSe;
        uint256[] ListPower;
        uint256[] ListReputation;
        string merkleRoot;
    }
    struct DataConstractor {
        uint256 IDDC;
        string Name;
        string Zone;
        address[] MetersList;

    }
    struct WanBlock{
        uint256[] UseZonePower;
        string dateUseDc;
        uint256[] ListMeter;
        uint256[] ListPower;
        uint256[] ListReputationWan;
        string merkleRootWan;
    }
    mapping (address => SmartMeter) public Meter;
    mapping (address => DataConstractor) public Dc;
    mapping(address => mapping(address => bool)) public connections;
    

    
    //établisement de connexion:
    function enableConnections(address _from, address _to) public onlyOwner NotSelf(_from,  _to){
        // vérifier la connexion si déjà établie 
        require(connections[_from][_to] == false, 'connections already established');
        connections[_from][_to] = true;

        emit gridconnectionEvent(_from, _to, true);
    }

    //désactiver la connexion:
    function disableConnections(address _from, address _to) public NotSelf(_from,  _to){
        // checking that connection not already false
        require(connections[_from][_to] == true, 'connections not established');
        connections[_from][_to] = false;

        emit gridconnectionEvent(_from, _to, false);
    }

    function addMeter( address add, uint256 _ID, string memory _name, address _DcAdd) public onlyOwner {
        Meter[add].IDMeter = _ID;
        Meter[add].Name = _name;
        Meter[add].DcAdd = _DcAdd;
        

    }
    
    function addDC( address add, uint256 _IDDC ,string memory _name, string memory _zone, address _Sm1, address _Sm2, address _Sm3) public onlyOwner {
        Dc[add].IDDC = _IDDC;
        Dc[add].Name = _name;
        Dc[add].Zone = _zone;
        Dc[add].MetersList.push(_Sm1);
        Dc[add].MetersList.push(_Sm2);
        Dc[add].MetersList.push(_Sm3);

    }

    function retrieveMeter(address _add) public view returns(string memory) {
        return Meter[_add].Name;
    }

    function retrieveDC(address _add) public view returns(string memory) {
        return Dc[_add].Name;
    }

    modifier onlyOwner{
        require(msg.sender == Administrator ,"You can't Deploy, SORRY!!!!");
        _;
    }

    modifier NotSelf(address _from, address _to) {
        require(_from != _to, "Can't Establish connections with self");
        _;
    }

    
}


    



