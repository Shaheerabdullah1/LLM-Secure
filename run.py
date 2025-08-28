import multiprocessing
import uvicorn

def run_middle_bot():
    uvicorn.run("api-middle-bot:app", host="127.0.0.1", port=8000)

def run_final_bot():
    uvicorn.run("api-final-bot:app", host="127.0.0.1", port=8001)

if __name__ == "__main__":
    try:
        # Create processes
        p1 = multiprocessing.Process(target=run_middle_bot)
        p2 = multiprocessing.Process(target=run_final_bot)

        # Start processes
        p1.start()
        p2.start()

        # Wait for processes
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("\nShutting down servers...") 