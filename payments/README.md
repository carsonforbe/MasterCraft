# Payment Gateway API

## Local Development

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## API Endpoints

### Initiate Payment
`POST /api/v1/payments`
Request body:
```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "amount": 50.00
}