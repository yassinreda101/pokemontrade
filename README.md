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

1. **As a trainer, I want to sign up and login so I can manage my Pokémon collection securely.**

2. **As a trainer, I want to receive a set of random Pokémon upon registration, so I can start my collection.**

3. **As a trainer, I want to search for Pokémon by name, type, rarity so I can easily find the Pokémon I want.**

4. **As a trainer, I want to propose and accept trades with other players, so I can exchange Pokémon.**

5. **As a trainer, I want to list my Pokémon in the marketplace, so I can sell them to other users.**

6. **As a trainer, I want to purchase Pokémon from the marketplace so I can expand my collection.**

7. **As a trainer, I want AI trade recommendations, so I can make informed trading decisions.**

8. **As a trainer, I want to generate unique Pokémon images using DALL-E so I can customize my collection.**

9. **As a trainer, I want to participate in AI battles, so I can engage with my Pokémon in a fun way.**

10. **As a trainer, I want to earn badges and achievements, so I can track my progress and accomplishments.**

11. **As a trainer, I want to chat with other players, so I can negotiate trades and discuss strategies.**

12. **As an administrator, I want to monitor trading activity, so I can prevent fraudulent trades.**

13. **As an administrator, I want to manage user accounts, so I can ensure fair play.**

14. **As an administrator, I want to oversee API integrations, so I can maintain platform performance.**

15. **As a trainer, I want to be able to buy/update my collection with the newest release Pokémon.**

16. **As a trainer, I want to be able to see my Pokémon's stats, so I can see which ones I want to battle with.**

17. **As a trainer, I want to be able to see what I need to do to complete my achievements/earn badges.**

18. **As an administrator, I want to see AI battles between players to see how everyone is doing and make changes.**

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
