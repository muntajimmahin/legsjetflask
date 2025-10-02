import flyvictor
import aircharter
import privatelegs
import globeair
import jettly
import logging

logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def run_all():
    # flyvictor.run()
    globeair.run()
    # aircharter.run()
    # privatelegs.run()
    # globeair.run()



if __name__ == "__main__":
    logging.info("Starting scraper")
    run_all()
    logging.info("Finished scraper")

