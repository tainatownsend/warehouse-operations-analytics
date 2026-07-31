# Data Inventory

## Purpose

This document inventories the data assets available for the Warehouse Operations Analytics project.

The objective is to understand the available information before performing exploratory analysis, writing SQL queries, or developing visualizations.

---

# Dataset Summary

**Dataset**

Logistics Operations Database

**Source**

Kaggle

**Publisher**

Yogape

**Type**

Synthetic relational logistics database

---

# Available Tables

| Table | Primary Role | Classification |
|---|---|---|
| customers | Customer information | Dimension |
| drivers | Driver information | Dimension |
| trucks | Fleet assets | Dimension |
| trailers | Trailer assets | Dimension |
| facilities | Warehouses and terminals | Dimension |
| routes | Transportation lanes | Dimension |
| loads | Shipments | Business Fact |
| trips | Transportation execution | Business Fact |
| delivery_events | Pickup and delivery events | Event Fact |
| fuel_purchases | Fuel transactions | Operational Fact |
| maintenance_records | Vehicle maintenance | Operational Fact |
| safety_incidents | Safety events | Operational Fact |
| driver_monthly_metrics | Driver summaries | Aggregated |
| truck_utilization_metrics | Fleet summaries | Aggregated |

---

# Operational Flow

The logistics process represented by this dataset appears to follow the sequence:

Customer

↓

Load

↓

Trip

↓

Delivery Event

Operational entities such as drivers, trucks, trailers, routes, and facilities support this workflow.

Fuel purchases, maintenance records, and safety incidents enrich the operational history.

---

# Analytical Domains

## Operations

- Loads
- Trips
- Delivery Events

## Resources

- Drivers
- Trucks
- Trailers
- Facilities

## Commercial

- Customers
- Routes

## Cost

- Fuel Purchases
- Maintenance Records

## Risk

- Safety Incidents

## Executive Reporting

- Driver Monthly Metrics
- Truck Utilization Metrics

---

# Initial Observations

- The dataset is relational.
- Business entities are separated from operational events.
- Aggregated reporting tables are already available.
- Operational performance can be analyzed from multiple perspectives.
- The project supports SQL, Python, and business analytics workflows.

---

# Known Limitations

- The dataset is synthetic.
- Business conclusions should be interpreted as analytical demonstrations.
- Column definitions still require inspection.
- Relationships will be validated during data exploration.

---

# Next Steps

The next stage will:

1. Inspect every table.
2. Identify columns and data types.
3. Validate primary and foreign keys.
4. Build the initial Entity Relationship Diagram (ERD).
5. Produce the first SQL exploration queries.