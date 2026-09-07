import React from "react";
import { useParams } from "react-router-dom";
import { Header } from "@/components/Header";
import { RF_5M_PAGES } from "@/lib/rfQuestions";
import { Sigma, ChevronLeft, ChevronRight } from "lucide-react";

const TINTS = {
  teal: "bg-teal-300/80",
  sky: "bg-sky-300/80",
  blue: "bg-blue-400/80",
  indigo: "bg-indigo-400/80",
  violet: "bg-violet-400/80",
};

export default function RelationsFunctions5M() {
  const { subjectId, ch } = useParams();
  const [page, setPage] = React.useState(0);
  const total = RF_5M_PAGES.length;
  const groups = RF_5M_PAGES[page] || [];

  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [page]);

  return (
    <div className="min-h-screen" style={{ backgroundImage: "linear-gradient(180deg, #6FE7DD 0%, #79A9E7 52%, #9C8BEA 100%)" }}>
      <Header showBack title="Relations and Functions" Icon={Sigma} bgClass="bg-violet-600" />

      {/* pb-28 keeps content clear of the fixed nav bar */}
      <main className="mx-auto max-w-2xl px-3 pb-28 pt-4 md:px-6">
        <div className="space-y-6">
          {groups.map((g) => (
            <section key={g.year} className="overflow-hidden rounded-xl shadow-sm">
              {/* Year banner */}
              <div className={`px-4 py-6 text-center ${TINTS[g.tint] || TINTS.teal}`}>
                <h2 className="text-4xl font-black italic tracking-wide text-black" style={{ fontFamily: "Georgia, 'Times New Roman', serif" }}>
                  {g.year}
                </h2>
              </div>

              {/* Question cards */}
              {g.questions.length === 0 ? (
                <div className="border-t border-slate-200 bg-white/95 px-4 py-6 text-center">
                  <p className="text-xs font-semibold text-slate-500">Questions will be added soon.</p>
                </div>
              ) : (
                <div className="space-y-px bg-slate-200">
                  {g.questions.map((q, i) => (
                    <div key={i} className="bg-white px-4 py-3">
                      <div className="mb-1 flex items-center gap-2">
                        <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-bold text-slate-600">{q.tag}</span>
                        <span className="rounded bg-violet-50 px-1.5 py-0.5 text-[10px] font-bold text-violet-700">{q.qno}</span>
                        <span className="ml-auto text-[11px] font-bold text-slate-500">({q.marks})</span>
                      </div>
                      <p className="text-[12px] leading-relaxed text-slate-800">{q.text}</p>
                    </div>
                  ))}
                </div>
              )}
            </section>
          ))}
        </div>
      </main>

      {/* FIXED navigation bar */}
      <div className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-2xl items-center justify-between gap-3 px-4 py-3 md:px-6">
          <button
            type="button"
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="inline-flex items-center gap-1.5 rounded-xl border-2 border-slate-500 bg-white px-5 py-2.5 text-sm font-bold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" /> Previous
          </button>

          <div className="flex items-center gap-2">
            <span className="text-sm font-extrabold text-slate-800">{page + 1}/{total}</span>
            <div className="flex items-center gap-1.5">
              {RF_5M_PAGES.map((_, i) => (
                <span key={i} className={`h-2 w-2 rounded-full transition ${i === page ? "w-5 bg-violet-600" : "bg-slate-300"}`} />
              ))}
            </div>
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
