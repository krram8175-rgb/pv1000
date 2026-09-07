import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Header } from "@/components/Header";
import { RF_5M_PAGES } from "@/lib/rfQuestions";
import { Sigma, ChevronLeft, ChevronRight } from "lucide-react";

export default function RelationsFunctions5M() {
  const { subjectId } = useParams();
  const navigate = useNavigate();
  const [page, setPage] = React.useState(0);
  const total = RF_5M_PAGES.length;
  const items = RF_5M_PAGES[page] || [];

  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [page]);

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Header showBack title="Relations and Functions" Icon={Sigma} bgClass="bg-violet-600" />

      {/* pb-28 leaves room so content is never hidden behind the fixed nav bar */}
      <main className="mx-auto max-w-2xl px-4 pb-28 pt-6 md:px-6">
        <div className="mb-5 flex items-center justify-between rounded-2xl border border-violet-100 bg-white p-4 shadow-sm">
          <div>
            <p className="text-xs font-bold uppercase tracking-wide text-violet-600">5 Marks · Part D</p>
            <h1 className="text-base font-extrabold text-slate-900">Relations and Functions</h1>
          </div>
          <span className="rounded-lg bg-violet-600 px-3 py-1.5 text-sm font-bold text-white">
            Page {page + 1} / {total}
          </span>
        </div>

        <div className="space-y-4">
          {items.map((q, i) => (
            <div key={i} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="mb-2 flex items-center gap-2">
                <span className="rounded-md bg-violet-50 px-2 py-1 text-xs font-bold text-violet-700">{q.year}</span>
                <span className="rounded-md bg-slate-100 px-2 py-1 text-xs font-bold text-slate-600">{q.qno}</span>
                <span className="ml-auto rounded-md border border-violet-200 px-2 py-1 text-xs font-bold text-violet-700">5M</span>
              </div>
              <p className="text-[15px] leading-relaxed text-slate-800">{q.text}</p>
            </div>
          ))}
        </div>
      </main>

      {/* FIXED navigation bar — stays put, never scrolls away */}
      <div className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-2xl items-center justify-between gap-3 px-4 py-3 md:px-6">
          <button
            type="button"
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-bold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" /> Previous
          </button>

          <div className="flex items-center gap-1.5">
            {RF_5M_PAGES.map((_, i) => (
              <span
                key={i}
                className={`h-2 w-2 rounded-full transition ${i === page ? "w-5 bg-violet-600" : "bg-slate-300"}`}
              />
            ))}
          </div>

          <button
            type="button"
            onClick={() => setPage((p) => Math.min(total - 1, p + 1))}
            disabled={page === total - 1}
            className="inline-flex items-center gap-1.5 rounded-xl bg-violet-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Next <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
