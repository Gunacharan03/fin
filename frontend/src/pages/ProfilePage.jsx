import { useState } from "react";
import {
  Box, VStack, HStack, Heading, Text, FormControl, FormLabel, Input,
  Select, Button, Divider, Alert, AlertIcon, useToast,
} from "@chakra-ui/react";
import { useAuth } from "../context/AuthContext";
import { authService } from "../services/authService";

export default function ProfilePage() {
  const { user, refreshProfile } = useAuth();
  const toast = useToast();

  const [profileForm, setProfileForm] = useState({
    name: user?.name || "",
    monthly_income: user?.monthly_income || 0,
    currency: user?.currency || "INR",
  });
  const [passwordForm, setPasswordForm] = useState({ current_password: "", new_password: "" });
  const [profileError, setProfileError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [savingProfile, setSavingProfile] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setProfileError("");
    setSavingProfile(true);
    try {
      await authService.updateProfile({
        ...profileForm,
        monthly_income: parseFloat(profileForm.monthly_income) || 0,
      });
      await refreshProfile();
      toast({ title: "Profile updated", status: "success", duration: 2000 });
    } catch (err) {
      setProfileError(err.response?.data?.detail || "Could not update profile.");
    } finally {
      setSavingProfile(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordError("");
    setSavingPassword(true);
    try {
      await authService.changePassword(passwordForm);
      setPasswordForm({ current_password: "", new_password: "" });
      toast({ title: "Password changed", status: "success", duration: 2000 });
    } catch (err) {
      setPasswordError(err.response?.data?.detail || "Could not change password.");
    } finally {
      setSavingPassword(false);
    }
  };

  return (
    <VStack align="stretch" spacing={6} maxW="560px">
      <Box>
        <Heading size="lg" fontFamily="heading" mb={1}>Profile</Heading>
        <Text color="gray.500" fontSize="sm">{user?.email}</Text>
      </Box>

      <Box bg="white" p={6} borderRadius="12px" border="1px solid" borderColor="surface.200">
        <Heading size="sm" mb={4} fontFamily="heading">Account details</Heading>
        {profileError && (
          <Alert status="error" borderRadius="8px" mb={4} fontSize="sm">
            <AlertIcon />{profileError}
          </Alert>
        )}
        <form onSubmit={handleProfileSubmit}>
          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel fontSize="sm">Full name</FormLabel>
              <Input value={profileForm.name} onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })} />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Monthly income</FormLabel>
              <Input type="number" value={profileForm.monthly_income} onChange={(e) => setProfileForm({ ...profileForm, monthly_income: e.target.value })} />
            </FormControl>
            <FormControl>
              <FormLabel fontSize="sm">Currency</FormLabel>
              <Select value={profileForm.currency} onChange={(e) => setProfileForm({ ...profileForm, currency: e.target.value })}>
                <option value="INR">INR (₹)</option>
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </Select>
            </FormControl>
            <Button type="submit" colorScheme="blue" isLoading={savingProfile} alignSelf="flex-start">
              Save changes
            </Button>
          </VStack>
        </form>
      </Box>

      <Box bg="white" p={6} borderRadius="12px" border="1px solid" borderColor="surface.200">
        <Heading size="sm" mb={4} fontFamily="heading">Change password</Heading>
        {passwordError && (
          <Alert status="error" borderRadius="8px" mb={4} fontSize="sm">
            <AlertIcon />{passwordError}
          </Alert>
        )}
        <form onSubmit={handlePasswordSubmit}>
          <VStack spacing={4} align="stretch">
            <FormControl isRequired>
              <FormLabel fontSize="sm">Current password</FormLabel>
              <Input type="password" value={passwordForm.current_password} onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })} />
            </FormControl>
            <FormControl isRequired>
              <FormLabel fontSize="sm">New password</FormLabel>
              <Input type="password" value={passwordForm.new_password} onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })} />
            </FormControl>
            <Button type="submit" colorScheme="blue" isLoading={savingPassword} alignSelf="flex-start">
              Update password
            </Button>
          </VStack>
        </form>
      </Box>
    </VStack>
  );
}
