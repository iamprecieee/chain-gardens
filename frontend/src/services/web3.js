import { ethers } from "ethers";
import {
  createAbstractClient,
  getSmartAccountAddressFromInitialSigner,
} from "@abstract-foundation/agw-client";
import { createPublicClient, http } from "viem";
import { abstractTestnet } from "viem/chains";
import environment from "../config/environment";

export const initializeProvider = async () => {
  if (!window.ethereum) {
    throw new Error("Please install MetaMask.");
  }
  try {
    await window.ethereum.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: environment.CHAIN_ID }], // 11124 in hex
    });
  } catch (err) {
    // Adds chain if non-existent
    await window.ethereum.request({
      method: "wallet_addEthereumChain",
      params: [
        {
          chainId: environment.CHAIN_ID,
          chainName: environment.CHAIN_NAME,
          rpcUrls: [environment.RPC_URL],
          nativeCurrency: {
            name: "Ethereum",
            symbol: "ETH",
            decimals: 18,
          },
          blockExplorerUrls: [environment.EXPLORER_URL],
        },
      ],
    });
  }
  const provider = new ethers.BrowserProvider(window.ethereum);
  return provider;
};

export const connectWallet = async (provider) => {
  // Check connected network
  const network = await provider.getNetwork();
  if (network.chainId !== 11124n) {
    throw new Error("Please switch to Abstract Chain.");
  }
  const signer = await provider.getSigner();
  const address = await signer.getAddress();
  // Initialize public client for AGW address derivation
  const publicClient = createPublicClient({
    chain: abstractTestnet,
    transport: http(),
  });
  // Get the AGW smart contract address for this signer
  const smartWalletAddress = await getSmartAccountAddressFromInitialSigner(
    address,
    publicClient
  );
  // Initialize AGW client
  const agwClient = await createAbstractClient({
    chain: abstractTestnet,
    signer: {
      address,
      signMessage: (message) => signer.signMessage(message),
      signTransaction: (tx) => signer.signTransaction(tx),
    },
  });
  return {
    signer,
    address,
    smartWalletAddress,
    agwClient,
  };
};

export const signMessage = async (signer, message) => {
  return await signer.signMessage(message);
};
