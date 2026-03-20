# AI-Driven Enterprise Decision Copilot

An AI-driven Enterprise Decision Copilot that enables non-technical users to query a realistic e-commerce ERP dataset using natural language and receive explainable, business-ready insights.

---

## 🎯 Problem Statement

Modern enterprises generate large volumes of structured operational and transactional data across customers, sellers, products, inventory, logistics, payments, and returns. While this data is stored in relational databases, effective access remains difficult for non-technical users.

Traditional dashboards fail when:
- Business users ask ad-hoc questions
- Insights require cross-domain reasoning
- Users want explanations, not just numbers

---

## 🏗️ Project Architecture

This project follows a **progressive complexity approach**:

| Stage | Name | Description | Status |
|-------|------|-------------|--------|
| 1 | Dataset Design & Population | Enterprise-grade PostgreSQL dataset | 🟢 Current |
| 2 | Data Access Layer | Backend service for safe queries | ⚪ Planned |
| 3 | Natural Language to SQL | NL queries → SQL execution | ⚪ Planned |
| 4 | Agentic RAG | Intent, validation, explanation agents | ⚪ Planned |
| 5 | Explainable Insights | Business summaries & recommendations | ⚪ Planned |
| 6 | Deployment & Demo | Supabase + Vercel deployment | ⚪ Planned |

---

## 🛒 Industry Context

Modeled on a **Myntra-like fashion e-commerce marketplace**:
- Marketplace model (customers + sellers)
- Large product catalog with fashion-specific attributes
- High return and refund rates (~25-30%)
- Inventory distributed across multiple warehouses
- Complex logistics and seller settlements

---

## 📊 Dataset Overview (Stage 1)

### 13 Interrelated Tables

| Table | Description | ~Rows |
|-------|-------------|-------|
| customers | Customer profiles & segments | 1,000 |
| sellers | Seller onboarding & ratings | 150 |
| products | Product catalog with attributes | 2,000 |
| warehouses | Warehouse locations | 10 |
| inventory | Stock levels per product/warehouse | 5,000 |
| inventory_movements | Stock changes over time | 25,000 |
| orders | Customer orders | 8,000 |
| order_items | Individual items in orders | 18,000 |
| payments | Payment transactions | 8,000 |
| shipments | Delivery tracking | 8,000 |
| returns | Return requests | 2,500 |
| refunds | Refund processing | 2,500 |
| seller_settlements | Seller payouts | 12,000 |

**Total:** ~90,000 rows (Supabase free-tier compatible)

---

## 💡 Example Business Questions

This dataset supports complex analytical queries:

1. **Revenue & Risk Analysis**
   - Which sellers generate high revenue but also high returns?
   
2. **Return Pattern Analysis**
   - Why are footwear returns higher during sale periods?
   
3. **Logistics Performance**
   - Which warehouses cause the most delivery delays?
   
4. **Payment Risk**
   - Are COD customers riskier than prepaid customers?
   
5. **Inventory Health**
   - How much inventory is stuck due to returns?

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL (Supabase account)
- pip packages: `psycopg2-binary`, `faker`, `python-dotenv`

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/enterprise-decision-copilot.git
   cd enterprise-decision-copilot
📁 Project Structure
text

enterprise-decision-copilot/
│
├── dataset/
│   ├── schema.sql                 # PostgreSQL schema for all 13 tables
│   ├── populate_supabase.py       # Python script to generate & insert data
│   ├── data_rules.md              # Business logic & assumptions
│   └── sample_queries.sql         # Example business queries
│
├── config/
│   └── .env.example               # Environment variables template
│
├── docs/
│   ├── stage1_overview.md         # Stage-1 detailed documentation
│   └── er_diagram.png             # Entity-Relationship diagram
│
├── requirements.txt               # Python dependencies
└── README.md                      # This file

🛠️ Tech Stack
Component	Technology
Database	PostgreSQL (Supabase)
Data Generation	Python, Faker
Future Backend	Python/Node.js
Future Frontend	React/Next.js
Deployment	Vercel + Supabase

📈 Why This Project Matters
This project demonstrates:
✅ Enterprise data modeling skills
✅ Understanding of real business processes
✅ Ability to balance simplicity and scalability
✅ Thoughtful application of AI (not hype-driven)
✅ End-to-end system thinking

📜 License
MIT License - feel free to use for learning and projects.

👤 Author
Built as a portfolio project demonstrating enterprise data engineering and AI integration skills.

🔗 Links
Supabase
Project Documentation
