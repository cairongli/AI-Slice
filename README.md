# AI Slice - Restaurant Order & Delivery System

AI-Enabled Online Restaurant Order & Delivery System built with React.js frontend and Python Flask backend.

## Features

- **Multi-User Platform**: Support for Customers, Chefs, Delivery Staff, and Managers
- **Menu Management**: Chefs can independently create and manage their dishes
- **Order System**: Customers can browse menus, add to cart, and place orders
- **Wallet System**: Digital wallet with VIP discounts (5% for VIP customers)
- **Delivery Bidding**: Delivery staff can bid on orders, lowest bidder wins automatically
- **AI Chat Assistant**: Intelligent support system with local knowledge base and LLM fallback
- **Reputation System**: Ratings and reviews affecting VIP status and user privileges
- **Manager Dashboard**: Process registrations, assign deliveries, and manage HR actions

## Project Structure

```
AI-Slice/
├── frontend/          # React.js frontend
│   ├── src/
│   │   ├── navComps/         # Navigation components
│   │   ├── userComps/         # Customer/User components
│   │   ├── SignInComps/        # Sign in components
│   │   ├── SignUpComps/        # Sign up components
│   │   ├── chefComps/          # Chef dashboard components
│   │   ├── deliveryComps/      # Delivery dashboard components
│   │   ├── managerComps/       # Manager dashboard components
│   │   ├── searchComps/        # Menu browsing components
│   │   ├── checkoutComps/      # Checkout components
│   │   ├── biddingComps/       # Bidding components
│   │   └── discussionComps/   # AI Chat components
│   └── package.json
├── backend/           # Python Flask backend
│   ├── app.py         # Main Flask application
│   └── requirements.txt
└── README.md
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
# OR
pip install -r requirements.txt 
```

3. Run the Flask server:
```bash
python3 app.py  
# OR
python app.py  
```
The backend API will be available at `http://localhost:5002`

## Mock Login Credentials

**Quick Login Examples:**
- Customer: `customer@test.com` / `customer123`
- VIP Customer: `vip@test.com` / `vip123`
- Chef: `chef@test.com` / `chef123`
- Delivery: `delivery@test.com` / `delivery123`
- Manager: `manager@test.com` / `manager123`

## Component Organization

Each major feature area has its own folder for easy navigation:

- **navComps/**: Navigation bar and routing
- **userComps/**: Homepage and customer dashboard
- **SignInComps/**: User authentication (sign in)
- **SignUpComps/**: User registration (sign up)
- **chefComps/**: Chef menu management and kitchen orders
- **deliveryComps/**: Delivery staff bidding and delivery tracking
- **managerComps/**: Manager dashboard for registrations and assignments
- **searchComps/**: Menu browsing and dish search
- **checkoutComps/**: Order checkout and payment processing
- **biddingComps/**: Delivery bidding interface
- **discussionComps/**: AI chat assistant interface

## Technologies Used

### Frontend
- React.js 
- React Router DOM
- Axios (for API calls)

### Backend
- Flask (Python web framework)
- Flask-CORS (for cross-origin requests)

