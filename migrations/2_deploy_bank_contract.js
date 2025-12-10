const BankContract = artifacts.require("BankContract");

module.exports = function (deployer) {
  console.log("Deploying BankContract...");
  
  deployer.deploy(BankContract).then((instance) => {
    console.log("BankContract deployed to:", instance.address);
    
    // Get ABI from the contract artifact (will be available after compilation)
    console.log("\nAfter migration, you can find the ABI in:");
    console.log("build/contracts/BankContract.json");
    
    console.log("\nPlease update:");
    console.log("1. CONTRACT_ADDRESS in backend/.env");
    console.log("2. CONTRACT_ADDRESS and CONTRACT_ABI in frontend/config.js");
    console.log("   (Copy ABI from build/contracts/BankContract.json)");
  });
};

