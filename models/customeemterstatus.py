from dataclasses import dataclass


@dataclass
class CustomEmeterStatus:
    voltage_mv: int
    power_mw: int
    current_ma: int
    total_wh: int
    today_kwh: float
    this_month_kwh: float
