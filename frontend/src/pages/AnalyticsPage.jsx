import { useEffect, useState } from "react";
import { VStack, HStack, Heading, Select, SimpleGrid, Text } from "@chakra-ui/react";
import { analyticsService } from "../services/aiService";
import IncomeChart from "../components/IncomeChart";
import ExpenseChart from "../components/ExpenseChart";
import CategoryChart from "../components/CategoryChart";
import LoadingSpinner from "../components/LoadingSpinner";

export default function AnalyticsPage() {
  const [trend, setTrend] = useState([]);
  const [expenseCategories, setExpenseCategories] = useState([]);
  const [incomeCategories, setIncomeCategories] = useState([]);
  const [months, setMonths] = useState(6);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const [trendData, expenseData, incomeData] = await Promise.all([
          analyticsService.getMonthlyTrend(months),
          analyticsService.getCategoryBreakdown("expense"),
          analyticsService.getCategoryBreakdown("income"),
        ]);
        setTrend(trendData);
        setExpenseCategories(expenseData);
        setIncomeCategories(incomeData);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [months]);

  if (loading) return <LoadingSpinner label="Crunching the numbers..." />;

  return (
    <VStack align="stretch" spacing={6}>
      <HStack justify="space-between">
        <Heading size="lg" fontFamily="heading">Analytics</Heading>
        <Select w="180px" value={months} onChange={(e) => setMonths(parseInt(e.target.value))}>
          <option value={3}>Last 3 months</option>
          <option value={6}>Last 6 months</option>
          <option value={12}>Last 12 months</option>
        </Select>
      </HStack>

      <IncomeChart data={trend} />
      <ExpenseChart data={trend} />

      <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={5}>
        {expenseCategories.length > 0 ? (
          <CategoryChart data={expenseCategories} />
        ) : (
          <Text color="gray.500" fontSize="sm">No expense data yet.</Text>
        )}
        {incomeCategories.length > 0 && <CategoryChart data={incomeCategories} />}
      </SimpleGrid>
    </VStack>
  );
}
