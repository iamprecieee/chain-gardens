# ✳️🌱 Chain Gardens 🌱✳️

Chain Gardens is an interactive blockchain-based virtual gardening platform where plants grow and change based on blockchain activity. This project integrates with the Abstract blockchain to create a dynamic gardening experience influenced by real blockchain metrics.

## Overview

Chain Gardens creates a unique connection between blockchain activity and virtual gardening. Users maintain a virtual garden where plant growth and health are directly influenced by their blockchain transactions and network conditions. The application monitors on-chain activities and translates them into garden events, creating an engaging gamified experience for DeFi users.

## Features

- **Web3 Authentication**: Secure wallet-based authentication with Abstract Global Wallet (AGW) integrated.
- **Dynamic Weather System**: Blockchain metrics influence garden weather conditions
- **Interactive Garden Management**: Plant, grow, and harvest various plant types
- **Real-time Blockchain Monitoring**: Tracks user activities and network conditions
- **Automated Growth System**: Plants grow based on multiple factors including weather and user activity
- **Pest Management System**: Dynamic challenges requiring specific blockchain actions to resolve
- **Performance Analytics**: Detailed statistics about garden health and growth efficiency

## Project Structure

```plaintext
chain-gardens/
├── base/                        # Django project configuration
├── blockchain/                  # Blockchain integration
│   ├── models.py                # Blockchain data models
│   ├── services.py              # Blockchain interaction services
│   └── tasks.py                 # Celery tasks
├── garden/                      # Garden management
│   ├── models.py                # Garden and plant models
│   ├── services.py              # Garden mechanics
│   └── views.py                 # API endpoints
├── user/                        # User authentication
│   ├── authentication.py        # Custom authentication
|   └── backends.py              # Custom authentication backend
│   └── models.py                # User models
|   └── views.py                 # Authentication endpoints
└── frontend/
    ├── src/
    │   ├── components/          # React components
    │   └── services/            # API and Web3 services
    └── public/
```

## Technical Architecture

### Backend (Django Rest Framework)
- REST API for garden management
- Celery tasks for blockchain monitoring
- Custom authentication system for wallet-based login
- Garden mechanics and growth calculations

### Frontend (React)
- Interactive garden interface
- Real-time updates and animations
- Web3 integration for blockchain interaction
- Responsive design for various screen sizes

### Blockchain Integration
- Abstract Global Wallet (AGW) integration
- Transaction monitoring and processing
- Network metrics collection
- Smart contract interaction

## Prerequisites

- Python 3.8+
- Node.js 16+
- Redis Server
- Abstract Chain Node access
- MetaMask or compatible Web3 wallet

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/iamprecieee/chain-gardens
cd chain-gardens
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations && python manage.py migrate
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

## Configuration

1. Create a `.env` file in the root directory:
```plaintext
SECRET_KEY_VALUE=your_django_secret_key
DEBUG_VALUE=true
ALLOWED_HOSTS_VALUE=localhost,127.0.0.1
ABSTRACT_RPC_URL=your_abstract_chain_rpc_url
ABSTRACT_CHAIN_ID=11124
ABSTRACT_EXPLORER_URL=https://explorer.testnet.abs.xyz
ABSTRACT_VERIFY_URL=https://verify.testnet.abs.xyz
REDIS_URL=your_redis_url
DATABASE_URL=your_database_url
```

2. Configure Celery:
```bash
# Start Redis server
redis-server

# Start Celery worker
celery -A base worker -l info

# Start Celery beat
celery -A base beat -l info
```

## Running the Application

1. Start the Django backend:
```bash
python manage.py runserver
```

2. Start the React frontend:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`


## Core Components

### Garden Management
- **PlantType**: Defines different plant varieties with unique growth characteristics
- **Plant**: Individual plant instances with growth stages and health metrics
- **Garden**: User's garden space with soil quality and environmental conditions

### Blockchain Integration
- **BlockchainMetrics**: Tracks network conditions affecting garden weather
- **WeatherState**: Translates blockchain metrics into garden weather conditions
- **BlockchainMonitor**: Monitors user activities and network state

### Authentication
- **WalletAuthentication**: Custom authentication using blockchain wallet signatures
- **UserAuthentication**: Manages authentication sessions and tokens

## API Documentation

### Authentication Endpoints
- **POST** `/api/v1/user/authenticate/`
  - Authenticates user with wallet signature
  - Returns authentication token

### Garden Endpoints
- **GET** `/api/v1/garden/`
  - Retrieves user's garden state
- **GET** `/api/v1/garden/status/`
  - Returns current garden conditions and weather
- **POST** `/api/v1/garden/plants/`
  - Plants new seed in specified position
- **DELETE** `/api/v1/garden/plants/{id}/`
  - Removes/harvests plant

## Game Mechanics

### Growth System
Plants grow based on multiple factors:
- Base growth rate of plant type
- Current weather conditions
- Soil quality
- Plant health
- User activity multipliers
- Pest damage (if present)

### Weather System
Weather conditions are determined by blockchain metrics:
- Network transaction volume
- Gas prices
- Network congestion
- Block times

### Pest System
Random pest infestations require specific blockchain actions to resolve:
- **Aphids**: Resolved by token transfers
- **Slugs**: Cleared by token swaps
- **Fungus**: Cured by staking activities

## Support

For support, please open an issue in the GitHub repository.

Live Link: [chain-gardens](https://chain-gardens.vercel.app)
