#!/usr/bin/env python3
"""MTProto proxy access-control bot.

Users: /start to request access.
Owner: Approve/Deny buttons; /list; /revoke @username or user_id.
"""
import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from telegram.request import HTTPXRequest

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ENV_FILE = Path.home() / ".config/remote-access/env"
USERS_FILE = Path.home() / ".config/proxy-bot/users.json"
STATE_FILE = Path.home() / ".config/proxy-bot/state.json"


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


ENV = load_env()
BOT_TOKEN = os.environ.get("BOT_TOKEN") or ENV.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("CHAT_ID") or ENV.get("CHAT_ID", "0"))


def load_users() -> dict:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return {}


def save_users(users: dict):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, indent=2))


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def current_proxy_link() -> str:
    state = load_state()
    return state.get("bore_link") or state.get("tailscale_link") or ""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def user_label(info: dict) -> str:
    name = info.get("name", "")
    handle = f"@{info['username']}" if info.get("username") else f"id:{info['user_id']}"
    return f"{handle} ({name})" if name else handle


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == OWNER_ID:
        await update.message.reply_text(
            "Owner commands:\n/list — all users\n/revoke @username or user_id"
        )
        return

    users = load_users()
    uid = str(user.id)

    if uid in users:
        record = users[uid]
        if record.get("approved"):
            link = current_proxy_link()
            if link:
                await update.message.reply_text(
                    "You're approved. Tap to add the proxy:",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Add Proxy", url=link)]]
                    ),
                )
            else:
                await update.message.reply_text(
                    "You're approved, but the proxy server is currently offline. Try again later."
                )
        elif record.get("denied"):
            await update.message.reply_text("Your request was denied.")
        else:
            await update.message.reply_text("Your request is pending. You'll be notified.")
        return

    # New request
    users[uid] = {
        "user_id": user.id,
        "username": user.username or "",
        "name": user.full_name or "",
        "approved": False,
        "denied": False,
        "requested_at": now_iso(),
    }
    save_users(users)

    label = user_label(users[uid])
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Approve", callback_data=f"approve:{uid}"),
            InlineKeyboardButton("Deny", callback_data=f"deny:{uid}"),
        ]
    ])
    await context.bot.send_message(
        OWNER_ID,
        f"Proxy access request from {label}",
        reply_markup=keyboard,
    )
    await update.message.reply_text(
        "Request sent to the admin. You'll receive the proxy link if approved."
    )


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    users = load_users()
    if not users:
        await update.message.reply_text("No requests yet.")
        return
    lines = []
    for uid, info in users.items():
        status = "✓" if info.get("approved") else ("✗" if info.get("denied") else "⏳")
        lines.append(f"{status} {user_label(info)}")
    await update.message.reply_text("\n".join(lines))


async def cmd_revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /revoke @username or user_id")
        return

    target = args[0].lstrip("@")
    users = load_users()
    found = None

    for uid, info in users.items():
        if uid == target or info.get("username", "").lower() == target.lower():
            found = (uid, info)
            break

    if not found:
        await update.message.reply_text(f"User not found: {target}")
        return

    uid, info = found
    users[uid]["approved"] = False
    users[uid]["denied"] = True
    users[uid]["revoked_at"] = now_iso()
    save_users(users)
    await update.message.reply_text(f"Revoked access for {user_label(info)}.")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.from_user.id != OWNER_ID:
        await query.answer("Not authorized.")
        return

    await query.answer()  # ack immediately so Telegram stops showing spinner

    action, uid = query.data.split(":", 1)
    users = load_users()

    if uid not in users:
        await query.edit_message_text("User not found (may have been removed).")
        return

    info = users[uid]
    label = user_label(info)

    if action == "approve":
        users[uid]["approved"] = True
        users[uid]["denied"] = False
        users[uid]["approved_at"] = now_iso()
        save_users(users)

        link = current_proxy_link()
        if link:
            try:
                await context.bot.send_message(
                    int(uid),
                    "Your proxy access has been approved!",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Add Proxy", url=link)]]
                    ),
                )
            except Exception as e:
                log.warning("Could not message user %s: %s", uid, e)

        await query.edit_message_text(f"Approved {label}.")

    elif action == "deny":
        users[uid]["approved"] = False
        users[uid]["denied"] = True
        users[uid]["denied_at"] = now_iso()
        save_users(users)
        await query.edit_message_text(f"Denied {label}.")


def main():
    if not BOT_TOKEN:
        sys.exit("BOT_TOKEN not set")
    if not OWNER_ID:
        sys.exit("CHAT_ID not set")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(HTTPXRequest(connect_timeout=15, read_timeout=30, write_timeout=30))
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(CommandHandler("revoke", cmd_revoke))
    app.add_handler(CallbackQueryHandler(handle_callback))

    log.info("proxy-bot starting (owner_id=%d)", OWNER_ID)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
