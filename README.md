# 🌌 SkillXchange

> **The world's most innovative peer-to-peer skill-swapping network.** Connect with peers, share expertise, and grow together in a professional ecosystem without spending a penny.

---

## ✨ Features

* **🌌 Ultra-Premium Visual Theme**: Designed with a sleek obsidian-dark cosmic backdrop, glowing neon details, ambient backing lighting blobs, and micro-interactive elements.
* **✍️ High-End Typography**: Styled with the beautiful and clean geometric **Outfit** display font and readable **Plus Jakarta Sans** for rich visual clarity.
* **📥 Advanced Collaboration Inbox**: Manage incoming match requests and outbox proposals seamlessly.
* **💬 Real-Time Aura Chat**: Embedded peer messaging running on **Socket.IO** and **MongoDB** for seamless communication.
* **🛠️ Django + SQLite Engine**: Highly-secured core data, authentication, profiles, and custom models powered by Django.
* **🎛️ Live Control Panel (Feature Highlight)**: Real-time, dual-pane customization environment allowing staff administrators to modify homepage headlines, features, and testimonials on the fly with live visual feedback.

---

## 🎛️ Live Control Panel Feature

SkillXchange comes equipped with a custom-engineered **Live Control Panel** (`/admin-portal/live-editor/`) that elevates landing page management to a premium interactive experience:

* **Dual-Pane Design**: Edit title, subtitle, CTA text, features, and customer testimonials in the left panel, and see updates instantly reflected in a high-fidelity visual preview on the right.
* **Dynamic Component Management**: Instantly add, modify, or delete showcase feature cards and community success stories.
* **Instant DB Sync**: When satisfied, hit the save action to securely sync adjustments directly into the database.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* MongoDB (Optional: required for chat functionality)

### Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pm023/SkillXchange.git
   cd SkillXchange
   ```

2. **Activate the Virtual Environment**:
   * On Windows:
     ```powershell
     .\venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory (based on `.env.example` if available, or fill in these parameters):
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   MONGODB_URI=mongodb://127.0.0.1:27017/
   MONGODB_NAME=skillxchange_db
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**:
   Run the application on a custom port to avoid local port collisions:
   ```bash
   python manage.py runserver 8002
   ```

---

## 🔐 Administrative Access

A pre-configured superuser account exists for testing both the Django Admin Dashboard and the Live Control Panel:

* **Django Standard Admin Site**: `http://127.0.0.1:8002/secure-admin/`
* **Custom Live Control Panel**: `http://127.0.0.1:8002/admin-portal/`
* **Username**: `admin`
* **Password**: `admin123`

---

## 💡 Troubleshooting: CSRF Verification Failures

During local development or when testing across multiple forwarded ports (e.g. switching between port 8000 and 8002), you may encounter a **403 Forbidden: CSRF verification failed** page. 

**Quick Solutions**:
1. **Clear Cookie Cache**: Open your browser dev tools, clear all site cookies and local storage for `127.0.0.1` or `localhost`, and refresh.
2. **Use Incognito Mode**: Open a private/incognito window to load `http://127.0.0.1:8002/`. This ensures a fresh, conflict-free session.

---

*Made with 💜 for the Skill Sharing Community.*
