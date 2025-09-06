# Smart Inventory & Business Management System

A comprehensive inventory management and business operations platform designed for small and medium businesses. Built with modern technologies to provide real-time inventory tracking, invoicing, accounting, and business analytics.

## 🚀 Features

### Core Functionality
- **📦 Inventory Management**: Track products, stock levels, and receive low-stock alerts
- **📄 Invoicing System**: Create, manage, and track invoices with payment recording
- **💰 Accounting**: Basic double-entry bookkeeping and financial reporting
- **📊 Dashboard Analytics**: Real-time business metrics and insights
- **📈 Excel Export**: Export data to Excel for further analysis
- **🔔 Smart Alerts**: Automatic notifications for low stock and overdue invoices

### Technical Features
- **RESTful API**: Built with FastAPI for high performance
- **Real-time Updates**: Live dashboard statistics
- **Responsive Design**: Works on desktop and mobile devices
- **Data Export**: Excel integration for reports and data analysis

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily upgradeable to PostgreSQL)
- **Pydantic** - Data validation using Python type annotations
- **Pandas** - Data manipulation and Excel export
- **Python 3.8+** - Programming language

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Router** - Navigation
- **Heroicons** - Beautiful hand-crafted SVG icons

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-inventory-system.git
cd smart-inventory-system
```

### 2. Backend Setup

#### Navigate to backend directory:
```bash
cd backend
```

#### Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Python dependencies:
```bash
pip install -r requirements.txt
```

#### Create .env file (if not exists):
```bash
# The .env file is already created with default settings
# You can modify it for production use
```

#### Run the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
API documentation will be at `http://localhost:8000/docs`

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

#### Install dependencies:
```bash
npm install
```

#### Start the development server:
```bash
npm start
```

The frontend application will be available at `http://localhost:3000`

## 🚀 Quick Start Guide

### 1. Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
# Run server
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 2. Access the Application

1. Open your browser and go to `http://localhost:3000`
2. You'll see the dashboard with business metrics
3. Navigate using the sidebar menu

### 3. Basic Usage

#### Adding Products:
1. Click on "Products" in the sidebar
2. Click "Add Product" button
3. Fill in product details (SKU, name, price, stock levels)
4. Click "Create" to save

#### Managing Inventory:
- View all products in the Products page
- Click the edit icon to update product details
- Monitor stock levels with color-coded indicators:
  - 🟢 Green: In Stock
  - 🟡 Yellow: Low Stock
  - 🔴 Red: Out of Stock

#### Exporting Data:
- Click the "Export" button on any page to download Excel reports
- Reports include comprehensive inventory data and analytics

## 📁 Project Structure

```
smart-inventory-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/    # API route handlers
│   │   ├── core/             # Core configuration
│   │   ├── database/         # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   └── App.tsx          # Main application
│   ├── package.json         # Node dependencies
│   └── tailwind.config.js  # Tailwind configuration
└── README.md
```

## 🔌 API Endpoints

### Products
- `GET /api/v1/products` - List all products
- `POST /api/v1/products` - Create new product
- `GET /api/v1/products/{id}` - Get product details
- `PATCH /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product
- `POST /api/v1/products/{id}/stock` - Update stock level

### Invoices
- `GET /api/v1/invoices` - List all invoices
- `POST /api/v1/invoices` - Create new invoice
- `GET /api/v1/invoices/{id}` - Get invoice details
- `PATCH /api/v1/invoices/{id}` - Update invoice
- `POST /api/v1/invoices/{id}/payment` - Record payment

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard statistics

### Exports
- `GET /api/v1/export/products` - Export products to Excel
- `GET /api/v1/export/invoices` - Export invoices to Excel
- `GET /api/v1/export/inventory-report` - Export inventory report

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Deployment

### Production Build

#### Backend:
```bash
cd backend
# Use production WSGI server
gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000
```

#### Frontend:
```bash
cd frontend
npm run build
# Serve the build folder with any static file server
```

### Environment Variables

Create a `.env` file in the backend directory with:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_VERSION=v1
DEBUG=False
```

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Multi-tenant support
- [ ] Advanced reporting and analytics
- [ ] Mobile application
- [ ] Barcode scanning
- [ ] Email notifications
- [ ] Supplier management
- [ ] Purchase order system
- [ ] Customer relationship management (CRM)
- [ ] AI-powered demand forecasting
- [ ] Integration with accounting software
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💼 Career Impact

This project demonstrates proficiency in:
- Full-stack development with modern frameworks
- RESTful API design and implementation
- Database design and management
- Frontend development with React and TypeScript
- Business logic implementation
- Data export and reporting capabilities
- Clean code architecture and best practices

Perfect for showcasing skills to companies like Amazon, Microsoft, or any tech-forward organization looking for talented developers with business acumen.

## 📧 Contact

Jose Herrera - hejoric@outlook.com

Project Link: [[https://github.com/yourusername/smart-inventory-system](https://github.com/yourusername/smart-inventory-system)](https://github.com/hejoric/smart-inventory-system)

---

**Built with ❤️ for small businesses everywhere**
