from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_runs: int
    success_rate: float
    avg_runtime_seconds: int
    active_runs: int


class DailyTrendItem(BaseModel):
    date: str
    runs: int
    success_rate: float


class DashboardTrendsResponse(BaseModel):
    daily: list[DailyTrendItem]
