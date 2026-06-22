import { useState } from "react";
import {
  Box, Button, FormControl, FormLabel, Input, VStack, Heading,
  Select, Textarea, Switch, HStack, Text, Alert, AlertIcon,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { transactionService } from "../services/transactionService";

const EXPENSE_CATEGORIES = [
  "Food", "Groceries", "Rent", "Utilities", "Transport", "Fuel",
  "Shopping", "Entertainment", "Healthcare", "Education", "EMI",
  "Insurance", "Subscriptions", "Travel", "Investment", "Other",
];
const INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment Returns", "Gift", "Other"];

export default function AddTransactionPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    type: "expense",
    amount: "",
    category: "",
    description: "",
    date: new Date().toISOString().slice(0, 10),
    is_recurring: false,
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const categories = form.type === "income" ? INCOME_CATEGORIES : EXPENSE_CATEGORIES;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!form.category) {
      setError("Please select a category.");
      return;
    }
    setLoading(true);
    try {
      await transactionService.create({ ...form, amount: parseFloat(form.amount) });
      navigate("/transactions");
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save transaction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="520px">
      <Heading size="lg" fontFamily="heading" mb={1}>Add Transaction</Heading>
      <Text color="gray.500" fontSize="sm" mb={6}>Record a new income or expense entry</Text>

      {error && (
        <Alert status="error" borderRadius="8px" mb={4} fontSize="sm">
          <AlertIcon />
          {error}
        </Alert>
      )}

      <Box bg="white" p={6} borderRadius="12px" border="1px solid" borderColor="surface.200">
        <form onSubmit={handleSubmit}>
          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel fontSize="sm">Type</FormLabel>
              <HStack>
                <Button
                  flex={1}
                  variant={form.type === "expense" ? "solid" : "outline"}
                  colorScheme="red"
                  onClick={() => setForm({ ...form, type: "expense", category: "" })}
                >
                  Expense
                </Button>
                <Button
                  flex={1}
                  variant={form.type === "income" ? "solid" : "outline"}
                  colorScheme="yellow"
                  onClick={() => setForm({ ...form, type: "income", category: "" })}
                >
                  Income
                </Button>
              </HStack>
            </FormControl>

            <FormControl isRequired>
              <FormLabel fontSize="sm">Amount</FormLabel>
              <Input type="number" step="0.01" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} placeholder="0.00" />
            </FormControl>

            <FormControl isRequired>
              <FormLabel fontSize="sm">Category</FormLabel>
              <Select placeholder="Select category" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {categories.map((c) => <option key={c} value={c}>{c}</option>)}
              </Select>
            </FormControl>

            <FormControl>
              <FormLabel fontSize="sm">Description (optional)</FormLabel>
              <Textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="e.g. Dinner with friends" rows={2} />
            </FormControl>

            <FormControl isRequired>
              <FormLabel fontSize="sm">Date</FormLabel>
              <Input type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} />
            </FormControl>

            <FormControl display="flex" alignItems="center">
              <FormLabel fontSize="sm" mb={0}>Recurring transaction</FormLabel>
              <Switch isChecked={form.is_recurring} onChange={(e) => setForm({ ...form, is_recurring: e.target.checked })} />
            </FormControl>

            <Button type="submit" colorScheme="blue" isLoading={loading} mt={2}>
              Save transaction
            </Button>
          </VStack>
        </form>
      </Box>
    </Box>
  );
}
