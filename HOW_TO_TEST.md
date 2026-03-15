# 🎯 STEP-BY-STEP TESTING GUIDE (How to Get IDs & Test)

## 🚀 Quick Start - See Clickable Links!

**To start server with beautiful output, run in NEW terminal:**
```bash
cd /Users/saniyakapure/Desktop/graphql-exm && source venv/bin/activate && ./server.sh
```

You'll see clickable links! **Cmd+Click** to open GraphQL Playground!

## ✅ Server URL: http://localhost:8000/graphql

---

## 🌐 HOW TO ACCESS THE GRAPHQL INTERFACE

### Option 1: GraphQL Playground (Visual Interface)
**Open in your browser:** http://localhost:8000/graphql

You'll see a nice interface where you can write queries and see results!

### Option 2: Thunder Client / Postman
- **URL:** `http://localhost:8000/graphql`
- **Method:** POST
- **Headers:** `Content-Type: application/json`
- **Body:** Raw JSON

---

## 📝 COMPLETE TESTING WORKFLOW (WITH IDs)

### STEP 1: Create Consumer (Get Consumer ID)

**Thunder Client/Postman Body:**
```json
{
  "query": "mutation { createConsumer(input: { name: \"Rajesh Kumar\" address: \"123 MG Road, Mumbai\" connectionType: \"residential\" }) { consumer { id name address connectionType } success message } }"
}
```

**Expected Response:**
```json
{
  "data": {
    "createConsumer": {
      "consumer": {
        "id": 1,  ← SAVE THIS ID!
        "name": "Rajesh Kumar",
        "address": "123 MG Road, Mumbai",
        "connectionType": "RESIDENTIAL"
      },
      "success": true,
      "message": "Consumer Rajesh Kumar created successfully"
    }
  }
}
```

✅ **Note the ID: 1** (This is your consumerId)

---

### STEP 2: Create Meter (Get Meter ID)

**Use the consumer ID from Step 1:**

```json
{
  "query": "mutation { createMeter(input: { consumerId: 1 meterNumber: \"MTR-2024-001\" }) { meter { id meterNumber consumer { name } } success message } }"
}
```

**Expected Response:**
```json
{
  "data": {
    "createMeter": {
      "meter": {
        "id": 1,  ← SAVE THIS ID!
        "meterNumber": "MTR-2024-001",
        "consumer": {
          "name": "Rajesh Kumar"
        }
      },
      "success": true,
      "message": "Meter created successfully"
    }
  }
}
```

✅ **Note the ID: 1** (This is your meterId)

---

### STEP 3: Record First Reading

**Use the meter ID from Step 2:**

```json
{
  "query": "mutation { recordMeterReading(input: { meterId: 1 readingValue: 1000 }) { meterReading { id readingValue readingDate } success message unitsConsumed } }"
}
```

**Response:**
```json
{
  "data": {
    "recordMeterReading": {
      "meterReading": {
        "id": 1,
        "readingValue": 1000,
        "readingDate": "2024-03-07T10:30:00"
      },
      "success": true,
      "message": "Reading recorded. Units consumed: 1000",
      "unitsConsumed": 1000
    }
  }
}
```

---

### STEP 4: Record Second Reading (Simulate Next Month)

**IMPORTANT:** Comment out duplicate check in `mutations/meter_reading.py` (lines 43-53) OR wait 24 hours

```json
{
  "query": "mutation { recordMeterReading(input: { meterId: 1 readingValue: 1500 }) { meterReading { id readingValue } success message unitsConsumed } }"
}
```

**Response shows:** 500 units consumed (1500 - 1000)

---

### STEP 5: Generate Bill (Get Bill ID)

**Use consumer ID from Step 1:**

```json
{
  "query": "mutation { generateBill(input: { consumerId: 1 billingCycle: \"2024-03\" }) { bill { id billingCycle totalUnits amount status } success message } }"
}
```

**Expected Response:**
```json
{
  "data": {
    "generateBill": {
      "bill": {
        "id": 1,  ← SAVE THIS ID!
        "billingCycle": "2024-03",
        "totalUnits": 500,
        "amount": 3750,
        "status": "GENERATED"
      },
      "success": true,
      "message": "Bill generated: 500 units × ₹7.5 = ₹3750"
    }
  }
}
```

✅ **Note the ID: 1** (This is your billId)

---

### STEP 6: Record Payment

**Use bill ID from Step 5:**

```json
{
  "query": "mutation { recordPayment(input: { billId: 1 amount: 3750 }) { payment { id amount paymentDate status } success message remainingAmount } }"
}
```

**Response:**
```json
{
  "data": {
    "recordPayment": {
      "payment": {
        "id": 1,
        "amount": 3750,
        "paymentDate": "2024-03-07T10:45:00",
        "status": "SUCCESS"
      },
      "success": true,
      "message": "Payment recorded. Bill fully paid!",
      "remainingAmount": 0
    }
  }
}
```

---

## 🔍 QUERY EXAMPLES (Using the IDs you got)

### Query All Consumers
```json
{
  "query": "query { allConsumers { id name address connectionType meters { meterNumber } } }"
}
```

### Query Single Consumer by ID
```json
{
  "query": "query { consumer(id: 1) { id name address meters { meterNumber } } }"
}
```

### Query Bills by Consumer
```json
{
  "query": "query { billsByConsumer(consumerId: 1) { id billingCycle totalUnits amount status } }"
}
```

### Query Readings by Meter
```json
{
  "query": "query { readingsByMeter(meterId: 1) { id readingValue readingDate } }"
}
```

### Query Payments by Bill
```json
{
  "query": "query { paymentsByBill(billId: 1) { id amount paymentDate status } }"
}
```

---

## 🎨 GRAPHQL PLAYGROUND (Better for Testing)

**Open:** http://localhost:8000/graphql

**In the left panel, type:**
```graphql
mutation {
  createConsumer(input: {
    name: "Rajesh Kumar"
    address: "123 MG Road, Mumbai"
    connectionType: "residential"
  }) {
    consumer {
      id
      name
      address
    }
    success
    message
  }
}
```

**Click the Play button (▶) to run!**

---

## 💡 PRO TIPS

1. **Save IDs:** After each mutation, note down the ID returned
2. **Use GraphQL Playground:** Easier than Thunder Client for GraphQL
3. **Multiple consumers:** Create different consumers to test independently
4. **Error testing:** Try duplicate meter numbers, invalid IDs to test validation

---

## 🆘 QUICK TROUBLESHOOTING

### Can't access http://localhost:8000/graphql?
```bash
# Check if server is running
lsof -i :8000

# Restart server
source venv/bin/activate
python main.py
```

### Need to disable duplicate reading check?
Edit `mutations/meter_reading.py`, comment out lines 43-53:
```python
# existing_reading = db_session.query(MeterReading).filter(
#     MeterReading.meter_id == input.meter_id,
#     MeterReading.reading_date >= today_start
# ).first()
# 
# if existing_reading:
#     return RecordMeterReading(...)
```

---

## 📊 TRACKING YOUR IDs

| What | ID | Notes |
|------|-----|-------|
| Consumer | 1 | First consumer created |
| Meter | 1 | First meter for consumer 1 |
| Reading 1 | 1 | First reading: 1000 |
| Reading 2 | 2 | Second reading: 1500 |
| Bill | 1 | For cycle 2024-03 |
| Payment | 1 | Full payment of ₹3750 |

---

**Open http://localhost:8000/graphql now and start testing!** 🚀
