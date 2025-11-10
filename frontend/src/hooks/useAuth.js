import { useState, useEffect } from "react";

const TOKEN_KEY = "fixhub_token";

export default function useAuth() {
  const [token, setTokenState] = useState(localStorage.getItem(TOKEN_KEY));

  const setToken = (t) => {
    if (!t) {
      localStorage.removeItem(TOKEN_KEY);
      setTokenState(null);
    } else {
      localStorage.setItem(TOKEN_KEY, t);
      setTokenState(t);
    }
  };

  return { token, setToken };
}
