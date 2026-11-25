#!/usr/bin/env bash
# Load the course CSV data into the database. Safe to re-run: it empties the tables first.
set -euo pipefail

source .env

DATA_DIR="docs/course_brief/Capstone2_Customer_Knowledge_Support_Dataset_v2/data"
PSQL="docker exec -i capstone2-db psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1"

echo "Emptying tables..."
$PSQL -c "TRUNCATE ticket_events, support_tickets, support_agents, entitlements, accounts, customers, products, document_registry;"

for table in products customers accounts entitlements support_agents support_tickets ticket_events document_registry; do
  echo "Loading $table..."
  $PSQL -c "\copy $table FROM pstdin WITH (FORMAT csv, HEADER true)" < "$DATA_DIR/$table.csv"
done

echo "Done."
