from .utils import RoboEpik, Config
from EpikCord import Intents


if __name__ == "__main__":
    RoboEpik(Config.token, Intents().all).login()