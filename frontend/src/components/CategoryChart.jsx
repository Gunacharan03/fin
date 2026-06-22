import { Box, Heading } from "@chakra-ui/react";
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const COLORS = ["#1F3A6B", "#C2891A", "#D14B3D", "#3A5BA0", "#E0A726", "#E5685B", "#15294E", "#9A6B12"];

export default function CategoryChart({ data = [] }) {
  return (
    <Box bg="white" p={5} borderRadius="12px" border="1px solid" borderColor="surface.200">
      <Heading size="sm" mb={4} fontFamily="heading">Spending by Category</Heading>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="total"
            nameKey="category"
            cx="50%"
            cy="50%"
            outerRadius={95}
            label={({ category, percent }) => `${category} ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Box>
  );
}
