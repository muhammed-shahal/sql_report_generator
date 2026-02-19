USE analytics;

-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SESSIONS TABLE
CREATE TABLE sessions (
    id VARCHAR(64) PRIMARY KEY,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- QUERY HISTORY
CREATE TABLE query_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64),
    user_id INT,
    question TEXT,
    sql_query TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EXPORT JOBS (ETL tracking)
CREATE TABLE export_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    query_hash VARCHAR(64),
    sql_query TEXT,
    status VARCHAR(50),
    file_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, query_hash)
);

-- ANALYTICS TABLES
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(255),
    signup_date DATE
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10,2),
    order_date DATE
);
