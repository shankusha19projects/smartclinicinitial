from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
DB_DIR = ROOT / "data"
DB_PATH = DB_DIR / "smarclinicai.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
SESSION_COOKIE = "scai_session"
SESSION_HOURS = 12


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def iso(value: dt.datetime) -> str:
    return value.replace(microsecond=0).isoformat()


def hash_password(password: str, salt_hex: str | None = None) -> str:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"pbkdf2_sha256$120000${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, rounds, salt_hex, digest_hex = stored.split("$", 3)
    except ValueError:
        return False
    if algo != "pbkdf2_sha256":
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(rounds))
    return hmac.compare_digest(digest.hex(), digest_hex)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def one(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> sqlite3.Row | None:
    return conn.execute(sql, params).fetchone()


def all_rows(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[dict]:
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def init_db() -> None:
    DB_DIR.mkdir(exist_ok=True)
    with db() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        tenant = one(conn, "SELECT id FROM tenants WHERE slug = ?", ("smartclinic-local",))
        if tenant is None:
            cur = conn.execute(
                "INSERT INTO tenants (name, slug, status) VALUES (?, ?, ?)",
                ("SmartClinic Local", "smartclinic-local", "active"),
            )
            tenant_id = cur.lastrowid
        else:
            tenant_id = tenant["id"]

        if one(conn, "SELECT id FROM users WHERE username = ?", ("Shash",)) is None:
            conn.execute(
                """
                INSERT INTO users (tenant_id, username, password_hash, full_name, role, specialty)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (tenant_id, "Shash", hash_password("12345"), "Shash", "Admin", "Clinic Administrator"),
            )

        if one(conn, "SELECT id FROM patients WHERE tenant_id = ? LIMIT 1", (tenant_id,)) is None:
            seed_patients(conn, tenant_id)

        if one(conn, "SELECT id FROM appointments WHERE tenant_id = ? LIMIT 1", (tenant_id,)) is None:
            seed_appointments(conn, tenant_id)


def seed_patients(conn: sqlite3.Connection, tenant_id: int) -> None:
    patients = [
        ("PT-8421", "Maria", "Gonzalez", "1954-05-12", "Spanish", "(973) 555-0112", "maria.g@email.com", "Medicaid", "scheduled", "Post-op orthopedic followup. Hypertensive."),
        ("PT-7732", "Wei", "Chen", "1982-11-04", "Mandarin", "(908) 555-0247", "wei.chen@email.com", "Blue Cross", "scheduled", "Cardiac monitoring. EKG every 3 months."),
        ("PT-9102", "Amir", "Al-Fayed", "1975-02-28", "Arabic", "(732) 555-0389", "amir.af@email.com", "United Healthcare", "completed", "Type 2 diabetes. Medication review completed."),
        ("PT-6544", "Elena", "Rostova", "1968-09-15", "Russian", "(201) 555-0415", "elena.r@email.com", "Aetna", "completed", "Asthma management. Inhaler technique corrected."),
        ("PT-5218", "Priya", "Sharma", "1990-07-22", "Hindi", "(848) 555-0533", "priya.s@email.com", "Cigna", "active", "Prenatal care, 28 weeks. GTT test scheduled."),
        ("PT-4390", "Carlos", "Mendez", "1965-03-10", "Spanish", "(609) 555-0628", "carlos.m@email.com", "Medicare", "active", "Hypertension and hyperlipidemia. Statin dosage increased."),
    ]
    today = utcnow().date().isoformat()
    conn.executemany(
        """
        INSERT INTO patients
        (tenant_id, patient_code, first_name, last_name, dob, language, phone, email, insurance, last_visit, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(tenant_id, *p[:8], today, p[8], p[9]) for p in patients],
    )


def seed_appointments(conn: sqlite3.Connection, tenant_id: int) -> None:
    today = utcnow().date().isoformat()
    rows = [
        ("7:30 AM", "Elena Rostova", "Russian", "Asthma Followup", 30, "completed"),
        ("8:15 AM", "Amir Al-Fayed", "Arabic", "Diabetes Mgmt", 30, "completed"),
        ("9:30 AM", "Maria Gonzalez", "Spanish", "Post-op Followup", 45, "scheduled"),
        ("11:00 AM", "Wei Chen", "Mandarin", "Cardiac Checkup", 30, "scheduled"),
        ("2:00 PM", "Priya Sharma", "Hindi", "Prenatal Visit", 45, "scheduled"),
        ("3:30 PM", "Carlos Mendez", "Spanish", "Cardiology Review", 30, "scheduled"),
    ]
    conn.executemany(
        """
        INSERT INTO appointments
        (tenant_id, patient_name, appointment_date, appointment_time, language, appointment_type, duration_minutes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(tenant_id, patient, today, time, lang, kind, duration, status) for time, patient, lang, kind, duration, status in rows],
    )


class Handler(SimpleHTTPRequestHandler):
    server_version = "SmartClinicsLocal/1.0"

    def translate_path(self, path: str) -> str:
        return str(ROOT / super().translate_path(path).replace(os.getcwd(), "").lstrip("\\/"))

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return
        if parsed.path.startswith("/api/"):
            self.handle_api("GET", parsed.path, parse_qs(parsed.query))
            return
        if parsed.path == "/app/" or parsed.path == "/app":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/app/dashboard.html")
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api("POST", parsed.path, parse_qs(parsed.query))
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def json_body(self) -> dict:
        length = int(self.headers.get("content-length", "0"))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def send_json(self, payload: dict | list, status: HTTPStatus = HTTPStatus.OK, cookie: str | None = None) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(data)

    def current_session(self) -> dict | None:
        cookie = SimpleCookie(self.headers.get("Cookie"))
        morsel = cookie.get(SESSION_COOKIE)
        if not morsel:
            return None
        with db() as conn:
            row = one(
                conn,
                """
                SELECT s.id AS session_id, s.tenant_id, s.user_id, u.username, u.full_name, u.role,
                       u.specialty, t.name AS tenant_name, t.slug AS tenant_slug
                FROM sessions s
                JOIN users u ON u.id = s.user_id
                JOIN tenants t ON t.id = s.tenant_id
                WHERE s.token_hash = ? AND s.expires_at > ?
                """,
                (token_hash(morsel.value), iso(utcnow())),
            )
            return dict(row) if row else None

    def require_session(self) -> dict | None:
        session = self.current_session()
        if session is None:
            self.send_json({"error": "Authentication required"}, HTTPStatus.UNAUTHORIZED)
        return session

    def handle_api(self, method: str, path: str, query: dict) -> None:
        try:
            if path == "/api/health" and method == "GET":
                self.send_json({"ok": True, "database": str(DB_PATH), "databaseName": "smarclinicai"})
            elif path == "/api/login" and method == "POST":
                self.login()
            elif path == "/api/logout" and method == "POST":
                self.logout()
            elif path == "/api/me" and method == "GET":
                session = self.require_session()
                if session:
                    self.send_json({"user": public_user(session), "tenant": public_tenant(session)})
            elif path == "/api/bootstrap" and method == "GET":
                self.bootstrap()
            elif path == "/api/patients" and method == "GET":
                self.get_patients()
            elif path == "/api/patients" and method == "POST":
                self.create_patient()
            elif path == "/api/appointments" and method == "GET":
                self.get_appointments(query)
            elif path == "/api/appointments" and method == "POST":
                self.create_appointment()
            elif path == "/api/sessions/create" and method == "POST":
                self.create_translation_session()
            else:
                self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, HTTPStatus.BAD_REQUEST)
        except sqlite3.Error as exc:
            self.send_json({"error": "Database error", "detail": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def login(self) -> None:
        payload = self.json_body()
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        with db() as conn:
            row = one(
                conn,
                """
                SELECT u.*, t.name AS tenant_name, t.slug AS tenant_slug
                FROM users u JOIN tenants t ON t.id = u.tenant_id
                WHERE u.username = ? AND u.status = 'active' AND t.status = 'active'
                """,
                (username,),
            )
            if row is None or not verify_password(password, row["password_hash"]):
                self.send_json({"error": "Invalid username or password"}, HTTPStatus.UNAUTHORIZED)
                return
            raw_token = secrets.token_urlsafe(32)
            expires_at = iso(utcnow() + dt.timedelta(hours=SESSION_HOURS))
            conn.execute(
                "INSERT INTO sessions (tenant_id, user_id, token_hash, expires_at) VALUES (?, ?, ?, ?)",
                (row["tenant_id"], row["id"], token_hash(raw_token), expires_at),
            )
            conn.execute(
                "INSERT INTO audit_logs (tenant_id, user_id, action, entity_type) VALUES (?, ?, ?, ?)",
                (row["tenant_id"], row["id"], "login", "user"),
            )
        cookie = f"{SESSION_COOKIE}={raw_token}; HttpOnly; SameSite=Lax; Path=/; Max-Age={SESSION_HOURS * 3600}"
        session = {
            "tenant_id": row["tenant_id"],
            "tenant_name": row["tenant_name"],
            "tenant_slug": row["tenant_slug"],
            "user_id": row["id"],
            "username": row["username"],
            "full_name": row["full_name"],
            "role": row["role"],
            "specialty": row["specialty"],
        }
        self.send_json({"ok": True, "user": public_user(session), "tenant": public_tenant(session)}, cookie=cookie)

    def logout(self) -> None:
        cookie = SimpleCookie(self.headers.get("Cookie"))
        morsel = cookie.get(SESSION_COOKIE)
        if morsel:
            with db() as conn:
                conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash(morsel.value),))
        expired = f"{SESSION_COOKIE}=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0"
        self.send_json({"ok": True}, cookie=expired)

    def bootstrap(self) -> None:
        session = self.require_session()
        if not session:
            return
        with db() as conn:
            counts = dict(
                patients=one(conn, "SELECT COUNT(*) AS c FROM patients WHERE tenant_id = ?", (session["tenant_id"],))["c"],
                appointments=one(conn, "SELECT COUNT(*) AS c FROM appointments WHERE tenant_id = ?", (session["tenant_id"],))["c"],
                sessions=one(conn, "SELECT COUNT(*) AS c FROM translation_sessions WHERE tenant_id = ?", (session["tenant_id"],))["c"],
            )
        self.send_json({"user": public_user(session), "tenant": public_tenant(session), "counts": counts})

    def get_patients(self) -> None:
        session = self.require_session()
        if not session:
            return
        with db() as conn:
            rows = all_rows(
                conn,
                """
                SELECT patient_code AS id, first_name AS firstName, last_name AS lastName, dob, language,
                       phone, email, insurance, last_visit AS lastVisit, status, notes
                FROM patients
                WHERE tenant_id = ?
                ORDER BY created_at DESC, id DESC
                """,
                (session["tenant_id"],),
            )
        self.send_json({"patients": rows})

    def create_patient(self) -> None:
        session = self.require_session()
        if not session:
            return
        payload = self.json_body()
        first = str(payload.get("firstName", "")).strip()
        last = str(payload.get("lastName", "")).strip()
        if not first or not last:
            self.send_json({"error": "First and last name are required"}, HTTPStatus.BAD_REQUEST)
            return
        with db() as conn:
            next_num = one(conn, "SELECT COUNT(*) + 1001 AS n FROM patients WHERE tenant_id = ?", (session["tenant_id"],))["n"]
            patient_code = f"PT-{next_num}"
            conn.execute(
                """
                INSERT INTO patients
                (tenant_id, patient_code, first_name, last_name, dob, language, phone, email, insurance, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session["tenant_id"],
                    patient_code,
                    first,
                    last,
                    payload.get("dob") or None,
                    payload.get("language") or "Spanish",
                    payload.get("phone") or None,
                    payload.get("email") or None,
                    payload.get("insurance") or None,
                    "active",
                    payload.get("notes") or None,
                ),
            )
        self.get_patients()

    def get_appointments(self, query: dict) -> None:
        session = self.require_session()
        if not session:
            return
        date = query.get("date", [utcnow().date().isoformat()])[0]
        with db() as conn:
            rows = all_rows(
                conn,
                """
                SELECT appointment_time AS time, patient_name AS patient, language AS lang,
                       appointment_type AS type, duration_minutes AS duration, status, appointment_date AS date
                FROM appointments
                WHERE tenant_id = ? AND appointment_date = ?
                ORDER BY appointment_date, appointment_time
                """,
                (session["tenant_id"], date),
            )
        self.send_json({"appointments": rows})

    def create_appointment(self) -> None:
        session = self.require_session()
        if not session:
            return
        payload = self.json_body()
        patient = str(payload.get("patient", "")).strip()
        if not patient:
            self.send_json({"error": "Patient name is required"}, HTTPStatus.BAD_REQUEST)
            return
        date = payload.get("date") or utcnow().date().isoformat()
        with db() as conn:
            conn.execute(
                """
                INSERT INTO appointments
                (tenant_id, patient_name, appointment_date, appointment_time, language, appointment_type, duration_minutes, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session["tenant_id"],
                    patient,
                    date,
                    payload.get("time") or "9:00 AM",
                    payload.get("lang") or "Spanish",
                    payload.get("type") or "Follow-up Visit",
                    int(payload.get("duration") or 30),
                    "scheduled",
                    payload.get("notes") or None,
                ),
            )
        self.get_appointments({"date": [date]})

    def create_translation_session(self) -> None:
        session = self.require_session()
        if not session:
            return
        payload = self.json_body()
        patient_name = str(payload.get("patient", "Guest Patient")).strip() or "Guest Patient"
        language = str(payload.get("language", "Spanish")).strip() or "Spanish"
        with db() as conn:
            cur = conn.execute(
                """
                INSERT INTO translation_sessions (tenant_id, patient_name, language, created_by)
                VALUES (?, ?, ?, ?)
                """,
                (session["tenant_id"], patient_name, language, session["user_id"]),
            )
            session_id = cur.lastrowid
        self.send_json({"sessionId": session_id, "patient": patient_name, "language": language})


def public_user(session: dict) -> dict:
    return {
        "id": session["user_id"],
        "username": session["username"],
        "fullName": session["full_name"],
        "role": session["role"],
        "specialty": session.get("specialty"),
    }


def public_tenant(session: dict) -> dict:
    return {
        "id": session["tenant_id"],
        "name": session["tenant_name"],
        "slug": session["tenant_slug"],
    }


if __name__ == "__main__":
    os.chdir(ROOT)
    init_db()
    port = int(os.environ.get("PORT", "3456"))
    httpd = ThreadingHTTPServer(("localhost", port), Handler)
    print(f"SmartClinics AI local server running at http://localhost:{port}")
    print(f"SQL database: {DB_PATH}")
    httpd.serve_forever()
