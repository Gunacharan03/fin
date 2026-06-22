import { createContext, useContext, useState, useCallback } from "react";
import { analyticsService } from "../services/aiService";

const FinanceContext = createContext(null);

export function FinanceProvider({ children }) {
  const [dashboard, setDashboard] = useState(null);
  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [refreshFlag, setRefreshFlag] = useState(0);

  const loadDashboard = useCallback(async () => {
    setDashboardLoading(true);
    try {
      const data = await analyticsService.getDashboard();
      setDashboard(data);
      return data;
    } finally {
      setDashboardLoading(false);
    }
  }, []);

  // Call this after creating/editing/deleting a transaction, goal, or reminder
  // so any screen listening to refreshFlag knows to refetch.
  const triggerRefresh = useCallback(() => {
    setRefreshFlag((f) => f + 1);
  }, []);

  return (
    <FinanceContext.Provider
      value={{ dashboard, dashboardLoading, loadDashboard, refreshFlag, triggerRefresh }}
    >
      {children}
    </FinanceContext.Provider>
  );
}

export function useFinance() {
  const ctx = useContext(FinanceContext);
  if (!ctx) throw new Error("useFinance must be used within a FinanceProvider");
  return ctx;
}
