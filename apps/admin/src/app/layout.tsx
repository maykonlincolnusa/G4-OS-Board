export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body style={{ margin: 0, fontFamily: "Segoe UI, sans-serif", background: "#f4f7fa" }}>
        <div style={{ padding: 24 }}>
          <h1>Board Governance OS AI - Admin</h1>
          {children}
        </div>
      </body>
    </html>
  );
}

