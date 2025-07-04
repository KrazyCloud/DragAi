from utils.log import logger
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from plugin.chatAnswer import get_answer
from env.authenticate import authenticate_token

router = APIRouter()

# ALLOWED_IP = ["10.226.53.238","10.226.37.205"]

# WebSocket server handler
@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str):

    client_ip = websocket.client.host
    print(f"🔍 Incoming connection from: {client_ip}")

    # Block unauthorized IPs
    #if client_ip not in ALLOWED_IP:
     #   print("❌ Unauthorized IP Address! Connection blocked.")
      #  await websocket.close(code=1008)
       # return

    await authenticate_token(token)
    logger.info("Authentication Verified")

    await websocket.accept()
    logger.info("Client connected.")
    
    exit_phrases = {"bye", "goodbye", "see you", "exit", "quit", "disconnect"}
    thanks_phrases = {"thanks", "thank you", "appreciate it", "thx"}
    bucket = {"crawling", "scrapping", "scrape", "crawl"}

    while True:
        try:
            user_input = await websocket.receive_text()
            logger.info(f"User input: {user_input}")

            # Check for exit phrases and disconnect
            if any(phrase in user_input.lower() for phrase in exit_phrases):
                exit_message = "Goodbye! Disconnecting..."
                await websocket.send_text(exit_message)
                logger.info("Client requested disconnection.")
                continue

            # Check for thank-you messages and reply
            if any(phrase in user_input.lower() for phrase in thanks_phrases):
                thanks_message = "You're welcome! Let me know if you need anything else. 😊"
                await websocket.send_text(thanks_message)
                logger.info("User expressed gratitude.")
                continue

            # Check for restricted words
            if any(word in user_input.lower() for word in bucket):
                warning_message = "Please use the word 'fetch' instead of 'crawling' or 'scrapping'."
                await websocket.send_text(warning_message)
                logger.warning(f"User used restricted words: {user_input}")
                continue

            # Get answer and send back to client
            answer = get_answer(user_input)
            await websocket.send_text(answer)

        except WebSocketDisconnect:
            logger.info("Client disconnected gracefully.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await websocket.send_text(f"Error: {str(e)}")
            break
