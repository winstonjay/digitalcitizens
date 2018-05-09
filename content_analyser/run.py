# -*- coding: utf-8 -*-
'''
run.py
run the flask webserver for our app. Taking file arguements.
'''
import argparse
from app import app


from config import Options



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db", type=str, default="session.pkl",
        help="filepath for saving progress")
    parser.add_argument(
        "--book", type=str, required=True,
        help="input configurations for the interface. ('codebook')")
    parser.add_argument(
        "--content", type=str, required=True,
        help="path to the content to analise")
    args = parser.parse_args()

    options = Options(args)
    app.config.update(options.__dict__)

    app.run()