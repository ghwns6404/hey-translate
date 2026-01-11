import logging
import os
import sys
from ui.app import App

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logging.getLogger('deepl').setLevel(logging.WARNING)
    if os.getenv("APP_DEBUG"):
        logger.setLevel(logging.DEBUG)

    app = App(logger)
    app.mainloop()
