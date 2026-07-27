# 🚀 RENDER DEPLOYMENT GUIDE

## Complete Step-by-Step Guide to Deploy on Render

---

## ✅ PREREQUISITES (Already Done!)

- ✅ `requirements.txt` created
- ✅ `app.py` updated with PORT support
- ✅ `.gitignore` created
- ✅ Project ready for deployment

---

## 📋 DEPLOYMENT STEPS

### **STEP 1: Create GitHub Repository**

1. **Go to GitHub:** https://github.com
2. **Sign in** (or create account if you don't have one)
3. **Click "New Repository"** (green button, top right)
4. **Fill details:**
   ```
   Repository name: student-performance-prediction
   Description: AI-Powered Student Performance Prediction System
   ✅ Public (select this)
   ❌ Don't initialize with README (we have files already)
   ```
5. **Click "Create repository"**

---

### **STEP 2: Push Code to GitHub**

**Open PowerShell in your project folder and run these commands:**

```powershell
# Step 1: Initialize git (if not already done)
git init

# Step 2: Add all files
git add .

# Step 3: Commit files
git commit -m "Initial commit - Student Performance Prediction ML Project"

# Step 4: Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/student-performance-prediction.git

# Step 5: Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username!

**If asked for credentials:**
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your GitHub password)
  - Get token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token

---

### **STEP 3: Deploy on Render**

1. **Go to Render:** https://render.com
2. **Click "Get Started for Free"** (top right)
3. **Sign Up with GitHub** (easiest way)
4. **Once logged in, click "New +"** (top right)
5. **Select "Web Service"**
6. **Connect GitHub repository:**
   - Find your repository: `student-performance-prediction`
   - Click "Connect"

---

### **STEP 4: Configure Render Settings**

**Fill in these details:**

```
Name: student-performance-prediction
  (or any name you want)

Region: Singapore (or closest to you)

Branch: main

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app
```

**Important Settings:**

```
Instance Type: Free
  ✅ Select "Free" (no credit card needed)

Environment Variables:
  (Leave empty for now, not needed)

Auto-Deploy:
  ✅ Yes (Enable auto-deploy from GitHub)
```

---

### **STEP 5: Deploy!**

1. **Click "Create Web Service"** (bottom of page)
2. **Wait for deployment** (5-10 minutes)
   - You'll see logs in real-time
   - Wait for "Deploy succeeded" message
3. **Your app is LIVE!** 🎉

**You'll get a URL like:**
```
https://student-performance-prediction-xxxx.onrender.com
```

---

## 🌐 ACCESSING YOUR DEPLOYED APP

**Your app will be at:**
```
https://your-app-name.onrender.com
```

**Pages:**
- Home: https://your-app-name.onrender.com/
- Prediction: https://your-app-name.onrender.com/prediction
- About: https://your-app-name.onrender.com/about
- Contact: https://your-app-name.onrender.com/contact

---

## ⚠️ IMPORTANT NOTES

### **Free Tier Limitations:**

1. **Sleep after 15 minutes of inactivity**
   - First request after sleep: 30-60 seconds to wake up
   - Solution: Keep app active or upgrade to paid

2. **750 hours/month free**
   - Enough for demos and testing
   - Resets every month

3. **Automatic restarts**
   - Render may restart your app
   - All data in memory will be lost
   - Model file is safe (stored in repo)

### **Performance:**

- First load: May be slow (waking up from sleep)
- After wake up: Fast and responsive
- Perfect for: Demos, testing, portfolio

---

## 🔄 UPDATING YOUR APP

**To update your deployed app:**

1. **Make changes locally**
2. **Commit and push to GitHub:**
   ```powershell
   git add .
   git commit -m "Updated feature X"
   git push
   ```
3. **Render auto-deploys!** (if auto-deploy enabled)
   - Wait 5-10 minutes
   - Changes will be live

---

## ✅ VERIFICATION CHECKLIST

After deployment, check:

- [ ] Home page loads
- [ ] Navigation works (all 4 pages)
- [ ] Prediction form accepts input
- [ ] Prediction works and shows results
- [ ] About page displays model info
- [ ] Contact page shows your details
- [ ] No emojis except 🎓 logo
- [ ] Professional appearance

---

## 🐛 TROUBLESHOOTING

### **Problem: Build Failed**

**Solution:**
- Check `requirements.txt` format
- Ensure all dependencies are listed
- Check Render logs for specific error

### **Problem: App crashes on startup**

**Solution:**
- Check `app.py` has PORT support: `port = int(os.environ.get("PORT", 5000))`
- Check Render logs for error message
- Ensure `gunicorn` is in requirements.txt

### **Problem: Model not found error**

**Solution:**
- Ensure `student_model.pkl` or `models/student_model.pkl` is in repo
- Check file is not in `.gitignore`
- Push model file to GitHub

### **Problem: Slow first load**

**Solution:**
- This is normal for free tier
- App sleeps after 15 min inactivity
- Upgrade to paid tier for always-on

---

## 💰 COST

**Free Forever (with limitations):**
- 750 hours/month
- Sleep after 15 min inactivity
- Perfect for demos

**Paid Tier ($7/month):**
- Always on (no sleep)
- Faster performance
- More resources

---

## 📊 RENDER DASHBOARD

**After deployment, you can:**

- View logs (real-time)
- Monitor performance
- Restart app manually
- Update environment variables
- View deployment history

---

## 🎓 FOR DEMO/SUBMISSION

**Share this URL:**
```
https://your-app-name.onrender.com
```

**Tips:**
1. Test before demo
2. Keep app active before presentation (visit it 5 min before)
3. Have backup localhost running (in case of internet issues)
4. Note: First load may be slow, explain it's free tier

---

## 📝 SUMMARY

**What you need:**
1. GitHub account ✅
2. Render account ✅
3. Push code to GitHub ✅
4. Deploy on Render ✅
5. Share your URL! 🎉

**Your project will be:**
- ✅ Live on internet
- ✅ Accessible from anywhere
- ✅ Professional portfolio piece
- ✅ Free forever

---

## 🚀 READY TO DEPLOY?

**Follow steps 1-5 above and your app will be live in 15 minutes!**

**Need help? Common issues are in Troubleshooting section.**

**Good luck! 💪**
