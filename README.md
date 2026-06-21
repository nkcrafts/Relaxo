# Relaxo - Focus & Break Timer

A gentle, colorful focus timer app that helps you stay productive with timed work sessions and break reminders.

## Features

- **Focus Buddy (app.py)**: Desktop break reminder with customizable work/break intervals
- **Relaxo (web/)**: Web-based goal tracker with timed focus sessions
- Pastel UI with encouraging messages
- Local storage for goal persistence
- Session tracking and statistics

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js (optional, for frontend development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nkcrafts/Relaxo.git
cd Relaxo
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

**Web Server (Relaxo):**
```bash
python server.py
```
Opens http://localhost:8000 in your browser.

**Desktop App (Focus Buddy):**
```bash
python app.py
```
Customize work/break times when prompted.

## Production Deployment

### Using Docker

Build and run with Docker:
```bash
docker build -t relaxo .
docker run -p 8000:8000 relaxo
```

### Environment Variables

Configure via `.env` file:
```
PORT=8000
HOST=0.0.0.0
WEB_FOLDER=web
ENVIRONMENT=production
DEBUG=false
```

### Deployment Options

- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo to Railway
- **Docker Hub**: Push image to registry
- **VPS**: Run Docker container on your server

## Project Structure

```
├── app.py                 # Desktop break reminder app
├── server.py             # Web server
├── index.html            # HTML entry point
├── web/
│   ├── index.html        # Web app HTML
│   ├── script.js         # Main app logic
│   └── styles.css        # Styling
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
└── .env                  # Environment variables
```

## Security Notes

- Uses localStorage for client-side data storage
- No server-side authentication required for local use
- For multi-user deployments, implement authentication
- Validate all user inputs
- Use HTTPS in production

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Development

To set up development environment:
```bash
pip install -r requirements.txt
# Run with DEBUG=true in .env
```

## License

MIT

## Author

Created with 💖 for focused, cozy work sessions.
