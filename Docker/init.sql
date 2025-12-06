cat > init.sql << 'EOF'
-- This file will be executed when the database is initialized
ALTER ROLE admin
SET
    client_encoding TO 'utf8';

ALTER ROLE admin
SET
    default_transaction_isolation TO 'read committed';

ALTER ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO admin;

EOF