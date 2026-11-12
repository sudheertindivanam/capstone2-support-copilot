CREATE TABLE document_registry (
    document_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    format VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    version VARCHAR(20),
    policy_id VARCHAR(50),
    product_scope VARCHAR(255),
    region_scope VARCHAR(100),
    document_type VARCHAR(100),
    effective_date DATE NULL,
    supersedes_document_id VARCHAR(20) NULL
);
