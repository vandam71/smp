__author__ = "Rafael Samorinha"
__version__ = "1.0.0"

import firebase_admin
from firebase_admin import credentials


def main():
    cred = credentials.Certificate("configs/smp-2020r-firebase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smp-2020r.firebaseio.com'
    })


if __name__ == '__main__':
    main()
