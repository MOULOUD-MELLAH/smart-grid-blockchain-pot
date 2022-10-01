// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

contract Connexions {
    address Administrator;

    //établir le propriétaire de contrat 
    constructor() public {
        Administrator = msg.sender; 
        Leader[msg.sender]=true;

    }

   //etablissement de connexions 
    event gridconnectionEvent(
        address _from,
        address _to,
        bool _status);

    //structure d'un smart meter 
    struct SmartMeter {
        uint256 IDMeter;
        uint256 zone;
        string public_key;
        string Name;
        address DcAdd;
    }
    
    //structure d'un data concentrateur 
    struct DataConstractor {
        uint256 IDDC;
        string public_key;
        string Name;
        uint256 zone;
        address[] MetersList;

    }

    //structure d'un block Nan 
    struct NanBlock{
        uint256[] ListMeter;
        string dateUSe;
        string TimeUse;
        string[] ListPower;
        uint256[] ListReputation;
        string merkleRoot;
        string merkleRootRep;
        bool dataValidate;
        bool RepValidate;
    }

    NanBlock public BlockNan1;
    NanBlock public blockNan2;

     
    struct WanBlock{
        string[] UseZonePower;
        string dateUseDc;
        string timeUseDC;
        uint256[] ListMeter;
        string[] ListPower;
        uint256[] ListReputationWan;
        uint256[] ListTheft;
    }

    WanBlock public BlockWan;

    struct NanVote {
        string dateUse;
        string TimeUse;
        uint256 votePos;
        uint256 voteNeg;
        uint256 Ra;
        uint256 Rt;
        uint256 Rr;
        uint256 NV;
    }

    NanVote public VoteBlockData;
    NanVote public VoteBlockRep;
    
    mapping(address => mapping(address => bool)) public connections;
    mapping (address => SmartMeter) public Meter;
    mapping (address => bool) public Leader;
    mapping (address => DataConstractor) public Dc;
    mapping (address => bool) public VotedData;
    mapping (address => bool) public VotedRep;
    
    

    
    //établisement de connexion:
    function enableConnections(address _from, address _to) public onlyOwner NotSelf(_from,  _to){
        // vérifier la connexion si déjà établie 
        require(connections[_from][_to] == false, 'connections already established');
        connections[_from][_to] = true;
        emit gridconnectionEvent(_from, _to, true);
    }

    //désactiver la connexion:
    function disableConnections(address _from, address _to) public NotSelf(_from,  _to){
        // vérifier la connexions si elle n'est pas déjà désactivé
        require(connections[_from][_to] == true, 'connections not established');
        connections[_from][_to] = false;
        emit gridconnectionEvent(_from, _to, false);
    }


    //ajoute d'un meter au deployement 
    function addMeter( address add, uint256 _ID, string memory _name, uint256 _zone, address _DcAdd) public onlyOwner {
        Meter[add].IDMeter = _ID;
        Meter[add].zone = _zone;
        Meter[add].Name = _name;
        Meter[add].DcAdd = _DcAdd;
        

    }

    //ajouter la clé public de smart meter à blockcahin 
    function addKeyMeter(address add, string memory _key) public {
        Meter[add].public_key = _key;
    }
    
    //ajouter un dc au deployement 
    function addDC( address add, uint256 _IDDC ,string memory _name, uint256 _zone, address[] memory _meterList) public onlyOwner {
        Dc[add].IDDC = _IDDC;
        Dc[add].Name = _name;
        Dc[add].zone = _zone;
        Dc[add].MetersList = _meterList;

    }

    //ajouter une clé public au dc 
    function addKeyDc(address add, string memory _key) public {
        Dc[add].public_key = _key;
    }

    //fonction qui va supprimer B1 si non valide 
    function Delete_B1() public onlyOwner {
        delete BlockNan1.ListMeter;
        delete BlockNan1.ListPower ;
        delete BlockNan1.ListReputation ;
        delete BlockNan1.merkleRoot ;

    }

    //avoir clé public d'un smart meter 
    function retrieveMeterKey(address _add) public view returns(string memory) {
        return Meter[_add].public_key;
    }

    //avoir le nom d'un smart meter 
    function retrieveMeter(address _add) public view returns(string memory) {
        return Meter[_add].Name;
    }

    //avoir l'id de smart meter 
    function retrieveIDMeter(address _add) public view returns(uint256) {
        return Meter[_add].IDMeter;
    }

    //avoir le nom de DC 
    function retrieveDC(address _add) public view returns(string memory) {
        return Dc[_add].Name;
    }

    //avoir la clé publique de DC 
    function retrieveDCKey(address _add) public view returns(string memory) {
        return Dc[_add].public_key;
    }
    //avoir id de dc 
    function retrieveIDDC(address _add) public view returns(uint256) {
        return Dc[_add].IDDC;
    }

    //avoir les smart meters de chaue dc (zone)
    function GetDcAccounts(address _add ) public view returns(address[] memory){
        return Dc[_add].MetersList;
    }

    //avoir la liste des réputations 
    function GetRepList() public view returns(uint256[] memory){
        return BlockNan1.ListReputation;
    }

    //partie de validation d'un bloc 
    //selection de leader 

    function select_leader(address[] memory _meters, uint256[] memory _Rep) public onlyOwner {
        for (uint256 i = 0; i < _meters.length; i++){
            Leader[_meters[i]] = false;

        }  
        uint256 Max = _Rep[0];
        uint256 IdMax = 0;    
        
        for (uint256 i = 1; i < _Rep.length; i++){
            if (_Rep[i] > Max){
                Max = _Rep[i];
                IdMax = i;
            }
        }
        Leader[_meters[IdMax]] = true;
        

    } 

   function GetEtatLeader(address _meter) public view returns(bool){
        return Leader[_meter];
    }

    //trouver le leader 
    function get_leader(address[] memory _accounts ) public view returns(address){
        for (uint256 i = 0; i < _accounts.length; i++){
            if (Leader[_accounts[i]] == true){
                return _accounts[i];
                
            }
        }


    }

    //inistailiser la liste de réputation au deployement 
    function WanInitialise( uint256[] memory _rep) public onlyLeader {
        BlockNan1.ListReputation = _rep ;
    }

    function tansactionNan1B1(uint256[] memory _meters,string memory _date, string memory _Time,string[] memory _listPower,string memory _merkleRoot) public onlyLeader {

        BlockNan1.ListMeter = _meters;
        BlockNan1.dateUSe = _date;
        BlockNan1.TimeUse = _Time;
        BlockNan1.ListPower = _listPower;
        BlockNan1.dataValidate = false;
        BlockNan1.RepValidate = false;
        BlockNan1.merkleRoot = _merkleRoot;
    }

    function get_dataMerkleRoot() public view returns(string memory) {
        return BlockNan1.merkleRoot;
    }

    function get_dateUse() public view returns(string memory) {
        return BlockNan1.dateUSe;
    }
    function get_TimeUse() public view returns(string memory) {
        return BlockNan1.TimeUse;
    }

    //fonction qui va enregistrer les votes et valider le block B1 
    function VoteB1(uint256 _id, bool _vote, string memory _date, string memory _time) public {
        require(!VotedRep[msg.sender]);
        VoteBlockRep.Rt =  VoteBlockData.Rt + BlockNan1.ListReputation[_id];
        VoteBlockData.NV = VoteBlockData.NV + 1;
        VoteBlockData.dateUse = _date;
        VoteBlockData.TimeUse = _time;
        if (_vote == true){
            VoteBlockData.votePos =  VoteBlockData.votePos + 1;
            VotedData[msg.sender] = true;
            VoteBlockData.Ra = VoteBlockData.Ra + BlockNan1.ListReputation[_id];
        } else if (_vote == false){
            VoteBlockData.voteNeg = VoteBlockData.voteNeg + 1;
            VotedData[msg.sender] = true;
            VoteBlockData.Rr = VoteBlockData.Ra + BlockNan1.ListReputation[_id];
        }
        if (VoteBlockData.Ra > 2 * VoteBlockData.Rt/3  && VoteBlockData.votePos > 2 * VoteBlockData.NV/3){
            BlockNan1.dataValidate = true;
        }else if (VoteBlockData.Rr > 2 * VoteBlockData.Rt/3  && VoteBlockData.voteNeg > 2 * VoteBlockData.NV/3){
            BlockNan1.dataValidate = false;
        }else {
            BlockNan1.dataValidate = false;
        }
    }
    //initialiser les variables de votes à 0 et à false 
    function VoteInitialize(address[] memory _meters) public onlyOwner {
        VoteBlockData.Rt = 0;
        VoteBlockData.Rr = 0;
        VoteBlockData.Ra = 0;
        VoteBlockData.NV = 0;
        VoteBlockData.voteNeg = 0;
        VoteBlockData.votePos = 0;
        for (uint256 i = 0; i < _meters.length; i++){
            VotedData[_meters[i]] = false;
            VotedRep[_meters[i]] = false;

        } 
    }
    //fonction qui retourne true si le block B1 est validé
    function DataVa() public view returns(bool) {
        return BlockNan1.dataValidate;
    }



    function tansactionNan1B2(uint256[] memory _Rep, string memory _merkleRootRep) public onlyLeader {

        BlockNan1.ListReputation = _Rep;
        BlockNan1.merkleRootRep = _merkleRootRep;
    }

    function get_dataMerkleRootRep() public view returns(string memory) {
        return BlockNan1.merkleRootRep;
    }

    //fonction qui va retourner liste des ids de bloc NAN
    function get_IDS(uint256 _NAN) public view returns(uint256[] memory){
        if(_NAN == 1){
            return BlockNan1.ListMeter;

        }else if(_NAN == 2){
            return blockNan2.ListMeter;
        }

    }

    //fonction qui va retourner liste des mesures
    function get_Mesures(uint256 _NAN) public view returns(string[] memory){
        if(_NAN == 1){
            return BlockNan1.ListPower;

        }else if(_NAN == 2){
            return blockNan2.ListPower;
        }

    }

    //fonction de vote sur B2 
    function VoteB2(uint256 _id, bool _vote, string memory _date, string memory _time) public {
        require(!VotedRep[msg.sender]);
        VoteBlockRep.Rt =  VoteBlockRep.Rt + BlockNan1.ListReputation[_id];
        VoteBlockRep.NV = VoteBlockRep.NV + 1;
        VoteBlockRep.dateUse = _date;
        VoteBlockRep.TimeUse = _time;
        if (_vote == true){
            VoteBlockRep.votePos =  VoteBlockRep.votePos + 1;
            VotedRep[msg.sender] = true;
            VoteBlockRep.Ra = VoteBlockRep.Ra + BlockNan1.ListReputation[_id];
        } else if (_vote == false){
           VoteBlockRep.voteNeg = VoteBlockRep.voteNeg + 1;
            VotedRep[msg.sender] = true;
            VoteBlockRep.Rr = VoteBlockRep.Ra + BlockNan1.ListReputation[_id];
        }
        if (VoteBlockRep.Ra > 2 * VoteBlockRep.Rt/3  && VoteBlockRep.votePos > 2 * VoteBlockRep.NV/3){
            BlockNan1.RepValidate = true;
        }else if (VoteBlockRep.Rr > 2 * VoteBlockRep.Rt/3  && VoteBlockRep.voteNeg > 2 * VoteBlockRep.NV/3){
            BlockNan1.RepValidate = false;
        }else {
            BlockNan1.RepValidate = false;
        }
    }
    //fonction qui initialise les variables avant le vote sur le block B2 
    function VoteInitializeB2(address[] memory _meters) public onlyOwner {
        VoteBlockRep.Rt = 0;
        VoteBlockRep.Rr = 0;
        VoteBlockRep.Ra = 0;
        VoteBlockRep.NV = 0;
        VoteBlockRep.voteNeg = 0;
        VoteBlockRep.votePos = 0;
        for (uint256 i = 0; i < _meters.length; i++){
            VotedRep[_meters[i]] = false;
            VotedRep[_meters[i]] = false;

        } 
    }

    //fonction qui retourne true si le block B2 est validé
    function RepVa() public view returns(bool) {
        return BlockNan1.RepValidate;
    }
    //initialiser le block Wan 
    function tansactionWanInit(uint256[] memory _rep, uint256[] memory _reptheft) public {
        BlockWan.ListReputationWan= _rep;
        BlockWan.ListTheft = _reptheft;
    }
    function tansactionWanInit2(string[] memory _energy ) public onlyOwner {

        BlockWan.UseZonePower = _energy ;
    
    }

    //transaction wan 
    function transactionWan(string memory _dateUseDc,string memory _timeUseDc, uint256[] memory _meter, string[] memory _power, uint256[] memory _rep, uint256[] memory _reptheft) public {
        BlockWan.dateUseDc = _dateUseDc;
        BlockWan.timeUseDC = _timeUseDc;
        BlockWan.ListMeter = _meter ;
        BlockWan.ListPower = _power; 
        BlockWan.ListReputationWan= _rep;
        BlockWan.ListTheft = _reptheft;
    }

    function getRepWan() public view returns(uint256[] memory) {
        return BlockWan.ListReputationWan;

    }
    function getRepTheftWan() public view returns(uint256[] memory) {
        return BlockWan.ListTheft;

    }
    function getUseZone() public view returns(string[] memory) {
        return BlockWan.UseZonePower;

    }

    function getIDDC(address _add) public view returns(uint256) {
        return Dc[_add].IDDC;

    }



    modifier onlyLeader{
        require(Leader[msg.sender] == true ,"Vous n'etes pas leader !!!!");
        _;
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


    



