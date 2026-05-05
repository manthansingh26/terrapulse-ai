from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.models import EnvironmentalData
from app.db.database import SessionLocal
from sqlalchemy import desc
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["WebSocket"])

# Store active connections
active_connections = []


@router.websocket("/cities")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time city data updates"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"✅ WebSocket client connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"📨 Received message: {data}")
            
            if data == "get_cities":
                # Query latest city data
                db = SessionLocal()
                try:
                    # Get latest data for each city
                    cities_data = db.query(EnvironmentalData).order_by(
                        desc(EnvironmentalData.timestamp)
                    ).all()
                    
                    logger.info(f"📊 Retrieved {len(cities_data)} city records from database")
                    
                    # Format as JSON
                    response = {
                        "type": "cities_update",
                        "timestamp": datetime.now().isoformat(),
                        "cities": [
                            {
                                "city": city.city,
                                "aqi": city.aqi,
                                "temperature": city.temperature,
                                "humidity": city.humidity,
                                "last_updated": city.timestamp.isoformat() if city.timestamp else None
                            }
                            for city in cities_data
                        ]
                    }
                    
                    # Send to all connected clients
                    for connection in active_connections:
                        try:
                            await connection.send_json(response)
                            logger.info("📤 Sent data to client")
                        except Exception as e:
                            logger.error(f"❌ Error sending to connection: {e}")
                finally:
                    db.close()
                    
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
        logger.info(f"❌ Client disconnected. Remaining connections: {len(active_connections)}")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}", exc_info=True)
        if websocket in active_connections:
            active_connections.remove(websocket)
        await websocket.close()
