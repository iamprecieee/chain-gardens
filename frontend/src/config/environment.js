const environment = {
  API_URL: process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1",
  CHAIN_ID: process.env.REACT_APP_CHAIN_ID || "0x2B74",
  CHAIN_NAME: process.env.REACT_APP_CHAIN_NAME || "Abstract Testnet",
  RPC_URL: process.env.REACT_APP_RPC_URL || "https://api.testnet.abs.xyz",
  EXPLORER_URL:
    process.env.REACT_APP_EXPLORER_URL || "https://explorer.testnet.abs.xyz",
  PAYMASTER_ADDRESS:
    process.env.REACT_APP_PAYMASTER_ADDRESS ||
    "0x5407B5040dec3D339A9247f3654E59EEccbb6391",
  POLLING_INTERVAL: parseInt(
    process.env.REACT_APP_POLLING_INTERVAL || "30000",
    10
  ),
};

export default environment;
