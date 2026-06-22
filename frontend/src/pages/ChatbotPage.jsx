import { useState, useRef, useEffect } from "react";
import {
  VStack, HStack, Heading, Text, Box, Input, Button, Flex, Avatar, useToast,
} from "@chakra-ui/react";
import { FiSend, FiMessageCircle } from "react-icons/fi";
import { aiService } from "../services/aiService";
import { useAuth } from "../context/AuthContext";

const STARTER_PROMPTS = [
  "How am I doing financially this month?",
  "Where can I cut back on spending?",
  "Can I afford a ₹20,000 purchase right now?",
];

export default function ChatbotPage() {
  const { user } = useAuth();
  const toast = useToast();
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! I'm your financial advisor. Ask me anything about your spending, savings, or goals." },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef();

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text) => {
    const messageText = text || input;
    if (!messageText.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: messageText }]);
    setInput("");
    setSending(true);

    try {
      const res = await aiService.sendChatMessage(messageText);
      setMessages((prev) => [...prev, { role: "assistant", content: res.content }]);
    } catch (err) {
      toast({ title: "Message failed to send", status: "error", duration: 3000 });
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, something went wrong. Please try again." }]);
    } finally {
      setSending(false);
    }
  };

  return (
    <VStack align="stretch" spacing={4} h="calc(100vh - 140px)">
      <Box>
        <Heading size="lg" fontFamily="heading" mb={1}>Advisor Chat</Heading>
        <Text color="gray.500" fontSize="sm">Grounded in your real income, spending, and goals.</Text>
      </Box>

      <Box flex={1} bg="white" borderRadius="12px" border="1px solid" borderColor="surface.200" p={4} overflowY="auto">
        <VStack align="stretch" spacing={4}>
          {messages.map((m, i) => (
            <Flex key={i} justify={m.role === "user" ? "flex-end" : "flex-start"}>
              <HStack align="flex-start" maxW="75%" spacing={2} flexDir={m.role === "user" ? "row-reverse" : "row"}>
                <Avatar
                  size="xs"
                  name={m.role === "user" ? user?.name : "AI Advisor"}
                  bg={m.role === "user" ? "brand.500" : "positive.500"}
                  color="white"
                  icon={m.role === "assistant" ? <FiMessageCircle /> : undefined}
                />
                <Box
                  bg={m.role === "user" ? "brand.500" : "surface.100"}
                  color={m.role === "user" ? "white" : "brand.900"}
                  px={4}
                  py={2.5}
                  borderRadius="12px"
                  fontSize="sm"
                  whiteSpace="pre-line"
                >
                  {m.content}
                </Box>
              </HStack>
            </Flex>
          ))}
          {sending && (
            <Flex justify="flex-start">
              <Box bg="surface.100" px={4} py={2.5} borderRadius="12px" fontSize="sm" color="gray.500">
                Thinking...
              </Box>
            </Flex>
          )}
          <div ref={scrollRef} />
        </VStack>
      </Box>

      {messages.length <= 1 && (
        <HStack wrap="wrap" spacing={2}>
          {STARTER_PROMPTS.map((p) => (
            <Button key={p} size="sm" variant="outline" onClick={() => sendMessage(p)}>
              {p}
            </Button>
          ))}
        </HStack>
      )}

      <HStack>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask about your finances..."
          bg="white"
        />
        <Button leftIcon={<FiSend />} colorScheme="blue" onClick={() => sendMessage()} isLoading={sending}>
          Send
        </Button>
      </HStack>
    </VStack>
  );
}
