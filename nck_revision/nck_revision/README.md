# 🏥 NCK Prep — Nursing Council of Kenya Exam Revision App

A mobile-first web app for nursing students to revise for NCK exams (BSN & KRCHN), with M-PESA subscription payment and admin approval system.

## Features
- 📚 BSN & KRCHN question banks with category filtering
- 💚 M-PESA payment (Send Money to 0114245222 — KES 200/month)
- ✅ Admin approves students after verifying M-PESA code
- 🃏 Tap-to-reveal answer cards
- 🔍 Search and filter by topic/difficulty
- 📱 Mobile-first responsive design
- 🔐 Secure authentication

## Quick Setup

### 1. Install Python & Django
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations questions
python manage.py migrate
```

### 3. Load Sample Data & Create Admin
```bash
python setup_data.py
```
This creates:
- Admin: **username=admin**, **password=admin1234**
- Sample categories (BSN & KRCHN)
- 10 sample exam questions

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Access the App
| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/` | Student home (questions) |
| `http://127.0.0.1:8000/accounts/login/` | Login |
| `http://127.0.0.1:8000/accounts/register/` | Student registration |
| `http://127.0.0.1:8000/admin-panel/` | Admin dashboard |
| `http://127.0.0.1:8000/admin/` | Django admin |

## How the Payment Flow Works
1. Student registers → redirected to payment page
2. Student sends KES 200 via M-PESA **Send Money** to **0114245222**
3. Student pastes their M-PESA transaction code
4. Admin logs into `/admin-panel/` and clicks **Approve**
5. Student is automatically granted access to questions

## Admin Guide
- **Add Questions**: Admin Panel → Add Question
- **Manage Categories**: Admin Panel → Manage Categories
- **Approve Payments**: Admin Panel → Dashboard (pending payments shown)
- **Django Admin**: `/admin/` for full database access

## Project Structure
```
nck_revision/
├── nck_revision/          # Django project settings
├── accounts/              # Auth, payments, users
│   ├── models.py          # CustomUser, Payment
│   ├── views.py           # Login, register, payment
│   └── admin.py           # Admin for users/payments
├── questions/             # Question bank
│   ├── models.py          # Category, Question
│   ├── views.py           # Home, admin panel views
│   └── forms.py           # Question/category forms
├── templates/             # HTML templates
│   ├── base.html
│   ├── accounts/          # login, register, payment
│   ├── questions/         # home (question cards)
│   └── admin_panel/       # dashboard, questions mgmt
├── static/
│   ├── css/style.css      # Mobile-first styles
│   └── js/main.js         # Toggle answers, UX
├── setup_data.py          # Quick setup script
├── requirements.txt
└── manage.py
```

## Deployment (Production)
For production, update `settings.py`:
```python
DEBUG = False
SECRET_KEY = 'your-secure-random-key'
ALLOWED_HOSTS = ['yourdomain.com']
```
Then run `python manage.py collectstatic`.

## GitHub Upload
```bash
git init
git add .
git commit -m "Initial NCK Prep app"
git remote add origin https://github.com/yourusername/nck-prep.git
git push -u origin main
```
