import subprocess
import logging


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    cmd = "python main.py --mode full"
    logging.info(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        logging.error("Weekly pipeline failed!")
    else:
        logging.info("Weekly pipeline completed successfully.")
        save_result = subprocess.run(["python", "scripts/save_last_update.py"])
        if save_result.returncode != 0:
            logging.error("Failed to save last update (exit code %s)", save_result.returncode)
        else:
            logging.info("Saved last update timestamp.")


if __name__ == "__main__":
    main()
