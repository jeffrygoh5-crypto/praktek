"""
Template Flask Login -> Dashboard
Deploy: Vercel | Database: Supabase (PostgreSQL)
"""
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ganti-secret-key-ini")

# DATABASE_URL diambil dari Environment Variable (Vercel / file .env lokal).
# Gunakan connection string "Transaction pooler" Supabase (port 6543).
db_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
# Paksa pakai driver psycopg (versi 3) supaya cocok dengan requirements.txt
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# NullPool: tidak menahan koneksi, cocok untuk serverless (Vercel)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"poolclass": NullPool}

db = SQLAlchemy(app)

# Zona Waktu WIB (Asia/Jakarta, UTC+7)
try:
    WIB = ZoneInfo("Asia/Jakarta")
except ZoneInfoNotFoundError:
    WIB = timezone(timedelta(hours=7), name="WIB")


def to_wib(dt):
    """Konversi objek datetime ke zona waktu WIB (UTC+7)."""
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(WIB)


@app.template_filter("to_wib")
def filter_to_wib(dt, fmt="%d %b %Y, %H:%M WIB"):
    """Filter Jinja2 untuk menampilkan format tanggal dalam zona waktu WIB."""
    wib_dt = to_wib(dt)
    return wib_dt.strftime(fmt) if wib_dt else "-"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=func.now())


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    return redirect(url_for("dashboard" if "user_id" in session else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["nama"] = user.nama or user.username
            return redirect(url_for("dashboard"))

        flash("Username atau password salah.", "danger")
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    now_wib = datetime.now(WIB)
    awal_hari_ini_wib = now_wib.replace(hour=0, minute=0, second=0, microsecond=0)

    # 7 hari terakhir dalam zona waktu WIB (6 hari yang lalu s.d. hari ini)
    day_dates = [(now_wib - timedelta(days=i)).date() for i in range(6, -1, -1)]
    trend_labels = [d.strftime("%d %b") for d in day_dates]
    trend_data = [0] * 7

    tujuh_hari_lalu_wib = datetime.combine(day_dates[0], datetime.min.time(), tzinfo=WIB)
    # Gunakan buffer -1 hari saat query SQL agar aman terhadap perbedaan timezone sesi DB,
    # lalu saring presisi berdasarkan zona waktu WIB di Python.
    query_batas_utc_naive = (tujuh_hari_lalu_wib.astimezone(timezone.utc) - timedelta(days=1)).replace(tzinfo=None)

    total_user = User.query.count()

    # Hitung pendaftaran per hari dan total 7 hari terakhir berdasarkan WIB
    recent_users = User.query.filter(User.created_at >= query_batas_utc_naive).all()
    user_hari_ini = 0
    user_7_hari = 0

    for u in recent_users:
        if u.created_at:
            u_wib = to_wib(u.created_at)
            if u_wib >= awal_hari_ini_wib:
                user_hari_ini += 1
            if u_wib >= tujuh_hari_lalu_wib:
                user_7_hari += 1
            u_date = u_wib.date()
            if u_date in day_dates:
                idx = day_dates.index(u_date)
                trend_data[idx] += 1

    user_lama = max(0, total_user - user_7_hari)

    komposisi_labels = ["User Baru (7 Hari)", "User Lama"]
    komposisi_data = [user_7_hari, user_lama]

    # Ambil 5 user terakhir untuk tabel User Terbaru
    latest_users = User.query.order_by(User.created_at.desc(), User.id.desc()).limit(5).all()

    bulan_indo = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    tanggal_hari_ini = f"{now_wib.day} {bulan_indo[now_wib.month]} {now_wib.year}"

    return render_template(
        "dashboard.html",
        nama=session["nama"],
        tanggal_hari_ini=tanggal_hari_ini,
        total_user=total_user,
        user_hari_ini=user_hari_ini,
        user_7_hari=user_7_hari,
        trend_labels=trend_labels,
        trend_data=trend_data,
        komposisi_labels=komposisi_labels,
        komposisi_data=komposisi_data,
        latest_users=latest_users,
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
