"""This module contains the database connection tools."""

import argparse

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.schema import Base


class DBConnection:
    """Initialize database, metadata and sessions."""

    def __init__(self, db_path: str):
        """Initialize the database and engine.

        Args:
            db_path (str): path to sqlite databse
        """
        self.db_path = Path(db_path)
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=True)
        if not self.db_path.exists():
            Base.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        """Create a database connection session.

        Returns:
            Session: database connection session
        """
        session = Session(self.engine)

        return session


# This will create a memory only sqllite database


# from sqlalchemy.orm import Session

# with Session(engine) as session:
#     spongebob = User(
#         name="spongebob",
#         fullname="Spongebob Squarepants",
#         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#     )
#     session.add_all([spongebob, sandy, patrick])
#     session.commit()


def main(args):
    """Execute database script.

    Args:
        args (Namespace): argparse namespace from command line arguments
    """
    db_path = args.path
    db_conn = DBConnection(db_path)
    session = db_conn.create_session()
    print(session)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True)
    args = parser.parse_args()
    main(args)
