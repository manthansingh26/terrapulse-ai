from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.models import EnvironmentalData
from app.db.database import SessionLocal
from sqlalchemy import desc
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["WebSocket"])

# Store active connections
active_connections = set()


@router.websocket("/cities")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time city data updates"""
    await websocket.accept()
    active_connections.add(websocket)
    logger.info(
        f"✅ WebSocket client connected. Total connections: {len(active_connections)}"
    )

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"📨 Received message: {data}")

            if data == "get_cities":
                # Query latest city data
                db = SessionLocal()
                try:
                    from sqlalchemy import func, and_
                    subquery = (
                        db.query(
                            EnvironmentalData.city,
                            func.max(EnvironmentalData.timestamp).label("max_timestamp"),
                        )
                        .group_by(EnvironmentalData.city)
                        .subquery()
                    )
                    # Get latest data for each city
                    cities_data = (
                        db.query(EnvironmentalData)
                        .filter(
                            and_(
                                EnvironmentalData.city == subquery.c.city,
                                EnvironmentalData.timestamp == subquery.c.max_timestamp,
                            )
                        )
                        .all()
                    )

                    logger.info(
                        f"📊 Retrieved {len(cities_data)} city records from database"
                    )

                    # Format as JSON
                    response = {
                        "type": "cities_update",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "cities": [
                            {
                                "city": city.city,
                                "aqi": city.aqi,
                                "temperature": city.temperature,
                                "humidity": city.humidity,
                                "last_updated": (
                                    city.timestamp.isoformat()
                                    if city.timestamp
                                    else None
                                ),
                            }
                            for city in cities_data
                        ],
                    }

                    # Send only to the requesting client
                    try:
                        await websocket.send_json(response)
                        logger.info("📤 Sent data to client")
                    except Exception as e:
                        logger.error(f"❌ Error sending to connection: {e}")
                finally:
                    db.close()

    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.discard(websocket)
        logger.info(
            f"❌ Client disconnected. Remaining connections: {len(active_connections)}"
        )
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}", exc_info=True)
        if websocket in active_connections:
            active_connections.discard(websocket)
        await websocket.close()
