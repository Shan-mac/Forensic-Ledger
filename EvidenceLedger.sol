
pragma solidity ^0.8.0;

contract EvidenceLedger {
    
    struct Evidence {
        string fileHash; 
        uint256 timestamp; 
        bool exists; 
    }

    mapping(string => Evidence) public evidenceRegistry;

    function recordEvidence(string memory _fileHash) public {
        require(!evidenceRegistry[_fileHash].exists, "Evidence already recorded!");

        evidenceRegistry[_fileHash] = Evidence({
            fileHash: _fileHash,
            timestamp: block.timestamp,
            exists: true
        });
    }

    function verifyEvidence(string memory _fileHash) public view returns (bool, uint256) {
        require(evidenceRegistry[_fileHash].exists, "Evidence not found in ledger!");
        return (true, evidenceRegistry[_fileHash].timestamp);
    }
}