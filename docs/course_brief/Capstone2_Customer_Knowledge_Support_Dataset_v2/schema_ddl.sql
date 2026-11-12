-- Capstone 2: Enterprise Customer Support AI Assistant
-- Portable core DDL for PostgreSQL 13+ and MySQL 8+

CREATE TABLE products (
  product_sku VARCHAR(20) PRIMARY KEY,
  product_name VARCHAR(100) NOT NULL,
  plan_tier VARCHAR(50) NOT NULL,
  monthly_list_price DECIMAL(10,2) NOT NULL,
  currency_code VARCHAR(3) NOT NULL,
  product_status VARCHAR(20) NOT NULL
);

CREATE TABLE customers (
  customer_id VARCHAR(20) PRIMARY KEY,
  customer_name VARCHAR(120) NOT NULL,
  email_address VARCHAR(180) NOT NULL,
  customer_segment VARCHAR(40) NOT NULL,
  region VARCHAR(40) NOT NULL,
  pii_classification VARCHAR(30) NOT NULL,
  vip_flag CHAR(1) NOT NULL
);

CREATE TABLE accounts (
  account_id VARCHAR(20) PRIMARY KEY,
  customer_id VARCHAR(20) NOT NULL,
  product_sku VARCHAR(20) NOT NULL,
  account_status VARCHAR(30) NOT NULL,
  start_date DATE NOT NULL,
  renewal_date DATE NOT NULL,
  licensed_seats INTEGER NOT NULL,
  auto_renew_flag CHAR(1) NOT NULL,
  monthly_price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_sku) REFERENCES products(product_sku)
);

CREATE TABLE entitlements (
  account_id VARCHAR(20) PRIMARY KEY,
  support_sla VARCHAR(40) NOT NULL,
  refund_policy_type VARCHAR(50) NOT NULL,
  admin_support_flag CHAR(1) NOT NULL,
  support_region VARCHAR(50) NOT NULL,
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE support_agents (
  agent_id VARCHAR(20) PRIMARY KEY,
  agent_name VARCHAR(120) NOT NULL,
  support_role VARCHAR(60) NOT NULL,
  support_region VARCHAR(50) NOT NULL
);

CREATE TABLE support_tickets (
  ticket_id VARCHAR(20) PRIMARY KEY,
  customer_id VARCHAR(20) NOT NULL,
  account_id VARCHAR(20) NOT NULL,
  intent_category VARCHAR(60) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  channel VARCHAR(20) NOT NULL,
  opened_at TIMESTAMP NOT NULL,
  ticket_status VARCHAR(30) NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  resolution_summary TEXT,
  sentiment VARCHAR(20),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE ticket_events (
  event_id VARCHAR(20) PRIMARY KEY,
  ticket_id VARCHAR(20) NOT NULL,
  event_at TIMESTAMP NOT NULL,
  event_type VARCHAR(50) NOT NULL,
  agent_id VARCHAR(20) NOT NULL,
  event_note TEXT NOT NULL,
  FOREIGN KEY (ticket_id) REFERENCES support_tickets(ticket_id),
  FOREIGN KEY (agent_id) REFERENCES support_agents(agent_id)
);
