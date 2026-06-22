import { Box, Heading } from "@chakra-ui/react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

export default function IncomeChart({ data = [] }) {
  return (
    <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
      <Heading size="sm" mb={4} fontFamily="heading">Income vs Expense Trend</Heading>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8E6DF" />
          <XAxis dataKey="month" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="income" stroke="#C2891A" strokeWidth={2} name="Income" />
          <Line type="monotone" dataKey="expense" stroke="#D14B3D" strokeWidth={2} name="Expense" />
          <Line type="monotone" dataKey="net" stroke="#1F3A6B" strokeWidth={2} strokeDasharray="4 2" name="Net" />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
}
