import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import api from "../services/api.js";
import { supabase } from "../lib/supabase.js";

const AuthContext = createContext(null);
export const ADMIN_ACCESS_ERROR = "This account is not an authorized administrator.";

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState("");

  const loadProfile = useCallback(async () => {
    try {
      const response = await api.get("/auth/me");
      setProfile(response.data);
      setAuthError("");
      return response.data;
    } catch (error) {
      if (error.response?.status === 403) {
        setAuthError(ADMIN_ACCESS_ERROR);
        setProfile(null);
        await supabase?.auth.signOut();
      } else {
        setProfile(null);
        setAuthError(error.apiError?.message || "Unable to load your administrator profile.");
      }
      return null;
    }
  }, []);

  useEffect(() => {
    if (!supabase) {
      setLoading(false);
      setAuthError("Authentication is not configured. Set the VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY environment variables.");
      return undefined;
    }
    let active = true;
    const hydrate = async (nextSession) => {
      if (!active) return;
      setSession(nextSession);
      if (nextSession) await loadProfile();
      else setProfile(null);
      if (active) setLoading(false);
    };
    supabase.auth.getSession().then(({ data }) => hydrate(data.session));
    const { data: listener } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession);
      if (!nextSession) {
        setProfile(null);
        setLoading(false);
      } else {
        // Defer API work until after the Supabase auth callback completes.
        window.setTimeout(() => { if (active) loadProfile().finally(() => setLoading(false)); }, 0);
      }
    });
    return () => {
      active = false;
      listener.subscription.unsubscribe();
    };
  }, [loadProfile]);

  const signIn = useCallback(async (email, password) => {
    if (!supabase) throw new Error("Authentication is not configured.");
    setAuthError("");
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    setSession(data.session);
    const nextProfile = await loadProfile();
    if (!nextProfile) {
      await supabase.auth.signOut();
      throw new Error(ADMIN_ACCESS_ERROR);
    }
    return nextProfile;
  }, [loadProfile]);

  const signOut = useCallback(async () => {
    if (supabase) {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
    }
    setSession(null);
    setProfile(null);
  }, []);

  const resetPassword = useCallback(async (email) => {
    if (!supabase) throw new Error("Authentication is not configured.");
    const redirectTo = `${window.location.origin}/login`;
    const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo });
    if (error) throw error;
  }, []);

  const value = useMemo(() => ({ session, profile, loading, authError, signIn, signOut, resetPassword, refreshProfile: loadProfile }),
    [session, profile, loading, authError, signIn, signOut, resetPassword, loadProfile]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
