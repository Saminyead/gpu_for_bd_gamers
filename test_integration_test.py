from data_coll_script import main

import os
import dotenv

dotenv.load_dotenv("test.env")
test_db_url = os.getenv("test_db_url")

def test_main(
        test_db_url:str = test_db_url
    ):
    """Directly tests main on a test database"""
    main(test_db_url)

    # tests we want to run:
    # - pull the tables (list them later), make sure none of them
    #   are empty