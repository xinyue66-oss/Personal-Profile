# **Project Database Setup and Access Guide**

This guide outlines the steps to set up, connect to, and access the `api` database used in this project. Follow these instructions to create and configure the database, verify the setup, and view data in the `app_users` table.

## **Table of Contents**
1. [Database Creation and Initial Setup](#database-creation-and-initial-setup)
2. [Connecting to the Database](#connecting-to-the-database)
3. [Verifying Database Tables](#verifying-database-tables)
4. [Viewing Data in Tables](#viewing-data-in-tables)
5. [Notes and Best Practices](#notes-and-best-practices)


### 1. Database Creation and Initial Setup

#### Step 1: Create the `api` Database

1. Open your terminal.
2. Log in to MariaDB or MySQL with administrative privileges:
   ```bash
   mysql -u root -p
   ```
3. Enter the root password when prompted.
4. Create the `api` database by running:
   ```sql
   CREATE DATABASE api;
   ```

#### Step 2: Create a Database User (Optional but Recommended)

To enhance security, create a dedicated user for this project with restricted privileges:

1. While still in the MySQL command line, create a new user (replace `newuser` and `newpassword` as needed):
   ```sql
   CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'newpassword';
   ```
2. Grant the new user privileges on the `api` database:
   ```sql
   GRANT ALL PRIVILEGES ON api.* TO 'newuser'@'localhost';
   ```
3. Apply the changes:
   ```sql
   FLUSH PRIVILEGES;
   ```

#### Step 3: Configure Django Settings

Update the Django `settings.py` file to connect to the `api` database using environment variables (recommended for security).

1. In your project’s `.env` file (use `.env.example` as a template), add:
   ```env
   DB_NAME=api
   DB_USER=newuser
   DB_PASSWORD=newpassword
   DB_HOST=127.0.0.1
   DB_PORT=3307
   ```
2. Ensure `settings.py` loads these variables and configures the `DATABASES` setting.

#### Step 4: Run Migrations

Once the database is created and Django is configured, run migrations to set up the necessary tables:

```bash
python manage.py migrate
```

---

### 2. Connecting to the Database

After the database setup, you can connect to `api` directly from the command line.

1. Open your terminal.
2. Use the following command to connect (replace `newuser` with the username):
   ```bash
   mysql -h 127.0.0.1 -P 3307 -u newuser -p
   ```
3. When prompted, enter the password for the database user.

---

### 3. Verifying Database Tables

After connecting, select the `api` database and view the tables created by Django migrations.

1. Select the database:
   ```sql
   USE api;
   ```
2. Show all tables to verify they were created correctly:
   ```sql
   SHOW TABLES;
   ```

Expected output includes project-specific tables, such as `app_users`, `app_profiles`, and Django’s built-in tables like `auth_user`.

---

### 4. Viewing Data in Tables

To view data in a specific table, such as `app_users`, use the following query:

```sql
SELECT * FROM app_users;
```

This command will display all rows in the `app_users` table, allowing you to verify the stored user data.

---

### 5. Notes and Best Practices

- **Environment Variables**: Store database credentials and other sensitive information in an `.env` file. Never commit this file to version control. Instead, include a `.env.example` file with placeholder values.
- **Database Permissions**: For security, use a dedicated database user with restricted permissions rather than root access.
- **Backup and Restore**: Regularly back up the `api` database and document the backup and restore procedures for disaster recovery.
- **Django Management**: Use Django’s `migrate` and `makemigrations` commands to manage database schema changes.

By following these steps, you ensure a secure, organized, and professional setup for managing your project’s database.
