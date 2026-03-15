# 🚀 START SERVER - SIMPLE INSTRUCTIONS

## Problem: Link not showing up?
You need to activate the virtual environment first!

---

## ✅ EASY METHOD - Copy These 3 Commands

Open your terminal and run these **one by one**:

```bash
cd /Users/saniyakapure/Desktop/graphql-exm
```

```bash
source venv/bin/activate
```

```bash
python main.py
```

---

## 📺 What You Should See

After running `python main.py`, you'll see:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**The link is:** http://localhost:8000/graphql

---

## 🎯 Step-by-Step with Screenshots

### Step 1: Open Terminal
- Open a **NEW** terminal window
- Don't use the existing one

### Step 2: Navigate to Project
```bash
cd /Users/saniyakapure/Desktop/graphql-exm
```

You should see:
```
saniyakapure@Saniyas-MacBook-Air-2 graphql-exm %
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` appear:
```
(venv) saniyakapure@Saniyas-MacBook-Air-2 graphql-exm %
```
↑ Notice the `(venv)` at the start!

### Step 4: Check Python (Optional - to verify)
```bash
which python
```

Should show:
```
/Users/saniyakapure/Desktop/graphql-exm/venv/bin/python
```
↑ This confirms you're using venv Python, not system Python!

### Step 5: Start Server
```bash
python main.py
```

You'll see:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🌐 Open the Link

Once server is running, open your browser and go to:

**http://localhost:8000/graphql**

or

**http://127.0.0.1:8000/graphql**

You should see the **GraphiQL Playground** with:
- Left side: Query editor
- Right side: Results
- Top: "Docs" and "Schema" buttons

---

## ❌ Troubleshooting

### Problem 1: "command not found: python"
**Solution:** Make sure venv is activated (you should see `(venv)` before your prompt)

### Problem 2: "AssertionError" or "SQLAlchemy error"
**Solution:** You're using system Python, not venv Python. Activate venv first!

### Problem 3: "Address already in use"
**Solution:** Port 8000 is busy. Kill existing server:
```bash
lsof -ti:8000 | xargs kill -9
```
Then try again.

### Problem 4: No output after running python main.py
**Solution:** Wait 2-3 seconds. If nothing appears, press Enter once.

---

## 🛑 How to Stop the Server

Press: **Ctrl + C** (hold Control and press C)

You'll see:
```
^C
INFO:     Shutting down
```

Then deactivate venv:
```bash
deactivate
```

---

## 🎬 Even Simpler - Use the Script!

We have a startup script that does everything:

```bash
./start.sh
```

If you see "permission denied":
```bash
chmod +x start.sh
./start.sh
```

---

## ✨ Once Server is Running

- ✅ Open http://localhost:8000/graphql in browser
- ✅ Open COMPLETE_TEST_CASES.md
- ✅ Copy first test mutation
- ✅ Paste in GraphiQL playground (left side)
- ✅ Click the ▶ Play button
- ✅ See results on right side!

---

## 📋 Quick Checklist

Before starting server, verify:
- [ ] You're in project directory (`cd /Users/saniyakapure/Desktop/graphql-exm`)
- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] Running `which python` shows venv path
- [ ] No other server running on port 8000

---

**Start fresh with a NEW terminal window if things aren't working!** 🎯
