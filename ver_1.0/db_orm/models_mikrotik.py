from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from .base import BaseMikrotik

#create DB, tables
class DhcpTableOrm(BaseMikrotik):
    __tablename__ = 'dhcp_table'
    id = Column(Integer, primary_key=True)
    ip = Column(String, unique=True, nullable=False)
    mac_address = Column(String, nullable=False)
    host_name = Column(String)
    age = Column(String)
    dynamic = Column(Boolean)
    last_seen = Column(String)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # traffic_records = relationship("TrafficTableOrm", back_populates="dhcp_records")

class DhcpHistoryTableOrm(BaseMikrotik):
    __tablename__ = "dhcp_history_table"
    id = Column(Integer, primary_key=True)
    ip = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    host_name = Column(String)
    dynamic = Column(Boolean)
    removed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class TrafficTableOrm(BaseMikrotik):
    __tablename__ = 'traffic_table'
    id = Column(Integer, primary_key=True)
    # dhcp_table_id = Column(Integer, ForeignKey("dhcp_table.id", ondelete="SET NULL"), nullable=True)
    ip = Column(String, nullable=False)
    name = Column(String, nullable=False)
    rx_Mbytes = Column(Integer)
    tx_Mbytes = Column(Integer)
    updated_at = Column(DateTime, default=func.current_timestamp())

    # dhcp_records = relationship("DhcpTableOrm", back_populates="traffic_records")

