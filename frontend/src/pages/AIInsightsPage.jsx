import { useState } from "react";
import {
  VStack, HStack, Heading, Text, Button, Box, SimpleGrid,
  CircularProgress, CircularProgressLabel, useToast,
} from "@chakra-ui/react";
import { FiTrendingUp, FiTarget, FiBell, FiFileText, FiZap } from "react-icons/fi";
import { FaPiggyBank } from "react-icons/fa";
import { aiService } from "../services/aiService";
import AIInsightCard from "../components/AIInsightCard";
import LoadingSpinner from "../components/LoadingSpinner";

export default function AIInsightsPage() {
  const toast = useToast();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [healthScore, setHealthScore] = useState(null);

  const runFullReport = async () => {
    setLoading(true);
    try {
      const [fullReport, score] = await Promise.all([
        aiService.getFullReport(),
        aiService.getFinancialHealthScore(),
      ]);
      setReport(fullReport);
      setHealthScore(score);
    } catch (err) {
      toast({
        title: "Could not generate insights",
        description: err.response?.data?.detail || "Please check your Gemini API key is configured on the backend.",
        status: "error",
        duration: 5000,
      });
    } finally {
      setLoading(false);
    }
  };

  const scoreColor = (s) => (s >= 70 ? "#C2891A" : s >= 40 ? "#E5A93A" : "#D14B3D");

  return (
    <VStack align="stretch" spacing={6}>
      <HStack justify="space-between" wrap="wrap">
        <Box>
          <Heading size="lg" fontFamily="heading" mb={1}>AI Insights</Heading>
          <Text color="gray.500" fontSize="sm">
            Multi-agent analysis of your finances — expense patterns, savings, goals, and bills.
          </Text>
        </Box>
        <Button leftIcon={<FiZap />} colorScheme="blue" onClick={runFullReport} isLoading={loading}>
          {report ? "Refresh insights" : "Generate insights"}
        </Button>
      </HStack>

      {loading && <LoadingSpinner label="Running expense, savings, goal, reminder & advisor agents..." />}

      {!loading && !report && (
        <Box bg="white" py={12} borderRadius="12px" border="1px solid" borderColor="surface.200" textAlign="center">
          <Text color="gray.500">Click "Generate insights" to run the full AI agent pipeline on your data.</Text>
        </Box>
      )}

      {!loading && report && (
        <>
          {healthScore && (
            <Box bg="white" p={6} borderRadius="12px" border="1px solid" borderColor="surface.200">
              <HStack justify="space-between" wrap="wrap" spacing={6}>
                <Box>
                  <Text fontSize="sm" color="gray.500" mb={1}>Financial Health Score</Text>
                  <Text fontSize="sm" color="gray.600">
                    Based on savings rate, spending ratio, and bill payment discipline.
                  </Text>
                </Box>
                <CircularProgress value={healthScore.score} color={scoreColor(healthScore.score)} size="90px" thickness="8px">
                  <CircularProgressLabel fontWeight={700} fontSize="lg">{healthScore.score}</CircularProgressLabel>
                </CircularProgress>
              </HStack>
            </Box>
          )}

          <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={4}>
            {report.expense_analysis && (
              <AIInsightCard title="Expense Analysis" icon={FiTrendingUp} accentColor="brand.500" content={report.expense_analysis.analysis_text} />
            )}
            {report.savings_recommendation && (
              <AIInsightCard title="Savings Recommendation" icon={FaPiggyBank} accentColor="positive.500" content={report.savings_recommendation.recommendation_text} />
            )}
            {report.goal_prediction && (
              <AIInsightCard title="Goal Predictions" icon={FiTarget} accentColor="brand.400" content={report.goal_prediction.narrative} />
            )}
            {report.reminder_alert && (
              <AIInsightCard title="Bills & Reminders" icon={FiBell} accentColor="danger.500" content={report.reminder_alert.narrative} />
            )}
          </SimpleGrid>

          {report.advisor_report && (
            <AIInsightCard title="Monthly Financial Report" icon={FiFileText} accentColor="brand.600" content={report.advisor_report.report_text} />
          )}
        </>
      )}
    </VStack>
  );
}
