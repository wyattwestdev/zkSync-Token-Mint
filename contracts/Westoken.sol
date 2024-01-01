// SPDX-License-Identifier: MIT

pragma solidity ^0.8.12;

// Enable ABI encoder v2
pragma abicoder v2;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Westoken is Ownable, ERC20
{
    // The maximum amount of tokens that can be minted.
    uint256 private maxSupply;
    // The amount of tokens available to be minted.
    uint256 private availableSupply;
    
    constructor(uint256 _initialSupply) ERC20("Westoken", "WEST")
    {
        maxSupply = _initialSupply * 10 ** decimals();
        availableSupply = maxSupply;
    }

    //
    // TOKEN
    //
    /**
     * @dev A function that burns the token in the sender's wallet and send it back to the token contract. 
     *
     * @param _amount The amount of tokens to be burned.
     *
     */
    function burn(uint256 _amount) public onlyOwner
    {
        uint256 amount = _amount * 10 ** decimals();
        require(amount <= balanceOf(msg.sender), "The amount must be less or equal than the wallet's balance.");
        require((amount + availableSupply) <= maxSupply);
        _burn(msg.sender, amount);
        availableSupply += amount;
    }

    /**
     * @dev A function that mints the token to the sender's wallet. 
     *
     * @param _amount The amount of tokens to be minted.
     *
     */
    function mint(uint256 _amount) public onlyOwner
    {
        uint256 amount = _amount * 10 ** decimals();
        require(amount <= availableSupply, "The amount is higher than the circulating supply.");
        _mint(msg.sender, amount);
        availableSupply -= amount;
    }

    /**
     * @dev A function that returns the token balance of the sender's wallet. 
     *
     * @return uint256 The token balance from the sender's wallet.
     *
     */
    function getBalance() external view returns(uint256)
    {
        return balanceOf(msg.sender);
    }

    //
    // TOKENOMICS
    //
    /**
     * @dev A function that returns the created token total supply. 
     *
     * @return uint256 The full amount of tokens in total supply.
     *
     */
    function getMaxSupply() view public returns(uint256)
    {
        return maxSupply;
    }

    /**
     * @dev A function that returns the created token circulating supply. 
     *
     * @return uint256 The full amount of tokens in circulating supply.
     *
     */
    function getAvailableSupply() view public returns(uint256)
    {
        return availableSupply;
    }

    /**
     * @dev A function that increases supply. 
     *
     * @param _amount The amount of tokens to be added to supply.
     *
     */
    function increaseSupply(uint256 _amount) public onlyOwner
    {
        uint256 amount = _amount * 10 ** decimals();
        maxSupply += amount;
        availableSupply += amount;
    }

    /**
     * @dev A function that burns tokens from supply. 
     *
     * @param _amount The amount of tokens to be burned from supply.
     *
     */
    function burnSupply(uint256 _amount) public onlyOwner
    {
        uint256 amount = _amount * 10 ** decimals();
        require(availableSupply >= amount, "The selected burn amount is higher than the circulating supply.");
        require(maxSupply >= amount, "The selected burn amount is higher than the total supply.");
        maxSupply -= amount;
        availableSupply -= amount;      
    }
}