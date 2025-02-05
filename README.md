# 🚀 RentalHub - Online Tool & Equipment Rental Marketplace

RentalHub is a **Django-based** online rental platform that allows users to rent tools and equipment seamlessly. The platform features **Google authentication**, an **AI chatbot using Google GenAI**, **secure payments via Razorpay**, **email notifications on successful booking**, and an **advanced search functionality** to improve the rental experience.

---

## 🌐 Live Demo
🔗 **Try it now**: [RentalHub Live](https://shubham393.pythonanywhere.com/core/)  

---

## 📌 Features

✅ **Google Authentication** – Secure and fast login with Google.  
✅ **AI Chatbot** – Integrated with **Google Generative AI** for instant assistance.  
✅ **Razorpay Payment Gateway** – Safe and seamless online transactions.  
✅ **Email Notifications** – Get instant booking confirmation via email.  
✅ **Advanced Search** – Easily find tools using a powerful search engine.  
✅ **User-friendly UI** – Clean and responsive design for a great experience.  

---

## 🛠️ Tech Stack

### 📌 Frontend:
- **HTML5**
- **CSS3**
- **JavaScript**

### 📌 Backend:
- **Python**  
- **Django**  

### 📌 Database:
- **SQLite**  

### 📌 Authentication:
- **Google OAuth**  

### 📌 AI Integration:
- **Google Generative AI**  

### 📌 Payment Gateway:
- **Razorpay**  

### 📌 Email Service:
- **SMTP**  

---

## 🚀 Installation Guide

Follow these steps to **set up RentalHub locally**:

### 1️⃣ Clone the Repository
`
git clone https://github.com/Shubham-393/rentalhub.git
cd rentalhub`

### 2️⃣ Create and Activate Virtual Environment

`python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate`
### 3️⃣ Install Dependencies

`pip install -r requirements.txt`
### 4️⃣ Set Up Environment Variables
Create a .env file and add the following details:

` DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password `
5️⃣ Apply Migrations

`python manage.py migrate`
6️⃣ Run the Development Server

`python manage.py runserver`
Your project is now running at:
🔗 http://127.0.0.1:8000/

### 📖 Usage Guide
✅ **Login/Register** – Use Google Authentication to sign in.
✅ **Browse Tools** – Explore rental options using the search bar.
✅ **Ask AI Chatbot** – Get assistance with tool selection.
✅ **Book and Pay** – Select tools, choose rental dates, and pay via Razorpay.
✅ **Email Confirmation** – Receive instant email confirmation after booking.
### 📊 Project Structure
`
rentalhub/
│── core/               # Main app
│   ├── models.py       # Database models
│   ├── views.py        # Business logic
│   ├── urls.py         # URL routes
│   ├── templates/      # HTML templates
│   ├── static/         # Static files (CSS, JS)
│   ├── forms.py        # Django forms
│   ├── utils.py        # Helper functions
│── rentalhub/          # Django project settings
│   ├── settings.py     # Project configuration
│   ├── urls.py         # Main URL routing
│── requirements.txt    # Dependencies
│── manage.py           # Django management script
│── README.md           # Project documentation
`
### 🤝 Contributing
Contributions are welcome! Follow these steps to contribute:

Fork the Repository.
Create a New Branch:
`
git checkout -b feature-branch-name`
Commit Your Changes:
`
git commit -m 'Add new feature'`
Push to GitHub:
`
git push origin feature-branch-name`
Create a Pull Request.
### 📜 License
This project is licensed under the MIT License.

### 📞 Contact
If you have any questions, feel free to reach out:
📧 **Email**: khotshubham393@gmail.com
🔗 **GitHub**: Shubham-393

✨ Enjoy using RentalHub! Happy Renting! 🚀








