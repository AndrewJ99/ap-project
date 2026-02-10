# How the backend is structured
 
 [WIP]

# How I modeled the data 
- key, merchantid, amount, cardBrand, status, declineReasonCode, transactionDate (Iso)
- 2 options CSV / JSON 

example: 
{
        "id": "001",
        "amount": 100.00,
        "merchantId": "b312436e-e477-49d4-be7f-9d027f9b9e34",
        "cardBrand": "Visa",
        "status": "approved",
        "declinedReason": "01",
        "created_at": "2023-10-01T12:00:00Z",
        "updated_at": "2023-10-01T12:00:00Z"
}

Data Type
ID - string
Amount - int
merchantId - string (15 characeter)  
cardBrand - string 
    only viable options are: Visa, Mastercard, Amex, Discover
status - string
declinedReason - string
    "01" 
    "02"
    "03"

createdat: string (Time ISO Format)


# How I approached filtering and aggregation 

Filtering - 
I would filter by status key, declined / success 
Filter by cardBrand (with status key) 

Aggregation - 
I would aggregate by grouping of cardbrand, with success and group by the time 



# Full Architecture 
### Frontend: (Vanilla JS)
index.html 
app.js (fetch data, real-time page update from aggregations/filters) 
styles.css (styling) 

### Backend: (Python)
- Routes: (http handlers) 
  - /api/transactions
  - /api/transactions/mtd-summary
  - /api/transactions/monthly-summary 

- Services: (Business Logic) 
  - Transactions (Filtering) 
  - AggregationServices (Summaries)

- Data Layer: 
  - In memory list 
  - Pandas DataFrame 




# Requirements: 
- 




## Notes: 
Mock transaction data is generated using a standalone utility script located in utils/generator.py. This script is run manually to produce a static transactions.json file, allowing the API to remain deterministic and simplifying testing and debugging

