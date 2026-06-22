import { useState } from "react";
import {
  Box, Button, FormControl, FormLabel, Input, VStack, Heading,
  Text, Alert, AlertIcon, Center, Link as ChakraLink, Select,
} from "@chakra-ui/react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "", email: "", password: "", monthly_income: "", currency: "INR",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register({ ...form, monthly_income: parseFloat(form.monthly_income) || 0 });
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Center minH="100vh" bg="surface.50" py={10}>
      <Box bg="white" p={8} borderRadius="14px" boxShadow="md" w="100%" maxW="440px">
        <Heading size="lg" fontFamily="heading" color="brand.500" mb={1}>
          Create your account
        </Heading>
        <Text color="gray.500" mb={6} fontSize="sm">
          Start tracking smarter, today
        </Text>

        {error && (
          <Alert status="error" borderRadius="8px" mb={4} fontSize="sm">
            <AlertIcon />
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <VStack spacing={4}>
            <FormControl isRequired>
              <FormLabel fontSize="sm">Full name</FormLabel>
              <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Jane Doe" />
            </FormControl>
            <FormControl isRequired>
              <FormLabel fontSize="sm">Email</FormLabel>
              <Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="you@example.com" />
            </FormControl>
            <FormControl isRequired>
              <FormLabel fontSize="sm">Password</FormLabel>
              <Input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="At least 6 characters" />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Monthly income (optional)</FormLabel>
              <Input type="number" value={form.monthly_income} onChange={(e) => setForm({ ...form, monthly_income: e.target.value })} placeholder="0" />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Currency</FormLabel>
              <Select value={form.currency} onChange={(e) => setForm({ ...form, currency: e.target.value })}>
                <option value="INR">INR (₹)</option>
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </Select>
            </FormControl>
            <Button type="submit" colorScheme="blue" w="100%" isLoading={loading}>
              Create account
            </Button>
          </VStack>
        </form>

        <Text fontSize="sm" color="gray.500" mt={5} textAlign="center">
          Already have an account?{" "}
          <ChakraLink as={Link} to="/login" color="brand.500" fontWeight={600}>
            Log in
          </ChakraLink>
        </Text>
      </Box>
    </Center>
  );
}
