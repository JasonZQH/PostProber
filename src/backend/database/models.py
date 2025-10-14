"""
Database models for OAuth token storage and user management
"""
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from pathlib import Path
import json

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / "postprober.db"
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table (simple session-based users)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Platform tokens table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS platform_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                access_token TEXT NOT NULL,
                refresh_token TEXT,
                token_type TEXT DEFAULT 'Bearer',
                expires_at TIMESTAMP,
                scope TEXT,
                platform_user_id TEXT,
                platform_username TEXT,
                platform_user_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, platform)
            )
        """)

        # OAuth state tracking (for CSRF protection)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS oauth_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                code_verifier TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_platform_tokens_user_platform ON platform_tokens(user_id, platform)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_oauth_states_state ON oauth_states(state)")

        conn.commit()
        conn.close()

    # User Management
    def create_user(self, session_id: str) -> int:
        """Create a new user with session ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (session_id) VALUES (?)", (session_id,))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    def get_user_by_session(self, session_id: str) -> Optional[Dict]:
        """Get user by session ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_user_activity(self, user_id: int):
        """Update user's last active timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_active = ? WHERE id = ?",
            (datetime.now(), user_id)
        )
        conn.commit()
        conn.close()

    # Platform Token Management
    def save_platform_token(
        self,
        user_id: int,
        platform: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        token_type: str = "Bearer",
        expires_in: Optional[int] = None,
        scope: Optional[str] = None,
        platform_user_id: Optional[str] = None,
        platform_username: Optional[str] = None,
        platform_user_data: Optional[Dict] = None
    ) -> int:
        """Save or update platform token"""
        conn = self.get_connection()
        cursor = conn.cursor()

        expires_at = None
        if expires_in:
            expires_at = datetime.now() + timedelta(seconds=expires_in)

        user_data_json = json.dumps(platform_user_data) if platform_user_data else None

        # Check if token exists
        cursor.execute(
            "SELECT id FROM platform_tokens WHERE user_id = ? AND platform = ?",
            (user_id, platform)
        )
        existing = cursor.fetchone()

        if existing:
            # Update existing token
            cursor.execute("""
                UPDATE platform_tokens
                SET access_token = ?,
                    refresh_token = ?,
                    token_type = ?,
                    expires_at = ?,
                    scope = ?,
                    platform_user_id = ?,
                    platform_username = ?,
                    platform_user_data = ?,
                    updated_at = ?
                WHERE user_id = ? AND platform = ?
            """, (
                access_token, refresh_token, token_type, expires_at, scope,
                platform_user_id, platform_username, user_data_json,
                datetime.now(), user_id, platform
            ))
            token_id = existing[0]
        else:
            # Insert new token
            cursor.execute("""
                INSERT INTO platform_tokens (
                    user_id, platform, access_token, refresh_token, token_type,
                    expires_at, scope, platform_user_id, platform_username,
                    platform_user_data, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, platform, access_token, refresh_token, token_type,
                expires_at, scope, platform_user_id, platform_username,
                user_data_json, datetime.now()
            ))
            token_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return token_id

    def get_platform_token(self, user_id: int, platform: str) -> Optional[Dict]:
        """Get platform token for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM platform_tokens WHERE user_id = ? AND platform = ?",
            (user_id, platform)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            token_data = dict(row)
            if token_data.get('platform_user_data'):
                token_data['platform_user_data'] = json.loads(token_data['platform_user_data'])
            return token_data
        return None

    def get_user_platforms(self, user_id: int) -> List[Dict]:
        """Get all connected platforms for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM platform_tokens WHERE user_id = ?",
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        platforms = []
        for row in rows:
            platform_data = dict(row)
            if platform_data.get('platform_user_data'):
                platform_data['platform_user_data'] = json.loads(platform_data['platform_user_data'])
            platforms.append(platform_data)
        return platforms

    def delete_platform_token(self, user_id: int, platform: str) -> bool:
        """Delete platform token (disconnect)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM platform_tokens WHERE user_id = ? AND platform = ?",
            (user_id, platform)
        )
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def get_expiring_tokens(self, hours: int = 24) -> List[Dict]:
        """Get tokens expiring within specified hours"""
        conn = self.get_connection()
        cursor = conn.cursor()
        expiry_threshold = datetime.now() + timedelta(hours=hours)
        cursor.execute(
            "SELECT * FROM platform_tokens WHERE expires_at IS NOT NULL AND expires_at <= ?",
            (expiry_threshold,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # OAuth State Management
    def create_oauth_state(
        self,
        state: str,
        user_id: int,
        platform: str,
        code_verifier: Optional[str] = None,
        expires_in: int = 600
    ) -> int:
        """Create OAuth state for CSRF protection"""
        conn = self.get_connection()
        cursor = conn.cursor()
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        cursor.execute("""
            INSERT INTO oauth_states (state, user_id, platform, code_verifier, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (state, user_id, platform, code_verifier, expires_at))
        state_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return state_id

    def get_oauth_state(self, state: str) -> Optional[Dict]:
        """Get OAuth state and verify it's not expired"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM oauth_states WHERE state = ? AND expires_at > ?",
            (state, datetime.now())
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def delete_oauth_state(self, state: str):
        """Delete OAuth state after use"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM oauth_states WHERE state = ?", (state,))
        conn.commit()
        conn.close()

    def cleanup_expired_states(self):
        """Remove expired OAuth states"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM oauth_states WHERE expires_at <= ?", (datetime.now(),))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted


# Singleton instance
db = Database()
