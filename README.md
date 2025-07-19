# 🏥 Triage Assist Locator

**Triage Assist Locator** is a command-line emergency triage assistant that helps users quickly find the nearest hospital based on their current location and the severity of an emergency. Designed for both ordinary users and medical facilities, it provides fast, intuitive, and offline-ready recommendations with estimated arrival times (ETA).

---

## 🚀 Features

- 🔍 Locate nearby hospitals based on injury severity
- 🧭 Calculate estimated time of arrival (ETA) using distance
- 🌐 Geocode user location (e.g., "Yaba, Lagos") into coordinates
- 🏥 Structured hospital database with geo-coordinates and specializations
- 🧠 Uses Python generators, async functions, and decorators for efficient data handling
- 📜 Logs user actions with timestamps using Python’s logging module

---

## 🛠 Tech Stack

- **Python 3.12+**
- **CLI-based interface** using built-in modules
- **Asyncio** for simulated I/O handling
- **Decorators** for logging and validation
- **Generators** for lazy data loading
- **Geolocation APIs** (Nominatim via geopy) for live user coordinates
- **MySQL** for hospital data storage (async access via aiomysql)

---

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- MySQL server (for hospital database)
- Git

### Clone the Repository

```bash
git clone https://github.com/elvisibenacho/TriageAssist.git
cd TriageAssist
```

### Install Dependencies

#### On Ubuntu

1. **Install Python 3.12 and pip:**
   ```bash
   sudo apt update
   sudo apt install python3.12 python3.12-venv python3-pip
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3.12 -m venv env
   source env/bin/activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL and environment variables:**
   - Install MySQL: `sudo apt install mysql-server`
   - Create a `.env` file in the project root with your DB credentials:
     ```
     HOST=localhost
     USER=your_mysql_user
     PASSWORD=your_mysql_password
     PORT=3306
     DATABASE_NAME=triage_db
     ```

#### On Windows

1. **Install Python 3.12 and pip:**
   - Download from [python.org](https://www.python.org/downloads/).
   - Add Python to your PATH during installation.

2. **Create and activate a virtual environment:**
   ```cmd
   python -m venv env
   .\env\Scripts\activate
   ```

3. **Install required packages:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Set up MySQL and environment variables:**
   - Download and install MySQL from [mysql.com](https://dev.mysql.com/downloads/installer/).
   - Create a `.env` file in the project root with your DB credentials as shown above.

---

## 📦 Required Packages

All dependencies are listed in [`requirements.txt`](requirements.txt):

- `aiomysql==0.2.0`
- `geographiclib==2.0`
- `geopy==2.4.1`
- `PyMySQL==1.1.1`
- `python-dotenv==1.1.1`

Install them with:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the application from the project root:

```bash
python3 -m  main.triage_locator.py or
python -m main.triage_locator.py
```

Follow the on-screen prompts to enter your name, location, and emergency severity. The program will display the top 5 nearest hospitals with ETA and distance.

---


## 🤝 Contributing

This project is open for collaboration! Contributions are welcome from the open-source community. To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes
4. Push to your fork and submit a pull request

Please ensure your code follows the existing style and includes appropriate documentation.

---

## 📄 License

This project is licensed under the MIT License.

---

## 💬 Contact

For questions, suggestions, or collaboration, open an issue or contact the maintainer via GitHub.

---

**Triage Assist Locator** — Empowering communities with fast, reliable
