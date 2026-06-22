import { useEffect, useState } from "react";
import {
  Box, SimpleGrid, Heading, Text, Stat, StatLabel, StatNumber, StatHelpText,
  VStack, HStack, Badge, CircularProgress, CircularProgressLabel, Center,
} from "@chakra-ui/react";
import { useAuth } from "../context/AuthContext";
import { analyticsService } from "../services/aiService";
import LoadingSpinner from "../components/LoadingSpinner";
import IncomeChart from "../components/IncomeChart";
import CategoryChart from "../components/CategoryChart";
import TransactionCard from "../components/TransactionCard";

const CURRENCY_SYMBOLS = { INR: "₹", USD: "$", EUR: "€", GBP: "£" };

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const currency = CURRENCY_SYMBOLS[user?.currency] || "₹";

  useEffect(() => {
    async function load() {
      try {
        const result = await analyticsService.getDashboard();
        setData(result);
      } catch (err) {
        setError("Could not load dashboard data.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <LoadingSpinner label="Loading your dashboard..." />;
  if (error) return <Text color="danger.500">{error}</Text>;

  const { summary, category_breakdown, monthly_trend, recent_transactions } = data;
  const scoreColor = summary.financial_health_score >= 70 ? "positive.500" : summary.financial_health_score >= 40 ? "orange.400" : "danger.500";

  return (
    <VStack align="stretch" spacing={6}>
      <Box>
        <Heading size="lg" fontFamily="heading">Welcome back, {user?.name?.split(" ")[0]}</Heading>
        <Text color="gray.500" fontSize="sm">Here's how your money is doing</Text>
      </Box>

      <SimpleGrid columns={{ base: 1, sm: 2, lg: 4 }} spacing={4}>
        <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
          <Stat>
            <StatLabel color="gray.500" fontSize="xs">Total Income</StatLabel>
            <StatNumber fontFamily="heading" color="positive.600">{currency}{summary.total_income.toLocaleString()}</StatNumber>
          </Stat>
        </Box>
        <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
          <Stat>
            <StatLabel color="gray.500" fontSize="xs">Total Expense</StatLabel>
            <StatNumber fontFamily="heading" color="danger.500">{currency}{summary.total_expense.toLocaleString()}</StatNumber>
          </Stat>
        </Box>
        <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
          <Stat>
            <StatLabel color="gray.500" fontSize="xs">Net Savings</StatLabel>
            <StatNumber fontFamily="heading" color="brand.500">{currency}{summary.net_savings.toLocaleString()}</StatNumber>
            <StatHelpText fontSize="xs" mb={0}>{summary.savings_rate_percent}% savings rate</StatHelpText>
          </Stat>
        </Box>
        <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
          <HStack justify="space-between">
            <Box>
              <Text fontSize="xs" color="gray.500" mb={1}>Financial Health</Text>
              <Badge colorScheme={summary.financial_health_score >= 70 ? "yellow" : summary.financial_health_score >= 40 ? "orange" : "red"}>
                {summary.financial_health_score >= 70 ? "Strong" : summary.financial_health_score >= 40 ? "Fair" : "Needs attention"}
              </Badge>
            </Box>
            <CircularProgress value={summary.financial_health_score} color={scoreColor} size="50px">
              <CircularProgressLabel fontSize="xs" fontWeight={700}>{summary.financial_health_score}</CircularProgressLabel>
            </CircularProgress>
          </HStack>
        </Box>
      </SimpleGrid>

      <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={5}>
        <IncomeChart data={monthly_trend} />
        <CategoryChart data={category_breakdown} />
      </SimpleGrid>

      <Box>
        <Heading size="md" fontFamily="heading" mb={3}>Recent Transactions</Heading>
        {recent_transactions.length === 0 ? (
          <Center bg="white" py={8} borderRadius="12px" border="1px solid" borderColor="surface.200">
            <Text color="gray.500" fontSize="sm">No transactions yet. Add your first one to get started.</Text>
          </Center>
        ) : (
          <VStack align="stretch" spacing={2}>
            {recent_transactions.map((t) => (
              <TransactionCard key={t.id} transaction={t} currency={currency} />
            ))}
          </VStack>
        )}
      </Box>
    </VStack>
  );
}
