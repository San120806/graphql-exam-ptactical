# 🔌 Smart Electricity Billing — GraphiQL Test Queries

Run these **in order** at `http://localhost:8000/graphql`

---

## ✅ STEP 1 — Create a Residential Consumer

```graphql
mutation {
  createConsumer(input: {
    name: "Saniya Kapure"
    address: "123 MG Road, Pune"
    connectionType: "RESIDENTIAL"
  }) {
    consumer { id name address connectionType status }
    success
    message
  }
}
```
> 📝 Note the `id` returned (should be `1`). Use it in next steps.

---

## ✅ STEP 2 — Create a Commercial Consumer (for rate comparison)

```graphql
mutation {
  createConsumer(input: {
    name: "ABC Office"
    address: "42 Business Park, Pune"
    connectionType: "COMMERCIAL"
  }) {
    consumer { id name connectionType }
    success
    message
  }
}
```

---

## ✅ STEP 3 — Create a Meter for Consumer 1

```graphql
mutation {
  createMeter(input: {
    consumerId: 1
    meterNumber: "MTR-RES-001"
  }) {
    meter { id meterNumber consumerId status }
    success
    message
  }
}
```
> 📝 Note the meter `id` (should be `1`).

---

## 🧪 TEST CASE 1 — Unit Calculation Accuracy

### Record First Reading (baseline)
```graphql
mutation {
  recordMeterReading(input: {
    meterId: 1
    readingValue: 3000
  }) {
    meterReading { id readingValue readingDate }
    success
    message
    unitsConsumed
  }
}
```
> 📝 First reading — `unitsConsumed` will be `3000` (no previous reading).

> ⚠️ **To record a second reading (next step), you must do it tomorrow OR temporarily comment out the duplicate check.** For testing, stop the server with `Ctrl+C`, delete the DB with `rm electricity_billing.db`, restart, or use the workaround below.

---

## 🧪 TEST CASE 5 — Duplicate Reading Prevention

### Try recording SAME meter again today ← should FAIL
```graphql
mutation {
  recordMeterReading(input: {
    meterId: 1
    readingValue: 3200
  }) {
    success
    message
    unitsConsumed
  }
}
```
> ✅ Expected: `success: false`, message: `"Reading already recorded today. Cannot duplicate."`

---

## ⚠️ WORKAROUND: Reset DB to continue testing

In terminal (server must be stopped first with `Ctrl+C`):
```bash
rm electricity_billing.db
python main.py
```
Then re-run Steps 1→3, then skip to Step 4 below with TWO readings.

---

## 🧪 TEST CASE 1 (continued) — Record Second Reading

After resetting, run Step 3 meter creation again, then:

### First reading
```graphql
mutation {
  recordMeterReading(input: {
    meterId: 1
    readingValue: 3000
  }) {
    success message unitsConsumed
  }
}
```

### (Next day or after reset — second reading)
```graphql
mutation {
  recordMeterReading(input: {
    meterId: 1
    readingValue: 3500
  }) {
    meterReading { id readingValue }
    success
    message
    unitsConsumed
  }
}
```
> ✅ Expected: `unitsConsumed: 500` (3500 - 3000)

---

## 🧪 TEST CASE 2 — Bill Generation Validation

```graphql
mutation {
  generateBill(input: {
    consumerId: 1
    billingCycle: "2025-03"
  }) {
    bill {
      id
      billingCycle
      totalUnits
      amount
      status
      generatedDate
      dueDate
    }
    success
    message
  }
}
```
> ✅ Expected:
> - `totalUnits: 500`
> - `amount: 3750` (500 × ₹7.5 residential rate)
> - `status: GENERATED`

---

## 🧪 TEST CASE 2b — Duplicate Bill Prevention ← should FAIL

```graphql
mutation {
  generateBill(input: {
    consumerId: 1
    billingCycle: "2025-03"
  }) {
    success
    message
  }
}
```
> ✅ Expected: `success: false`, message: `"Bill already generated for cycle 2025-03"`

---

## 🧪 TEST CASE 3 — Payment Workflow

### Pay the bill fully (use bill id from Step above, e.g. `1`)
```graphql
mutation {
  recordPayment(input: {
    billId: 1
    amount: 3750
  }) {
    payment {
      id
      amount
      paymentDate
      status
    }
    success
    message
    remainingAmount
  }
}
```
> ✅ Expected: `success: true`, message: `"Payment recorded. Bill fully paid!"`, `remainingAmount: 0`

### Try paying again (already paid) ← should FAIL
```graphql
mutation {
  recordPayment(input: {
    billId: 1
    amount: 100
  }) {
    success
    message
  }
}
```
> ✅ Expected: `success: false`, message: `"Bill is already paid"`

---

## 🧪 TEST CASE 4 — Overdue Handling

Generate a bill for commercial consumer, then check overdue query:

```graphql
mutation {
  generateBill(input: {
    consumerId: 2
    billingCycle: "2025-01"
  }) {
    bill { id amount status dueDate }
    success message
  }
}
```

Then query overdue bills (bills past due date get marked OVERDUE on next partial payment):
```graphql
query {
  billsByStatus(status: "OVERDUE") {
    id
    consumerId
    billingCycle
    amount
    dueDate
    status
  }
}
```

---

## 🧪 TEST CASE 6 — Billing History Maintained

```graphql
query {
  billsByConsumer(consumerId: 1) {
    id
    billingCycle
    totalUnits
    amount
    status
    generatedDate
    dueDate
  }
}
```

```graphql
query {
  paymentsByBill(billId: 1) {
    id
    amount
    paymentDate
    status
  }
}
```

---

## 📋 Full Data Verification Queries

### See all consumers
```graphql
query {
  allConsumers {
    id name address connectionType status
  }
}
```

### See all meters
```graphql
query {
  allMeters {
    id meterNumber consumerId status
  }
}
```

### See all readings
```graphql
query {
  allMeterReadings {
    id meterId readingValue readingDate
  }
}
```

### See all bills
```graphql
query {
  allBills {
    id consumerId billingCycle totalUnits amount status generatedDate dueDate
  }
}
```

### See all payments
```graphql
query {
  allPayments {
    id billId amount paymentDate status
  }
}
```

---

## 💡 Rate Card (for Viva)
| Connection Type | Rate per Unit |
|---|---|
| RESIDENTIAL | ₹7.5 |
| COMMERCIAL | ₹12.0 |
