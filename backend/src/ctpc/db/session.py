from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from ctpc.db.models import Base


SCHEMAS = ("raw", "core", "marts", "ops", "experimental")


class DatabaseManager:
    def __init__(self, engine: Engine, schema_paths: dict[str, str] | None = None) -> None:
        self.engine = engine
        self.schema_paths = schema_paths or {}
        self.session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    @classmethod
    def for_sqlite(cls, path: Path) -> "DatabaseManager":
        path.parent.mkdir(parents=True, exist_ok=True)
        schema_paths = {
            schema: str(path.with_name(f"{path.stem}-{schema}.db"))
            for schema in SCHEMAS
        }
        engine = create_engine(
            f"sqlite+pysqlite:///{path}",
            future=True,
            connect_args={"check_same_thread": False},
        )
        _register_sqlite_schema_attach(engine, schema_paths)
        return cls(engine, schema_paths)

    @classmethod
    def for_memory(cls) -> "DatabaseManager":
        schema_paths = {schema: ":memory:" for schema in SCHEMAS}
        engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            future=True,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        _register_sqlite_schema_attach(engine, schema_paths)
        return cls(engine, schema_paths)

    @classmethod
    def from_url(cls, database_url: str) -> "DatabaseManager":
        if database_url.startswith("sqlite"):
            if database_url.endswith(":memory:"):
                return cls.for_memory()
            if ":///" in database_url:
                return cls.for_sqlite(Path(database_url.split(":///", maxsplit=1)[1]))
        engine = create_engine(database_url, future=True)
        return cls(engine)

    def create_all(self) -> None:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Session:
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def _register_sqlite_schema_attach(engine: Engine, schema_paths: dict[str, str]) -> None:
    @event.listens_for(engine, "connect")
    def _attach_schemas(dbapi_connection, _connection_record) -> None:  # type: ignore[no-untyped-def]
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        for schema, schema_path in schema_paths.items():
            cursor.execute(f"ATTACH DATABASE '{schema_path}' AS {schema}")
        cursor.close()
