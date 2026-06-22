import { useState } from "react";
import { Box, Button, FormControl, FormLabel, Input, VStack, Heading, Text, Textarea, Alert, AlertIcon } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { goalService } from "../services/goalService";

export default function AddGoalPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: "", target_amount: "", current_amount: "0", target_date: "", notes: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await goalService.create({
        ...form,
        target_amount: parseFloat(form.target_amount),
        current_amount: parseFloat(form.current_amount) || 0,
        target_date: form.target_date || null,
      });
      navigate("/goals");
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create goal.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="520px">
      <Heading size="lg" fontFamily="heading" mb={1}>New Savings Goal</Heading>
      <Text color="gray.500" fontSize="sm" mb={6}>e.g. "Save ₹60,000 for a laptop"</Text>

      {error && (
        <Alert status="error" borderRadius="8px" mb={4} fontSize="sm">
          <AlertIcon />
          {error}
        </Alert>
      )}

      <Box bg="white" p={6} borderRadius="12px" border="1px solid" borderColor="surface.200">
        <form onSubmit={handleSubmit}>
          <VStack spacing={4} align="stretch">
            <FormControl isRequired>
              <FormLabel fontSize="sm">Goal title</FormLabel>
              <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="e.g. New Laptop" />
            </FormControl>
            <FormControl isRequired>
              <FormLabel fontSize="sm">Target amount</FormLabel>
              <Input type="number" value={form.target_amount} onChange={(e) => setForm({ ...form, target_amount: e.target.value })} placeholder="60000" />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Already saved (optional)</FormLabel>
              <Input type="number" value={form.current_amount} onChange={(e) => setForm({ ...form, current_amount: e.target.value })} placeholder="0" />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Target date (optional)</FormLabel>
              <Input type="date" value={form.target_date} onChange={(e) => setForm({ ...form, target_date: e.target.value })} />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Notes (optional)</FormLabel>
              <Textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} rows={2} />
            </FormControl>
            <Button type="submit" colorScheme="blue" isLoading={loading} mt={2}>
              Create goal
            </Button>
          </VStack>
        </form>
      </Box>
    </Box>
  );
}
