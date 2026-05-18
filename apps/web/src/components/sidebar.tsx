import Link from "next/link";

const links = [
  ["Executive Dashboard", "/dashboard"],
  ["Board AI Chat", "/board-ai-chat"],
  ["Board Pack Generator", "/board-pack-generator"],
  ["Meetings", "/meetings"],
  ["Decision Memory", "/decision-memory"],
  ["Action Tracker", "/action-tracker"],
  ["Risk Center", "/risk-center"],
  ["Approval Workflows", "/approval-workflows"],
  ["Document Library", "/document-library"],
  ["Knowledge Base", "/knowledge-base"],
  ["Agents Console", "/agents-console"],
  ["Skills & Playbooks", "/skills-playbooks"],
  ["Channels", "/channels"],
  ["Integrations", "/integrations"],
  ["Analytics", "/analytics"],
  ["Audit Logs", "/audit-logs"],
  ["Settings", "/settings"],
  ["Users & Permissions", "/users-permissions"],
  ["Admin Ops", "/admin-ops"]
] as const;

export function Sidebar() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-line bg-white px-4 py-6 lg:block">
      <div className="mb-6 rounded-xl bg-slate-900 p-4 text-white">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Board Governance OS AI</p>
        <p className="mt-2 text-sm font-semibold">Executive Governance Platform</p>
      </div>
      <nav className="space-y-2">
        {links.map(([label, href]) => (
          <Link key={href} href={href} className="block rounded-lg px-3 py-2 text-sm text-slate-700 hover:bg-slate-100">
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}

