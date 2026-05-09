# QRKot — Cat Charity Fund v3
 
A donation platform for cat support projects with Google Sheets reporting.  
Built with FastAPI + FastAPI Users + SQLAlchemy + Alembic + Aiogoogle.
 
> **This is v3** — adds Google Sheets export via Google API.  
> [v1](https://github.com/vaultik/cat-charity-v1) — core donation logic only.  
> [v2](https://github.com/vaultik/cat-charity-v2) — adds user authentication.
 
## Features
 
- Create charity projects with a fundraising target
- Make donations — automatically invested into open projects (oldest first, FIFO)
- Track investment progress per project and per donation
- User authentication via FastAPI Users (JWT)
- Three access levels: anonymous, authenticated user, superuser/admin
- Export closed projects report to Google Sheets via Google API *(superuser only)*
- Pytest test suite

## Tech Stack

- **Python 3.9**
- **FastAPI 0.111.0**
- **FastAPI Users 13.0.0**
- **SQLAlchemy 2.0.29**
- **Alembic 1.7.7**
- **Pydantic 2.7.1**
- **Aiogoogle 5.13.0**
- **pytest 7.1.3**

Full list of dependencies: `requirements.txt`
 
## Google API Setup
 
Before running, you need a Google Cloud service account:
 
1. Go to [Google Cloud Console](https://console.cloud.google.com/) → create a project
2. Enable **Google Sheets API** and **Google Drive API**
3. Create a **Service Account** → download the JSON key file
4. Copy the credentials from the JSON into your `.env` (see below)

## How to Run
 
```bash
# Clone the repository
git clone https://github.com/vaultik/cat-charity-v3
cd cat-charity-v3
 
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
 
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
 
Create `.env` in the project root:
 
```env
APP_TITLE=QRKot
DATABASE_URL=sqlite+aiosqlite:///./qrkot.db
SECRET=your_secret_key
 
# Google Service Account credentials (from downloaded JSON key)
EMAIL=your-service-account@your-project.iam.gserviceaccount.com
PRIVATE_KEY_ID=your_private_key_id
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
```
 
```bash
# Apply migrations
alembic upgrade head
 
# Start the server
uvicorn app.main:app --reload
```
 
API docs available at `http://127.0.0.1:8000/docs`
 
## Access Levels
 
| Role | Permissions |
|---|---|
| Anonymous | Read charity projects |
| User | Make donations, view own donations |
| Superuser | Full CRUD on projects, view all donations, export to Sheets |
 
## API Examples
 
**POST** `/charity_project/` — create a project *(superuser only)*
 
```json
// Request body
{
  "name": "WowWow",
  "description": "Needs more",
  "full_amount": 1000
}
 
// Response 200
{
  "name": "WowWow",
  "description": "Needs more",
  "full_amount": 1000,
  "id": 3,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2025-12-19T17:21:24.032248"
}
```
 
**GET** `/google/` — export closed projects to Google Sheets *(superuser only)*
 
Returns a URL to the newly created spreadsheet with completed projects sorted by fundraising speed.
 
## Author
 
[github.com/vaultik](https://github.com/vaultik)
