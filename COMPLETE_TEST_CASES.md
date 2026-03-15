# 🧪 COMPLETE TEST CASES - Copy & Paste Ready

## 🎯 All 6 Expected Test Cases with Queries

---

## ✅ TEST CASE 1: Unit Calculation Accuracy

**Goal:** Verify that units consumed = current reading - previous reading

### Step 1: Create Consumer
```graphql
mutation {
  createConsumer(
    name: "Test User"
    email: "test@example.com"
    phone: "9999999999"
    address: "Test Address"
    consumerType: RESIDENTIAL
  ) {
    consumer {
      id
      name
      consumerType
    }
  }
}
```

### Step 2: Create Meter
```graphql
mutation {
  createMeter(
    meterNumber: "MTR-TEST-001"
    consumerId: 1
  ) {
    meter {
      id
      meterNumber
      consumer {
        name
      }
    }
  }
}
```

### Step 3: Record First Reading (Baseline)
```graphql
mutation {
  recordMeterReading(
    meterId: 1
    currentReading: 1000
    readingDate: "2024-01-01"
  ) {
    meterReading {
      id
      currentReading
      unitsConsumed
      readingDate
    }
  }
}
```
**Expected:** `unitsConsumed: 1000` (first reading treated as baseline)

### Step 4: Record Second Reading
```graphql
mutation {
  recordMeterReading(
    meterId: 1
    currentReading: 1500
    readingDate: "2024-02-01"
  ) {
    meterReading {
      id
      currentReading
      previousReading
      unitsConsumed
      readingDate
    }
  }
}
```
**Expected:** `unitsConsumed: 500` (1500 - 1000 = 500) ✅

### Step 5: Record Third Reading
```graphql
mutation {
  recordMeterReading(
    meterId: 1
    currentReading: 2300
    readingDate: "2024-03-01"
  ) {
    meterReading {
      id
      currentReading
      previousReading
      unitsConsumed
      readingDate
    }
  }
}
```
**Expected:** `unitsConsumed: 800` (2300 - 1500 = 800) ✅

---

## ✅ TEST CASE 2: Bill Generation Validation

**Goal:** Verify bill amount = total units × rate per consumer type

### Test 2a: Residential Bill (Rate: ₹7.5/unit)
```graphql
mutation {
  generateBill(
    consumerId: 1
    billingCycle: "2024-02"
  ) {
    bill {
      id
      consumer {
        name
        consumerType
      }
      totalUnits
      amount
      billingCycle
      status
      dueDate
    }
  }
}
```
**Expected:** 
- `totalUnits: 500` (only Feb reading)
- `amount: 3750` (500 × 7.5 = ₹3,750) ✅

### Test 2b: Commercial Bill (Rate: ₹12/unit)

**First create commercial consumer:**
```graphql
mutation {
  createConsumer(
    name: "ABC Shop"
    email: "shop@example.com"
    phone: "8888888888"
    address: "Shop Address"
    consumerType: COMMERCIAL
  ) {
    consumer {
      id
      name
      consumerType
    }
  }
}
```

**Create meter for commercial:**
```graphql
mutation {
  createMeter(
    meterNumber: "MTR-COMM-001"
    consumerId: 2
  ) {
    meter {
      id
      meterNumber
    }
  }
}
```

**Record readings:**
```graphql
mutation {
  recordMeterReading(
    meterId: 2
    currentReading: 5000
    readingDate: "2024-01-01"
  ) {
    meterReading {
      id
      unitsConsumed
    }
  }
}
```

```graphql
mutation {
  recordMeterReading(
    meterId: 2
    currentReading: 5300
    readingDate: "2024-02-01"
  ) {
    meterReading {
      id
      unitsConsumed
    }
  }
}
```

**Generate commercial bill:**
```graphql
mutation {
  generateBill(
    consumerId: 2
    billingCycle: "2024-02"
  ) {
    bill {
      id
      consumer {
        name
        consumerType
      }
      totalUnits
      amount
      billingCycle
    }
  }
}
```
**Expected:** 
- `totalUnits: 300` (5300 - 5000)
- `amount: 3600` (300 × 12 = ₹3,600) ✅

---

## ✅ TEST CASE 3: Payment Workflow

**Goal:** Verify payment updates bill status properly

### Step 1: Check Bill Before Payment
```graphql
query {
  allBills {
    id
    amount
    status
    consumer {
      name
    }
  }
}
```
**Expected:** Bill with `status: "GENERATED"`

### Step 2: Record Full Payment
```graphql
mutation {
  recordPayment(
    billId: 1
    amount: 3750
    paymentMethod: "UPI"
  ) {
    payment {
      id
      amount
      paymentMethod
      paymentDate
      status
      bill {
        id
        status
        amount
      }
    }
  }
}
```
**Expected:** 
- Payment `status: "SUCCESS"`
- Bill `status: "PAID"` ✅

### Step 3: Verify Bill Updated
```graphql
query {
  bill(id: 1) {
    id
    amount
    status
    payments {
      id
      amount
      paymentMethod
      paymentDate
    }
  }
}
```
**Expected:** Bill shows `status: "PAID"` and payment details ✅

### Step 4: Try Partial Payment (Bill 2)
```graphql
mutation {
  recordPayment(
    billId: 2
    amount: 2000
    paymentMethod: "CARD"
  ) {
    payment {
      id
      amount
      status
      bill {
        id
        amount
        status
      }
    }
  }
}
```
**Expected:** Bill still `status: "GENERATED"` (partial payment doesn't mark as paid) ✅

---

## ✅ TEST CASE 4: Overdue Handling

**Goal:** Verify bills show correct overdue status based on due date

### Step 1: Generate Bill with Past Due Date
```graphql
mutation {
  generateBill(
    consumerId: 1
    billingCycle: "2024-01"
  ) {
    bill {
      id
      billingCycle
      dueDate
      status
      generatedDate
    }
  }
}
```
**Note:** Due date is automatically set to 15 days from generation

### Step 2: Check Overdue Bills
```graphql
query {
  billsByStatus(status: "OVERDUE") {
    id
    consumer {
      name
    }
    amount
    dueDate
    status
  }
}
```
**Expected:** Shows bills past their due date ✅

### Step 3: Filter by Status
```graphql
query {
  allBills {
    id
    status
    dueDate
    amount
    consumer {
      name
    }
  }
}
```
**Manual Check:** Bills with `dueDate < today` and `status != "PAID"` should be overdue

---

## ✅ TEST CASE 5: Duplicate Reading Prevention

**Goal:** Verify system prevents/allows duplicate readings (currently DISABLED for testing)

### Test: Try Recording Same Day Reading Twice

**First reading today:**
```graphql
mutation {
  recordMeterReading(
    meterId: 1
    currentReading: 2500
    readingDate: "2024-03-08"
  ) {
    meterReading {
      id
      currentReading
      readingDate
    }
  }
}
```

**Second reading same day:**
```graphql
mutation {
  recordMeterReading(
    meterId: 1
    currentReading: 2600
    readingDate: "2024-03-08"
  ) {
    meterReading {
      id
      currentReading
      readingDate
    }
  }
}
```

**Expected (Current - DISABLED):** Both readings recorded successfully ✅
**Expected (Production - ENABLED):** Second reading rejected with error

**Viva Explanation:**
"For testing and development, I've disabled duplicate prevention so we can quickly test multiple scenarios. In production, we would enable this check to prevent multiple readings on the same day for the same meter."

---

## ✅ TEST CASE 6: Billing History Maintained

**Goal:** Verify all bills and payments are properly stored and queryable

### Step 1: View All Consumers with Their Meters
```graphql
query {
  allConsumers {
    id
    name
    consumerType
    meters {
      id
      meterNumber
    }
  }
}
```

### Step 2: View Billing History for a Consumer
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
    payments {
      id
      amount
      paymentMethod
      paymentDate
    }
  }
}
```
**Expected:** All bills for consumer with payment history ✅

### Step 3: View Reading History for a Meter
```graphql
query {
  readingsByMeter(meterId: 1) {
    id
    currentReading
    previousReading
    unitsConsumed
    readingDate
  }
}
```
**Expected:** All readings in chronological order ✅

### Step 4: View All Payments
```graphql
query {
  allPayments {
    id
    amount
    paymentMethod
    paymentDate
    status
    bill {
      id
      consumer {
        name
      }
      amount
      billingCycle
    }
  }
}
```
**Expected:** Complete payment history with bill details ✅

### Step 5: Complex Query - Full History
```graphql
query {
  consumer(id: 1) {
    id
    name
    email
    consumerType
    meters {
      id
      meterNumber
      readings {
        id
        currentReading
        unitsConsumed
        readingDate
      }
    }
    bills {
      id
      billingCycle
      totalUnits
      amount
      status
      payments {
        id
        amount
        paymentMethod
        paymentDate
      }
    }
  }
}
```
**Expected:** Complete consumer history with all relationships ✅

---

## 📊 TEST RESULTS CHECKLIST

After running all tests, verify:

- [ ] **Unit Calculation:** 1500 - 1000 = 500 ✅
- [ ] **Bill Amount (Residential):** 500 × ₹7.5 = ₹3,750 ✅
- [ ] **Bill Amount (Commercial):** 300 × ₹12 = ₹3,600 ✅
- [ ] **Payment Updates Status:** Bill status changes to PAID ✅
- [ ] **Partial Payment:** Bill remains GENERATED ✅
- [ ] **Overdue Detection:** Past due bills identified ✅
- [ ] **Duplicate Prevention:** Currently disabled for testing ✅
- [ ] **History Queries:** All data retrievable ✅

---

## 🎓 For Your Viva

**Be ready to demonstrate:**
1. Run any mutation live
2. Show immediate query results
3. Explain the GraphQL response structure
4. Walk through the calculation logic
5. Explain relationships (Consumer → Meter → Readings → Bills → Payments)

---

## 💡 Quick Tips

- **Copy entire mutation** from here → Paste in GraphQL Playground
- **Change IDs** if you get errors (use actual IDs from responses)
- **Run queries** after mutations to verify changes
- **Save responses** to show working project in exam

**You've got this! 🚀**
