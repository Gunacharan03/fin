import { useState } from "react";
import {
  Box, Button, FormControl, FormLabel, Input, VStack, Heading,
  Text, Alert, AlertIcon, Center, Link as ChakraLink,
} from "@chakra-ui/react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(form);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Center minH="100vh" bg="surface.50">
      <Box bg="white" p={8} borderRadius="14px" boxShadow="md" w="100%" maxW="420px">
        <Heading size="lg" fontFamily="heading" color="brand.500" mb={1}>
          Welcome back
        </Heading>
        <Text color="gray.500" mb={6} fontSize="sm">
          Log in to Fin
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
              <FormLabel fontSize="sm">Email</FormLabel>
              <Input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="you@example.com"
              />
            </FormControl>
            <FormControl isRequired>
              <FormLabel fontSize="sm">Password</FormLabel>
              <Input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="••••••••"
              />
            </FormControl>
            <Button type="submit" colorScheme="blue" w="100%" isLoading={loading}>
              Log in
            </Button>
          </VStack>
        </form>

        <Text fontSize="sm" color="gray.500" mt={5} textAlign="center">
          New here?{" "}
          <ChakraLink as={Link} to="/register" color="brand.500" fontWeight={600}>
            Create an account
          </ChakraLink>
        </Text>
      </Box>
    </Center>
  );
}
