"use client";

import { FormEvent, useMemo, useState } from "react";

type Citation = {
  document_id?: string;
  title?: string;
  area?: string;
  snippet?: string;
  retrieval_score?: number;
};

const API_GATEWAY = process.env.NEXT_PUBLIC_API_GATEWAY_URL ?? "http://localhost:8080";

export default function Page() {
  const [tenantId, setTenantId] = useState("11111111-1111-1111-1111-111111111111");
  const [email, setEmail] = useState("ceo@novaboard.ai");
  const [password, setPassword] = useState("123456");
  const [token, setToken] = useState("");
  const [question, setQuestion] = useState("Quais os principais riscos e decisões pendentes deste mês?");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);
  const [error, setError] = useState("");

  const canAsk = useMemo(() => token.trim().length > 0 && question.trim().length > 0, [token, question]);

  async function loginDemo() {
    setAuthLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_GATEWAY}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const body = await response.json();
      const access = body?.data?.access_token ?? body?.access_token;
      if (!response.ok || !access) {
        throw new Error(body?.data?.detail ?? body?.detail ?? "Falha no login");
      }
      setToken(access);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado no login");
    } finally {
      setAuthLoading(false);
    }
  }

  async function askExecutiveQuestion(event: FormEvent) {
    event.preventDefault();
    if (!canAsk) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setCitations([]);
    setConfidence(null);

    try {
      const response = await fetch(`${API_GATEWAY}/api/v1/agent/orchestrator/executive-question/stream?stream=1`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "text/event-stream",
          "Authorization": `Bearer ${token}`,
          "x-tenant-id": tenantId,
        },
        body: JSON.stringify({ question, role: "ceo", intent: "executive_question" }),
      });

      if (!response.ok) {
        const txt = await response.text();
        throw new Error(txt || "Falha ao consultar orquestrador");
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error("Streaming não disponível");

      const decoder = new TextDecoder();
      let buffer = "";
      let activeEvent = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const messages = buffer.split("\n\n");
        buffer = messages.pop() ?? "";

        for (const msg of messages) {
          const lines = msg.split("\n");
          for (const line of lines) {
            if (line.startsWith("event:")) {
              activeEvent = line.replace("event:", "").trim();
            }
            if (line.startsWith("data:")) {
              const payload = line.replace("data:", "").trim();
              if (activeEvent === "chunk") {
                setAnswer((prev) => prev + payload);
              }
              if (activeEvent === "done") {
                try {
                  const parsed = JSON.parse(payload);
                  setCitations(parsed.citations ?? []);
                  setConfidence(parsed.confidence_score ?? null);
                } catch {
                  // ignore malformed final payload
                }
              }
            }
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado no chat");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <h2 className="text-xl font-semibold">Board AI Chat</h2>
        <p className="mt-1 text-sm text-muted">Chat executivo com streaming do orquestrador e citações do RAG.</p>
      </div>

      <div className="panel grid gap-4 p-5 lg:grid-cols-2">
        <div className="space-y-3">
          <label className="block text-sm font-medium">Tenant ID</label>
          <input className="w-full rounded-lg border border-line px-3 py-2 text-sm" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />

          <label className="block text-sm font-medium">Email</label>
          <input className="w-full rounded-lg border border-line px-3 py-2 text-sm" value={email} onChange={(e) => setEmail(e.target.value)} />

          <label className="block text-sm font-medium">Senha</label>
          <input type="password" className="w-full rounded-lg border border-line px-3 py-2 text-sm" value={password} onChange={(e) => setPassword(e.target.value)} />

          <button onClick={loginDemo} disabled={authLoading} className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">
            {authLoading ? "Autenticando..." : "Login (JWT)"}
          </button>
        </div>

        <div className="space-y-3">
          <label className="block text-sm font-medium">Token JWT</label>
          <textarea className="h-36 w-full rounded-lg border border-line px-3 py-2 text-xs" value={token} onChange={(e) => setToken(e.target.value)} />
        </div>
      </div>

      <form className="panel space-y-3 p-5" onSubmit={askExecutiveQuestion}>
        <label className="block text-sm font-medium">Pergunta Executiva</label>
        <textarea className="h-24 w-full rounded-lg border border-line px-3 py-2 text-sm" value={question} onChange={(e) => setQuestion(e.target.value)} />
        <button type="submit" disabled={!canAsk || loading} className="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">
          {loading ? "Consultando..." : "Perguntar"}
        </button>
      </form>

      {error ? (
        <div className="panel border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>
      ) : null}

      <div className="panel p-5">
        <h3 className="font-semibold">Resposta</h3>
        <p className="mt-2 whitespace-pre-wrap text-sm text-slate-800">{answer || "Sem resposta ainda."}</p>
        <p className="mt-3 text-xs text-muted">
          Confidence score: {confidence !== null ? confidence.toFixed(2) : "n/a"}
        </p>
      </div>

      <div className="panel p-5">
        <h3 className="font-semibold">Citações</h3>
        <div className="mt-3 space-y-3">
          {citations.length === 0 ? <p className="text-sm text-muted">Nenhuma citação retornada.</p> : null}
          {citations.map((citation, idx) => (
            <article key={`${citation.document_id ?? "doc"}-${idx}`} className="rounded-lg border border-line p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                {citation.title ?? citation.document_id ?? "Documento"} {citation.area ? `• ${citation.area}` : ""}
              </p>
              <p className="mt-1 text-sm text-slate-800">{citation.snippet ?? "Sem trecho."}</p>
              <p className="mt-2 text-xs text-muted">Score: {citation.retrieval_score ?? "n/a"}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
