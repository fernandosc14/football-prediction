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
        subprocess.run(["python", "scripts/save_last_update.py"])


if __name__ == "__main__":
    main()
