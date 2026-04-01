from sqlalchemy import String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctpc.models.base import Base


class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    synonyms: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )

    evidence_rows = relationship(
        "DiseaseTargetEvidence", back_populates="disease", cascade="all, delete-orphan"
    )
