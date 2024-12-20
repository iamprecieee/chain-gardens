import React, { useState, useEffect } from "react";
import {
  initializeProvider,
  connectWallet,
  signMessage,
} from "./services/web3";
import {
  setAuthToken,
  authenticate,
  disconnect,
  api,
  getGardenDetails,
  getCurrentWeather,
  getPlantTypes,
  plantSeed,
  removePlant,
} from "./services/api";
import { GardenView } from "./components/GardenView";
import { PlantDetails } from "./components/PlantDetails";
import { GardenStats } from "./components/GardenStats";
import { PestAlert } from "./components/PestAlert";
import { ActivityStatus } from "./components/ActivityStatus";

function App() {
  // Authentication state
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [address, setAddress] = useState("");
  const [authToken, setUserAuthToken] = useState("");
  const [smartWalletAddress, setSmartWalletAddress] = useState("");
  const [, setAgwClient] = useState(null);

  // Response state
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  // Garden state
  const [garden, setGarden] = useState(null);
  const [weather, setWeather] = useState(null);
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [plantTypes, setPlantTypes] = useState([]);

  // Initialize web3
  useEffect(() => {
    let isMounted = true;
    let accountLength = 1;

    const init = async () => {
      try {
        const networkProvider = await initializeProvider();
        if (isMounted) {
          setProvider(networkProvider);

          const handleAccountsChanged = async (accounts) => {
            console.log("Accounts changed:", accounts);
            if (accounts.length === 0) {
              accountLength = 0;
            }
            if (accountLength === 1) {
              await disconnect();
            }
            if (accounts.length === 1) {
              accountLength = 1;
            }
            setSigner(null);
            setAddress("");
            setUserAuthToken("");
            setAuthToken("");
            setSmartWalletAddress("");
            setAgwClient(null);
            // Clear the Authorization header
            delete api.defaults.headers.common["Authorization"];
          };
          // Remove any existing listeners first
          window.ethereum.removeAllListeners("accountsChanged");
          // Add new event listener
          window.ethereum.on("accountsChanged", handleAccountsChanged);
        }
      } catch (err) {
        showError(err.message);
      }
    };
    init();
    // Cleanup function to remove the specific listener
    return () => {
      isMounted = false;
      window.ethereum.removeAllListeners("accountsChanged");
    };
  }, []);

  // Connect wallet
  const connectUserWallet = async () => {
    try {
      setLoading(true);
      showStatus("Connecting wallet...");
      // const { signer, address } = await connectWallet(provider);
      const {
        signer,
        address,
        smartWalletAddress,
        agwClient: client,
      } = await connectWallet(provider);
      setSigner(signer);
      setAddress(address);
      setSmartWalletAddress(smartWalletAddress);
      setAgwClient(client);
      showStatus("Wallet connected");
    } catch (err) {
      showError("Failed to connect wallet: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Authenticate user
  const authenticateUser = async () => {
    try {
      setLoading(true);
      showStatus("Authenticating...");
      // Create and sign transaction to prove ownership
      const message = `Sign in to Chain Gardens with wallet: ${address.toLowerCase()}`;
      const signature = await signMessage(signer, message);
      // Call the authentication endpoint with signature and address
      const { token } = await authenticate(address, signature);
      setUserAuthToken(token);
      setAuthToken(token);
      showStatus("Authentication successful");
      await loadGardenData();
    } catch (err) {
      if (
        typeof err.message === "string" &&
        err.message.includes("user rejected")
      ) {
        showError("User rejected the request.");
      } else {
        showError(err.message || "Connection failed");
      }
    } finally {
      setLoading(false);
    }
  };

  // Load garden data
  useEffect(() => {
    if (authToken) {
      loadGardenData();
      const interval = setInterval(loadGardenData, 30000); // Every 30 seconds
      return () => clearInterval(interval);
    }
  }, [authToken]);

  const loadGardenData = async () => {
    try {
      const [gardenData, weatherData, types] = await Promise.all([
        getGardenDetails(),
        getCurrentWeather(),
        getPlantTypes(),
      ]);

      setGarden(gardenData);
      setWeather(weatherData);
      setPlantTypes(types);
    } catch (err) {
      console.error("Failed to load garden data:", err);
      setWeather(null);
    }
  };

  const handlePlant = async (slotPosition, plantTypeId) => {
    try {
      setLoading(true);
      setStatus("Planting...");

      await plantSeed(slotPosition, plantTypeId);
      await loadGardenData();

      setStatus("Plant added successfully");
    } catch (err) {
      setError("Failed to plant: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (plantId) => {
    try {
      setLoading(true);
      setStatus("Harvesting...");

      await removePlant(plantId);
      await loadGardenData();

      setStatus("Plant removed successfully");
    } catch (err) {
      setError("Failed to remove: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper function to show and auto-dismiss messages
  const showStatus = (message, duration = 3000) => {
    setStatus(message);
    setIsVisible(true);

    const timer = setTimeout(() => {
      setStatus("");
      setIsVisible(false);
    }, duration);

    return () => clearTimeout(timer);
  };

  const showError = (message, duration = 3000) => {
    setError(message);
    setIsVisible(true);

    const timer = setTimeout(() => {
      setError("");
      setIsVisible(false);
    }, duration);

    return () => clearTimeout(timer);
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-black font-mono">
      <div className="max-w-7xl mx-auto bg-green-500 rounded-lg shadow-md p-8">
        <header className="text-center mb-8">
          <h1 className="bg-indigo-700 px-1 py-3 rounded-md text-center text-3xl font-extrabold text-white mb-8">
            ✳️🌱Chain Gardens🌱✳️
          </h1>
          {!address ? (
            <button
              onClick={connectUserWallet}
              disabled={loading}
              className="w-full flex justify-center py-2 px-1 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-indigo-700 hover:bg-indigo-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {loading ? "Connecting..." : "Connect Wallet"}
            </button>
          ) : !authToken ? (
            <button
              onClick={authenticateUser}
              disabled={loading}
              className="w-full flex justify-center py-2 px-1 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-indigo-700 hover:bg-indigo-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              {loading ? "Authenticating..." : "Authenticate"}
            </button>
          ) : (
            <div className="mt-4 space-y-2">
              <div className="text-center font-bold text-black">
                EOA: {address.slice(0, 6)}...{address.slice(-4)}
              </div>
              <div className="text-center font-bold text-black">
                Smart Wallet: {smartWalletAddress.slice(0, 6)}...
                {smartWalletAddress.slice(-4)}
              </div>
            </div>
          )}
        </header>

        {authToken && garden && (
          <div className="mt-8 space-y-8">
            <PestAlert garden={garden} />
            <ActivityStatus garden={garden} />
            <div className="bg-black rounded-lg border-2 border-indigo-900/20 shadow-inner p-8">
              <GardenView
                garden={garden}
                weather={weather}
                onPlant={handlePlant}
                onRemove={handleRemove}
                availablePlants={plantTypes}
                onSelectPlant={setSelectedPlant}
              />
            </div>
            <div className="bg-black rounded-lg border-2 border-indigo-900/20 shadow-inner p-8">
              <GardenStats garden={garden} weather={weather} />
            </div>
          </div>
        )}

        {selectedPlant && (
          <PlantDetails
            plant={selectedPlant}
            onClose={() => setSelectedPlant(null)}
          />
        )}

        {(error || status) && (
          <div
            className={`
              p-4 rounded-md text-center font-medium
              ${error ? "bg-red-100 text-red-700" : "bg-blue-100 text-blue-700"}
              transition-opacity duration-500 
              ${isVisible ? "opacity-100" : "opacity-0"}
            `}
          >
            {error || status}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
