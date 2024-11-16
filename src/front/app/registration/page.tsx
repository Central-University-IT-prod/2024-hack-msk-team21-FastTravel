"use client";
import { useState, useRef } from "react";
import Link from "next/link";
import "./styles.css";

export default function Registration() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordRepeat, setPasswordRepeat] = useState("");
  const nameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const passwordRepeatRef = useRef<HTMLInputElement>(null);

  const register = async () => {
    if (password !== passwordRepeat) {
      alert("Пароли не совпадают");
      return;
    }

    const data = {
      name,
      email,
      password,
    };

    try {
      const response = await fetch("/api/registration", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        alert("Регистрация успешна");
      } else {
        const result = await response.json();
        alert(`Ошибка: ${result.error}`);
      }
    } catch (error) {
      console.error("Ошибка:", error);
      alert("Произошла ошибка при регистрации");
    }
  };

  return (
      <div>
        <a id="welcome">Регистрация</a>
        <div id="login_form">
          <div className="input" onClick={() => nameRef.current?.focus()}>
            <input
                ref={nameRef}
                className="input__field"
                name="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder=" "
                autoComplete="off"
                autoCorrect="off"
            />
            <label className="input__label">Имя</label>
          </div>
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
          <div className="input" onClick={() => passwordRepeatRef.current?.focus()}>
            <input
                ref={passwordRepeatRef}
                className="input__field"
                name="password_repeat"
                type="password"
                value={passwordRepeat}
                onChange={(e) => setPasswordRepeat(e.target.value)}
                placeholder=" "
                autoComplete="off"
                autoCorrect="off"
            />
            <label className="input__label">Повторите пароль</label>
          </div>
          <button id="register" onClick={register}>Создать</button>
        </div>
        <Link href="/login">
          <button id="login_button">Уже есть аккаунт?</button>
        </Link>
      </div>
  );
}