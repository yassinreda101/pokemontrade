# ⭐ Pokémon Trading App

Welcome to the **Pokémon Trading App**, the ultimate platform for Pokémon enthusiasts to collect, trade, battle, and customize their Pokémon! Built with Django and integrated with AI services, this app offers a full-featured experience for trainers at Georgia Tech and beyond.

---

## 📖 Table of Contents
- [Features](#features)
- [User Stories](#user-stories)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Meet the Team](#meet-the-team)
- [License](#license)

---

## ✨ Features
- 👤 **User Registration/Login**
- 🔀 **Starter Pokémon Assignment**
- 🔎 **Search Pokémon by Name, Type, or Rarity**
- 📦 **Marketplace to Buy and Sell Pokémon**
- 🤝 **Propose, Accept, and Reject Trades**
- 🧠 **AI-Powered Trade Recommendations**
- 💥 **AI-Driven Pokémon Battles**
- 🎨 **Custom Pokémon Generation with DALL-E**
- 🏆 **Achievements and Badges**
- 💬 **Real-time Chat System**
- 🛡️ **Admin Monitoring for Fair Play and Fraud Prevention**

---

## 📚 User Stories
- As a trainer, sign up and receive a random starter set of Pokémon.
- Search for Pokémon easily.
- List your Pokémon for trade or marketplace sale.
- Propose and accept trades with others.
- Get trade recommendations powered by AI.
- Create custom Pokémon designs.
- Battle with other trainers through AI-simulated matches.
- Track your badges and achievements.
- Chat with fellow trainers.

Admin functionality includes:
- Managing trades and preventing fraud.
- Managing user accounts and API integrations.
- Monitoring AI battles.

---

## 🛠 Technologies Used
- **Backend:** Django (Python)
- **Database:** SQLite (Development)
- **Frontend:** Django Templates + Bootstrap
- **External APIs:**
  - PokeAPI for Pokémon data
  - Pokémon TCG API for card simulations
  - OpenAI API for AI battles and DALL-E image generation
- **Authentication:** Django's built-in auth system
- **Architecture:** Client-Server, Factory Method Pattern, Observer Pattern

---

## 📚 Getting Started

### Prerequisites
- Python 3.10+
- Django 4+
- Virtualenv (optional but recommended)

### Installation

```bash
# Clone the repository
$ git clone https://github.com/your-username/pokemon-trading-app.git
$ cd pokemon-trading-app

# Create and activate a virtual environment
$ python -m venv venv
$ source venv/bin/activate   # Mac/Linux
$ venv\Scripts\activate     # Windows

# Install dependencies
$ pip install -r requirements.txt

# Setup environment variables
Create a `.env` file:
SECRET_KEY=your_django_secret_key
OPENAI_API_KEY=your_openai_api_key
POKEMONTCG_API_KEY=your_pokemontcg_api_key

# Apply migrations
$ python manage.py migrate

# Create a superuser
$ python manage.py createsuperuser

# Run the server
$ python manage.py runserver
```

Access the app at `http://127.0.0.1:8000/`

---

## 🛠️ Architecture
- **Accounts App**: Handles registration, login, profile, XP system.
- **Pokémons App**: Manages Pokémon entities, custom creations, and stats.
- **Marketplace App**: Enables buying/selling Pokémon.
- **Trades App**: Manages trade proposals and acceptances.
- **Battles App**: Simulates AI-based Pokémon battles.
- **Achievements App**: Tracks user accomplishments.
- **Chat App**: Real-time communication between trainers.

**Design Patterns Used:**
- **Factory Method** for Pokémon creation.
- **Observer Pattern** for trade notifications.

---

## 👨‍💻 Meet the Team
This app was built by a passionate team of Georgia Tech students as part of our CS 2340 project. We combined expertise in backend development, frontend design, AI integration, and software architecture.

---

## 📅 License
This project is for educational purposes only.

---

> "Gotta catch 'em all — and trade 'em too!" 🖊️

---

# 💡 Quick Links
- [PokeAPI](https://pokeapi.co/)
- [Pokemon TCG API](https://pokemontcg.io/)
- [OpenAI API](https://platform.openai.com/)

---
