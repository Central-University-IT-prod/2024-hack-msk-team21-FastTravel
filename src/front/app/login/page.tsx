"use client";
import { useState, useRef } from "react";
import Link from "next/link";
// @ts-expect-error
import Cookies from "js-cookie";
import "./styles.css"

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  const login = async () => {
    const data = {
      email,
      password,
    };

    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        Cookies.set("access_token_cookie", result.access_token, { expires: 1, secure: true, sameSite: "strict" });
        alert("Вход успешен");
      } else {
        const result = await response.json();
        alert(`Ошибка: ${result.error}`);
      }
    } catch (error) {
      console.error("Ошибка:", error);
      alert("Произошла ошибка при входе");
    }
  };

  return (
      <div>
        <a id="welcome">Войди в систему</a>
        <div id="login_form">
          <div className="input" onClick={() => emailRef.current?.focus()}>
            <input
                ref={emailRef}
                className="input__field"
                name="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder=" "
                autoComplete="off"
                autoCorrect="off"
            />
            <label className="input__label">Email</label>
          </div>
          <div className="input" onClick={() => passwordRef.current?.focus()}>
            <input
                ref={passwordRef}
                className="input__field"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder=" "
                autoComplete="off"
                autoCorrect="off"
            />
            <label className="input__label">Пароль</label>
          </div>
          <button id="login" onClick={login}>Войти</button>
        </div>
        <Link href="/registration">
          <button id="register_button">Нет аккаунта?</button>
        </Link>
      </div>
  );
}