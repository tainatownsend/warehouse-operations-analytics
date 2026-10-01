# Warehouse Analytics — Public Portfolio Anonymization Contract

Use this contract before turning any internal distribution-centre analysis into a public portfolio artifact.

## Never publish
- Employer/customer order IDs, purchase orders, tracking numbers or facility-identifying operational keys.
- Internal table/schema/server names, credentials, URLs, screenshots, query text copied from corporate systems, or proprietary thresholds.
- Real SKU-level, associate-level, carrier-level or site-level performance when it can reveal confidential operations.

## Public-safe transformation
- Rebuild the problem with synthetic or openly licensed data.
- Rename facilities, tables, fields and business rules.
- Preserve the analytical pattern, not the employer data: entity resolution, cancellation-driver EDA, split-shipment logic, inventory aging, carrier trend analysis, QA locks, etc.
- State clearly that the portfolio dataset is synthetic/open and that results do not represent employer performance.

## Evidence worth preserving privately
For each internal project, retain a private accomplishment note containing: business question, analytical method, tools used, validation method, measurable operational outcome when disclosure is permitted, and the public-safe analogue to build.

## Current candidate portfolio slices
1. Order-cancellation root-cause exploration using synthetic warehouse/order events.
2. Rush-order multi-node lookup using synthetic split shipments.
3. Inventory-aging prioritization with generated stock/location history.
4. Carrier service trend analysis using public/synthetic parcel events.

The public repository should contain only the reconstructed version.
