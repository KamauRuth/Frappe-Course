# Shop API Demo (Bruno)

This Bruno collection includes:

- GET list of shops with all fields
- POST create a new shop
- Token authentication using Frappe API key and secret

## Setup

1. Open Bruno.
2. Open the folder `bruno/shop-api-demo` as a collection.
3. Select environment `local` and update:
   - `API_KEY`
   - `API_SECRET`
4. Run the requests in order.

## Auth Header Used

`Authorization: token {{API_KEY}}:{{API_SECRET}}`
