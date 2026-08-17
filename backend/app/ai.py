from statistics import mean
class MockProvider:
    def execute(self, prompt, data):
        rows = data.get("rows", []) if isinstance(data, dict) else []
        values = [float(r.get("revenue", r.get("value", 0))) for r in rows if isinstance(r, dict)]
        total = round(sum(values), 2); avg = round(mean(values), 2) if values else 0
        finding = f"Revenue totals {total:,.0f} across {len(values)} observations, averaging {avg:,.0f}." if values else "The operational signal indicates manual repetition and uneven performance."
        return {"plan": ["Validate supplied business inputs", "Calculate performance signals", "Prioritize actionable opportunity"], "tool_calls": ["data_analysis", "business_kpi", "recommendation"], "response": f"{finding} Focus on the lowest-performing segment, automate the recurring reporting step, and review results weekly.", "metrics": {"total": total, "average": avg}}
