
<div align="center">

# Football Prediction

![License](https://img.shields.io/github/license/fernandosc14/football-prediction)
![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Stars](https://img.shields.io/github/stars/fernandosc14/football-prediction?style=social)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support%20me-yellow?logo=buy-me-a-coffee&style=flat)](https://buymeacoffee.com/fernandosc14)

</div>


<details>
   <summary>Table of Contents</summary>

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

</details>


## Description

Football Prediction is a modern, data-driven platform for forecasting football match outcomes.
It leverages machine learning models and real-time data to provide accurate predictions, confidence scores, and insights.

**Key Features:**
- Predict match results, double chance, over/under goals, and BTTS.
- Interactive frontend built with Next.js and Tailwind CSS.
- Automated data fetching and model training.
- REST API for integration and custom queries.
- Scheduled updates via cloud automation.

**New in v1.0.0:**
- Improved authentication and API security
- Enhanced error handling and startup validation
- Stable production-ready configuration

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/fernandosc14/football-prediction.git
   cd football-prediction
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root and add your secrets (see [Configuration](#configuration)).

5. **Run the backend:**
   ```bash
   uvicorn src.api:app --reload
   ```

6. **Run the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

## Usage

- Access the frontend at `http://localhost:3000`
- Use the REST API endpoints (see API docs for details)
- Example API call:
  ```bash
  curl http://localhost:8000/predictions
  ```

- Run the weekly update script:
  ```bash
  python scripts/run_weekly.py
  ```

## Configuration

Set the following environment variables in your `.env` file:

```env
REDIS_URL=your_redis_url
API_KEY=your_api_key
ENDPOINT_API_KEY=your_endpoint_api_key
```

Other optional settings can be found in `config.yaml` and `frontend/.env.local`.

## Contributing

We welcome contributions! To get started:

- Fork the repository
- Create a new branch (`git checkout -b feature/your-feature`)
- Commit your changes
- Open a pull request

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and ensure all tests pass before submitting.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Upstash Redis](https://upstash.com/)
- [Render](https://render.com/)
- [SoccerDataAPI](https://soccerdataapi.com/)
- Special thanks to all contributors and the open-source community!
