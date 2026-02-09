# Sailing Capacity API

A high-performance **FastAPI** service designed to calculate **total weekly shipping capacity (TEU)** over a given time range.

The API applies **"latest departure" logic**, meaning that for any given sailing, **only the most recent schedule version is considered**. This ensures accurate, up-to-date capacity calculations at scale.

---

## Getting Started

### 1. Build and Run the Application

The service and its PostgreSQL database are fully containerized. Use **Docker Compose** to start everything:

```bash
docker-compose up --build
```

Once running:

* **API Base URL:** [http://localhost:8000](http://localhost:8000)
* **Swagger UI (Interactive Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 2. Seed the Database

Populate the database with initial sailing data:

```bash
docker exec -it xeneta_api_container python scripts/populate_db.py
```


---

### 3. Run Tests

Execute the full test suite inside the API container:

```bash
docker exec -it xeneta_api_container pytest
```

All tests should pass, confirming the API, database, and business logic are correctly configured.

---

##  API Usage

### Fetch Weekly Capacity

Returns the **total offered capacity (TEU) per week** for all sailings within a specified date range.

**Endpoint**

```
GET /capacity
```

**Query Parameters**

| Parameter | Type   | Description             |
| --------- | ------ | ----------------------- |
| date_from | string | Start date (YYYY-MM-DD) |
| date_to   | string | End date (YYYY-MM-DD)   |

---

### Example Request

```bash
curl "http://localhost:8000/capacity?date_from=2024-01-01&date_to=2024-01-31"
```

### Example Response

```json
[
  {
    "week_start_date": "2024-01-01",
    "week_no": 1,
    "offered_capacity_teu": 25000
  },
  {
    "week_start_date": "2024-01-08",
    "week_no": 2,
    "offered_capacity_teu": 28500
  }
]
```

Each entry represents the total capacity offered by all valid sailings for that calendar week.

---

##  Business Logic

### Latest Departure Logic

* Multiple schedule versions may exist for the same sailing.
* For each sailing, **only the most recent departure (latest schedule version)** is considered.
* This filtering is performed directly in PostgreSQL using `DISTINCT ON`, ensuring high performance even on large datasets.

---

### Weekly Aggregation Semantics (Important)

* Capacity is aggregated **per ISO 8601 calendar week**:

  * Weeks start on **Monday**

* The API aggregates capacity **only for departures that fall within the requested date range** (`date_from` → `date_to`).

    **This means weeks at the beginning or end of the range may be *partial weeks*.**

For example:

* If `date_to` falls on a Wednesday,
* the last returned week will include capacity from **Monday to Wednesday only**,
* not the full Monday–Sunday week.


---

## Tech Stack & Optimization

### Core Stack

* **FastAPI** – Async, high-performance Python web framework
* **PostgreSQL** – Reliable relational database with advanced querying
* **Docker & Docker Compose** – Consistent local development and deployment

---

### Performance Optimizations

* **Composite Indexing**
  Accelerates lookups on date ranges and sailing identifiers.

* **Database-first filtering**
  Heavy data reduction happens in PostgreSQL, keeping the API layer fast and memory-efficient.

