# Restaurant Bot

A customer support bot for restaurants with specialized agents for handling menu inquiries, orders, and reservations.

## Project Structure

```
restaurant-bot/
├── my_agents/
│   ├── triage_agent.py          # Routes customer requests to appropriate agents
│   ├── menu_agent.py            # Handles menu inquiries
│   ├── order_agent.py           # Processes customer orders
│   └── reservation_agent.py     # Manages restaurant reservations
├── main.py                      # Main entry point
├── models.py                    # Data models
├── pyproject.toml              # Project configuration
├── .python-version             # Python version specification
└── README.md                   # This file
```

## Getting Started

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the bot:
   ```bash
   python main.py
   ```

## Agents

- **Triage Agent**: Routes incoming customer requests to the appropriate agent
- **Menu Agent**: Provides menu information and recommendations
- **Order Agent**: Processes and manages customer orders
- **Reservation Agent**: Handles restaurant reservations
