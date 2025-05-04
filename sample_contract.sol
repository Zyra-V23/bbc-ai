// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SimpleLending
 * @dev A simple lending contract for demonstration purposes
 * @notice This contract has some intentional vulnerabilities
 */
contract SimpleLending {
    address public owner;
    
    // Track user balances
    mapping(address => uint256) public deposits;
    mapping(address => uint256) public borrowedAmount;
    
    // Events
    event Deposit(address indexed user, uint256 amount);
    event Withdraw(address indexed user, uint256 amount);
    event Borrow(address indexed user, uint256 amount);
    event Repay(address indexed user, uint256 amount);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(tx.origin == owner, "Only owner can call this function");
        _;
    }
    
    // Users can deposit ETH
    function deposit() external payable {
        deposits[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    // Users can withdraw their deposits
    function withdraw(uint256 amount) external {
        require(deposits[msg.sender] >= amount, "Insufficient funds");
        
        deposits[msg.sender] -= amount;
        
        // Send funds back to user
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit Withdraw(msg.sender, amount);
    }
    
    // Users can borrow ETH if there's enough in the contract
    function borrow(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(address(this).balance >= amount, "Not enough funds in contract");
        
        borrowedAmount[msg.sender] += amount;
        
        // Send borrowed funds to user
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit Borrow(msg.sender, amount);
    }
    
    // Users can repay their borrowed amounts
    function repay() external payable {
        require(borrowedAmount[msg.sender] >= msg.value, "Repaying too much");
        
        borrowedAmount[msg.sender] -= msg.value;
        
        emit Repay(msg.sender, msg.value);
    }
    
    // Owner can withdraw all funds in emergency
    function emergencyWithdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        (bool success, ) = owner.call{value: balance}("");
        require(success, "Transfer failed");
    }
    
    // Function to get the total amount of ether in the contract
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    // Function to get user information
    function getUserInfo(address user) external view returns (uint256 deposited, uint256 borrowed) {
        return (deposits[user], borrowedAmount[user]);
    }
    
    // External call function for demonstration
    function callExternalContract(address target, bytes memory data) external onlyOwner {
        (bool success, ) = target.call(data);
        require(success, "External call failed");
    }
}
