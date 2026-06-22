import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LoadingSpinner from "../components/LoadingSpinner";

export default function HomePage() {
  const { user, loading } = useAuth();

  if (loading) return <LoadingSpinner label="Loading Fin..." />;
  return <Navigate to={user ? "/dashboard" : "/login"} replace />;
}
