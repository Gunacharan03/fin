import { Box, Heading } from "@chakra-ui/react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

export default function ExpenseChart({ data = [] }) {
  return (
    <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
      <Heading size="sm" mb={4} fontFamily="heading">Monthly Expense Trend</Heading>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8E6DF" />
          <XAxis dataKey="month" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Bar dataKey="expense" fill="#D14B3D" radius={[4, 4, 0, 0]} name="Expense" />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}
