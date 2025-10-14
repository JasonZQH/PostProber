"""
WebSocket Manager

Manages WebSocket connections for real-time health alerts.
Broadcasts health status changes to all connected clients.
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Set
import json
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections and broadcasting

    Features:
    - Multiple client connections
    - Broadcast to all clients
    - Connection state tracking
    - Automatic cleanup on disconnect
    - Heartbeat/ping mechanism
    """

    def __init__(self):
        # Active WebSocket connections
        self.active_connections: List[WebSocket] = []

        # Track connection metadata
        self.connection_metadata: Dict[WebSocket, Dict] = {}

        # Alert history (last 50 alerts)
        self.alert_history: List[Dict] = []
        self.max_history = 50

    async def connect(self, websocket: WebSocket, client_id: str = None):
        """
        Accept a new WebSocket connection

        Args:
            websocket: WebSocket connection object
            client_id: Optional unique identifier for client
        """
        await websocket.accept()

        self.active_connections.append(websocket)
        self.connection_metadata[websocket] = {
            "client_id": client_id or f"client_{len(self.active_connections)}",
            "connected_at": datetime.now().isoformat(),
            "alerts_sent": 0
        }

        logger.info(f"Client connected: {self.connection_metadata[websocket]['client_id']}")
        logger.info(f"Total active connections: {len(self.active_connections)}")

        # Send welcome message with connection info
        await self.send_personal_message({
            "type": "connection",
            "status": "connected",
            "client_id": self.connection_metadata[websocket]["client_id"],
            "timestamp": datetime.now().isoformat(),
            "message": "Connected to PostProber Health Monitor"
        }, websocket)

        # Send recent alert history
        if self.alert_history:
            await self.send_personal_message({
                "type": "history",
                "alerts": self.alert_history[-10:],  # Last 10 alerts
                "timestamp": datetime.now().isoformat()
            }, websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection

        Args:
            websocket: WebSocket connection object
        """
        if websocket in self.active_connections:
            client_info = self.connection_metadata.get(websocket, {})
            logger.info(f"Client disconnected: {client_info.get('client_id', 'unknown')}")

            self.active_connections.remove(websocket)
            self.connection_metadata.pop(websocket, None)

            logger.info(f"Total active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        """
        Send a message to a specific client

        Args:
            message: Message dictionary
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: Dict):
        """
        Broadcast a message to all connected clients

        Args:
            message: Message dictionary to broadcast
        """
        if not self.active_connections:
            logger.debug("No active connections to broadcast to")
            return

        logger.info(f"Broadcasting to {len(self.active_connections)} clients: {message.get('type', 'unknown')}")

        # Track disconnected clients
        disconnected = []

        # Send to all active connections
        for connection in self.active_connections:
            try:
                await connection.send_json(message)

                # Update metadata
                if connection in self.connection_metadata:
                    self.connection_metadata[connection]["alerts_sent"] += 1

            except WebSocketDisconnect:
                logger.warning(f"Client disconnected during broadcast")
                disconnected.append(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_health_alert(self, alert: Dict):
        """
        Broadcast a health alert to all clients

        Args:
            alert: Health alert dictionary with:
                - platform: str
                - severity: "critical" | "warning" | "info"
                - message: str
                - recommended_action: str
                - timestamp: str (ISO format)
                - status: str (healthy/degraded/down)
        """
        # Add to history
        self.alert_history.append(alert)

        # Keep only last N alerts
        if len(self.alert_history) > self.max_history:
            self.alert_history = self.alert_history[-self.max_history:]

        # Broadcast to all clients
        await self.broadcast({
            "type": "health_alert",
            "alert": alert,
            "timestamp": datetime.now().isoformat()
        })

    async def broadcast_health_update(self, health_data: List[Dict]):
        """
        Broadcast periodic health status update

        Args:
            health_data: List of health check results for all platforms
        """
        await self.broadcast({
            "type": "health_update",
            "platforms": health_data,
            "timestamp": datetime.now().isoformat()
        })

    async def ping_all(self):
        """
        Send ping to all clients to keep connections alive
        """
        await self.broadcast({
            "type": "ping",
            "timestamp": datetime.now().isoformat()
        })

    def get_stats(self) -> Dict:
        """
        Get connection statistics

        Returns:
            Statistics dictionary
        """
        return {
            "active_connections": len(self.active_connections),
            "total_alerts": len(self.alert_history),
            "clients": [
                {
                    "client_id": meta["client_id"],
                    "connected_at": meta["connected_at"],
                    "alerts_sent": meta["alerts_sent"]
                }
                for meta in self.connection_metadata.values()
            ]
        }


# Global instance
manager = ConnectionManager()


async def handle_websocket_connection(websocket: WebSocket, client_id: str = None):
    """
    Handle a WebSocket connection lifecycle

    Args:
        websocket: WebSocket connection
        client_id: Optional client identifier
    """
    await manager.connect(websocket, client_id)

    try:
        # Keep connection alive and handle incoming messages
        while True:
            # Receive messages from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                message_type = message.get("type", "unknown")

                # Handle different message types
                if message_type == "pong":
                    # Client responded to ping
                    logger.debug(f"Received pong from client")

                elif message_type == "get_stats":
                    # Client requested stats
                    stats = manager.get_stats()
                    await manager.send_personal_message({
                        "type": "stats",
                        "data": stats,
                        "timestamp": datetime.now().isoformat()
                    }, websocket)

                elif message_type == "get_history":
                    # Client requested alert history
                    await manager.send_personal_message({
                        "type": "history",
                        "alerts": manager.alert_history[-20:],  # Last 20
                        "timestamp": datetime.now().isoformat()
                    }, websocket)

                else:
                    logger.warning(f"Unknown message type: {message_type}")

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {data}")
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    except WebSocketDisconnect:
        logger.info("Client disconnected normally")
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# Background task for periodic pings
async def ping_clients_periodically(interval: int = 30):
    """
    Periodically ping all clients to keep connections alive

    Args:
        interval: Seconds between pings (default: 30)
    """
    while True:
        await asyncio.sleep(interval)
        await manager.ping_all()
