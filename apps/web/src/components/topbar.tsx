export function Topbar() {
  return (
    <header className="sticky top-0 z-10 border-b border-line bg-white/90 px-6 py-4 backdrop-blur">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold">Board Governance OS AI</h1>
          <p className="text-xs text-muted">Workspace: NovaBoard Academy Group</p>
        </div>
        <div className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">System Health 97%</div>
      </div>
    </header>
  );
}

