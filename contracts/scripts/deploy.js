const hre = require("hardhat");

async function main() {
  console.log("Deploying BankContract...");

  const BankContract = await hre.ethers.getContractFactory("BankContract");
  const bankContract = await BankContract.deploy();

  await bankContract.waitForDeployment();

  const address = await bankContract.getAddress();
  console.log("BankContract deployed to:", address);

  // Get ABI
  const contractArtifact = await hre.artifacts.readArtifact("BankContract");
  console.log("\nContract ABI (copy to frontend/config.js):");
  console.log(JSON.stringify(contractArtifact.abi, null, 2));

  console.log("\nPlease update:");
  console.log("1. CONTRACT_ADDRESS in backend/.env");
  console.log("2. CONTRACT_ADDRESS and CONTRACT_ABI in frontend/config.js");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

