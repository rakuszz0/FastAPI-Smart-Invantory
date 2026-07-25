# Smart Inventory API

Smart Inventory API is a backend system designed to manage inventory, customers, suppliers, transactions, and payment processing. The application is built with FastAPI to ensure ease of use, rapid development, and seamless integration with third-party services like Midtrans.

## Project Overview
Smart Inventory API is designed to help operational and business teams manage inventory, customer, supplier, transaction, and payment processes in a centralized manner. This system provides a secure backend interface that is scalable and ready for daily operational use as well as integration with external payment services.

## Key Features
- Manage products, suppliers, customers, and transactions
- Authentication system for login, registration, and token refresh
- Simple AI endpoints for forecasting, recommendations, and anomaly detection
- Security middleware, logging, CORS, rate limiting, and security headers
- Payment integration with Midtrans and DOKU framework
- Payment webhooks to process transaction status automatically

## Initial Setup
Follow these steps to run the application in your local environment.

1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

2. Install all dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
uvicorn app.main:app --reload
```

4. Run tests

```bash
python -m pytest -q
```

5. Open API documentation

After the server is running, open:

```text
http://localhost:8000/docs
```

This interactive documentation makes it easy to view all available endpoints.

## API Structure
All main endpoints use the prefix:

```text
/api/v1
```

Some important endpoints:
- `/products` for managing products
- `/suppliers` for managing suppliers
- `/customers` for managing customers
- `/transactions` for managing transactions
- `/auth` for registration, login, and token refresh
- `/ai/*` for demo AI features
- `/payments/*` for payment flow
- `/admin/payments/*` for payment operations by admin

## User Roles
This application supports role-based access control. Common roles are:
- `admin` for administrative operations
- `staff` for operational data management
- `user` for regular users

If you want to expand the permission system, these roles can be used to restrict access to certain endpoints so only users with specific rights can access them.

## Midtrans Payment Guide
The application is equipped with a basic payment flow ready to test on Midtrans sandbox.

### Environment Configuration
Add the following variables to your `.env` file:

```bash
MIDTRANS_SERVER_KEY="SB-Mid-server-3JWScOa4pa0QJjHG4vAEzCmh"
MIDTRANS_CLIENT_KEY="SB-Mid-client-cSoG5C-yKiBSkgTj"
MIDTRANS_ENVIRONMENT="sandbox"
EMAIL_SYSTEM="jiwagila023@gmail.com"
PAYMENT_WEBHOOK_SECRET="change-me-in-production"
```

### Payment Flow
1. Create a transaction first via the transaction endpoint.
2. Call the payment endpoint to start the payment process.
3. Midtrans will send a webhook notification when payment status changes.
4. The system will automatically update transaction and payment status.

### Payment Endpoints

#### 1. Initiate Payment
This endpoint is used to create a new payment record for an existing transaction.

```bash
curl -X POST http://localhost:8000/api/v1/payments/initiate \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id": 1, "provider": "midtrans"}'
```

The purpose of this endpoint is to initialize payment based on a specific transaction and send data to the selected payment provider.

#### 2. Receive Midtrans Webhook
This endpoint receives notifications from the payment provider. When a webhook arrives, the system will validate the signature, read the payment status, and update the transaction status accordingly.

Example webhook payload for successful payment:

```bash
curl -X POST http://localhost:8000/api/v1/payments/webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <sha256-hmac-of-raw-body>' \
  -d '{
    "transaction_time": "2026-07-26 10:00:00",
    "transaction_status": "settlement",
    "transaction_id": "midtrans-sandbox-001",
    "order_id": "txn-1",
    "gross_amount": "10000.00",
    "currency": "IDR",
    "fraud_status": "accept",
    "payment_type": "bank_transfer",
    "status_code": "200",
    "status_message": "midtrans payment notification"
  }'
```

Example webhook payload for failed payment:

```bash
curl -X POST http://localhost:8000/api/v1/payments/webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <sha256-hmac-of-raw-body>' \
  -d '{
    "transaction_time": "2026-07-26 10:05:00",
    "transaction_status": "deny",
    "transaction_id": "midtrans-sandbox-002",
    "order_id": "txn-2",
    "gross_amount": "10000.00",
    "currency": "IDR",
    "fraud_status": "accept",
    "payment_type": "bank_transfer",
    "status_code": "201",
    "status_message": "transaction is denied"
  }'
```

Example webhook payload for expired payment:

```bash
curl -X POST http://localhost:8000/api/v1/payments/webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <sha256-hmac-of-raw-body>' \
  -d '{
    "transaction_time": "2026-07-26 10:10:00",
    "transaction_status": "expire",
    "transaction_id": "midtrans-sandbox-003",
    "order_id": "txn-3",
    "gross_amount": "10000.00",
    "currency": "IDR",
    "fraud_status": "accept",
    "payment_type": "bank_transfer",
    "status_code": "202",
    "status_message": "transaction expired"
  }'
```

Common status mappings by the system:
- `settlement` or `capture` → internal status `paid`
- `deny`, `cancel`, `failure`, `expire`, `expired` → internal status `failed`

Example successful response from Midtrans:

```json
{
  "status_code": "201",
  "status_message": "Transaction processed successfully",
  "transaction_id": "midtrans-sandbox-001",
  "order_id": "txn-1",
  "gross_amount": "10000.00",
  "currency": "IDR",
  "transaction_status": "settlement",
  "payment_type": "bank_transfer",
  "fraud_status": "accept"
}
```

#### 3. View Payment List (Admin)
This endpoint is used by admin to view all payment records ever created.

```bash
curl -X GET http://localhost:8000/api/v1/admin/payments/ \
  -H 'Authorization: Bearer <admin-token>'
```

#### 4. Retry Payment (Admin)
This endpoint is used when admin wants to resend the payment process for the same record.

```bash
curl -X POST http://localhost:8000/api/v1/admin/payments/1/retry \
  -H 'Authorization: Bearer <admin-token>'
```

#### 5. Refund Payment (Admin)
This endpoint is used to mark a payment as refunded.

Request body:

```json
{}
```

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/admin/payments/1/refund \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <admin-token>' \
  -d '{}'
```

Example JSON response:

```json
{
  "success": true,
  "payment_id": 1,
  "status": "refunded"
}
```

#### 6. Cancel Payment (Admin)
This endpoint is used to mark a payment as canceled.

Request body:

```json
{}
```

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/admin/payments/1/cancel \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <admin-token>' \
  -d '{}'
```

Example JSON response:

```json
{
  "success": true,
  "payment_id": 1,
  "status": "canceled"
}
```

## Important Notes
- For production environment, use a secret manager and more specific signature verification according to the payment provider.
- Webhooks should be processed idempotently to prevent duplicate processing.
- When a webhook shows `paid` status, the transaction will automatically move to `completed` status.

## How to Test with Postman
This section is designed to help non-technical teams easily test the payment flow.

### 1. Run Local Application
Make sure the server is running first:

```bash
uvicorn app.main:app --reload
```

### 2. Open Postman
Create a new request with the appropriate method.

### 3. Test Payment Endpoints
#### A. Create Payment
- Method: `POST`
- URL: `http://localhost:8000/api/v1/payments/initiate`
- Body: raw JSON

```json
{
  "transaction_id": 1,
  "provider": "midtrans"
}
```

#### B. Test Successful Webhook
- Method: `POST`
- URL: `http://localhost:8000/api/v1/payments/webhook`
- Header: `Content-Type: application/json`
- Header: `X-Signature: <sha256-hmac-signature-of-body>`
- Body: raw JSON

```json
{
  "transaction_time": "2026-07-26 10:00:00",
  "transaction_status": "settlement",
  "transaction_id": "midtrans-sandbox-001",
  "order_id": "txn-1",
  "gross_amount": "10000.00",
  "currency": "IDR",
  "fraud_status": "accept",
  "payment_type": "bank_transfer",
  "status_code": "200",
  "status_message": "midtrans payment notification"
}
```

#### C. Test Failed Webhook
Use the same body, but change `transaction_status` to `deny`.

#### D. Test Expired Webhook
Use the same body, but change `transaction_status` to `expire`.

### 4. Test Admin Endpoints
To view payment list or perform refund/cancel operations, use admin token in the Authorization header.

```text
Authorization: Bearer <admin-token>
```

Example endpoints:
- `GET http://localhost:8000/api/v1/admin/payments/`
- `POST http://localhost:8000/api/v1/admin/payments/1/refund`
- `POST http://localhost:8000/api/v1/admin/payments/1/cancel`

### 5. Check Results
After sending a request, ensure:
- Payment status changes according to webhook
- Transaction changes to `completed` when payment is successful
- Transaction changes to `failed` or `expired` when webhook shows that condition

## Admin Response Examples
The following admin endpoint returns concise data about processed payments:

```json
[
  {
    "id": 1,
    "transaction_id": 7,
    "amount": 10000.0,
    "status": "paid",
    "provider": "midtrans",
    "provider_payment_id": "midtrans-sandbox-001"
  }
]
```

This endpoint can be used for internal monitoring, audit purposes, and payment status tracking by operational teams or stakeholders.

## Formal Version for Stakeholders and Clients
This project is developed as a backend solution that supports structured inventory and transaction management, with focus on security, scalability, and ease of integration. The payment features currently available are designed to support a safe and transparent transaction flow, including webhook processing, payment status monitoring, and administrative actions such as refunds and cancellations.

The main purpose of this implementation is to provide a foundation system ready for real business processes, with adequate documentation so that internal teams and external partners can quickly understand the workflow.

## Testing
Tests for payment flow, webhooks, and admin access are available in the `tests` folder.
