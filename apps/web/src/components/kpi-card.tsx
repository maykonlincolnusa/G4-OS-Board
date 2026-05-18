type Props = {
  title: string;
  value: string;
  trend: string;
  status?: "good" | "warning" | "risk";
};

export function KpiCard({ title, value, trend, status = "good" }: Props) {
  const tone = {
    good: "text-emerald-700 bg-emerald-50",
    warning: "text-amber-700 bg-amber-50",
    risk: "text-red-700 bg-red-50",
  }[status];

  return (
    <article className="panel p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</p>
      <p className="mt-3 text-2xl font-bold text-ink">{value}</p>
      <span className={`mt-3 inline-flex rounded-full px-2 py-1 text-xs font-semibold ${tone}`}>{trend}</span>
    </article>
  );
}

