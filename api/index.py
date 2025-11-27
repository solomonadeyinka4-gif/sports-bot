import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
import os

TOKEN = "8398040646:AAGIscooSFhP1BO_TEq4H1MH2gRuc9Jd5eM"

# Model setup (same as before)
df = pd.DataFrame({
    'home_strength': [88,82,91,79,85,90,76,87,83,89,95,70,92,78,86],
    'away_strength': [83,89,80,85,92,78,90,81,87,79,75,94,80,88,84],
    'winner': [0,2,0,1,2,0,2,0,0,2,0,2,1,0,2]
})
model = LogisticRegression(multi_class='multinomial', max_iter=1000)
model.fit(df[['home_strength','away_strength']], df['winner'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot on Vercel! /predict football TeamA vs TeamB")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Same predict logic as before
    if not context.args:
        await update.message.reply_text("Usage: /predict <sport> team1 vs team2")
        return
    try:
        text = " ".join(context.args).lower()
        if " vs " not in text:
            await update.message.reply_text("Use: team1 vs team2")
            return
        team1, team2 = [t.strip().capitalize() for t in text.split(" vs ")]
        s1 = np.random.randint(75,96)
        s2 = np.random.randint(75,96)
        pred = model.predict([[s1,s2]])[0]
        conf = max(model.predict_proba([[s1,s2]])[0]) * 100
        outcomes = ["Home Win 🏆", "Draw 🤝", "Away Win 🏆"]
        await update.message.reply_text(
            f"*{team1} vs {team2}*\n\n"
            f"Prediction: *{outcomes[pred]}*\n"
            f"Confidence: {conf:.1f}%\n\n"
            "Hosted free on Vercel!",
            parse_mode="Markdown"
        )
    except:
        await update.message.reply_text("Try: /predict football Arsenal vs Chelsea")

# Vercel handler for webhook
async def handler(request):
    update = Update.de_json(json.loads(await request.body()), app.bot)
    await app.process_update(update)
    return 'OK'

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))

# For Vercel: export async def main(request): ... (full docs: vercel.com/docs/functions)
