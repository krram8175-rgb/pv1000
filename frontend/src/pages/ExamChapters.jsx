import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Header } from "@/components/Header";
import { EXAM_CHAPTERS, SUBJECT_META } from "@/lib/examChapters";
import { Atom, ChevronRight, GraduationCap, Lock, FileText } from "lucide-react";

const CLASSES = [
  { key: "11", label: "Class 11", sub: "1st PUC" },
  { key: "12", label: "Class 12", sub: "2nd PUC" },
];

// Chapters that stay unlocked in addition to the first two of each list.
const EXTRA_FREE = new Set(["Matrices", "Atoms"]);

// Chapters that are ALWAYS locked (in every exam), regardless of position.
const FORCE_LOCK = new Set(["Electrostatic Potential and Capacitance", "Electrochemistry"]);

// Chapters locked only in a specific exam. Keyed by `${examId}:${chapterName}`.
const FORCE_LOCK_BY_EXAM = new Set(["neet:Structure of Atom", "neet:Motion in a Straight Line", "kcet:Determinants", "kcet:Motion in a Straight Line"]);

// Subjects where every chapter is locked.
const LOCK_ALL_SUBJECTS = new Set(["biology"]);

// Chapter names that have a ready PYQ practice bank -> maps to backend bank key.
// Keyed by `${examId}:${subjectId}:${chapterName}`.
const CHAPTER_BANKS = {
  "neet:physics:Units and Measurements": "neet-physics-units-and-measurements",
  "neet:physics:Electric Charges and Fields": "neet-physics-electric-charges-and-fields",
  "neet:physics:Atoms": "neet-physics-atoms",
  "neet:chemistry:Some Basic Concepts of Chemistry": "neet-chemistry-some-basic-concepts-of-chemistry",
  "neet:chemistry:Solutions": "neet-chemistry-solutions",
  "neet:math:Basic Maths": "neet-math-basic-maths",
  "neet:math:Set and Relation": "neet-math-set-and-relation",
  "neet:math:Matrices": "neet-math-matrices",
  "neet:math:Determinants": "neet-math-determinants",
  "kcet:physics:Units and Measurements": "kcet-physics-units-and-measurements",
  "kcet:physics:Electric Charges and Fields": "kcet-physics-electric-charges-and-fields",
  "kcet:physics:Atoms": "neet-physics-atoms",
  "kcet:chemistry:Some Basic Concepts of Chemistry": "neet-chemistry-some-basic-concepts-of-chemistry",
  "kcet:chemistry:Structure of Atom": "neet-chemistry-structure-of-atom",
  "kcet:chemistry:Solutions": "neet-chemistry-solutions",
  "kcet:math:Basic Maths": "neet-math-basic-maths",
  "kcet:math:Set and Relation": "neet-math-set-and-relation",
  "kcet:math:Matrices": "neet-math-matrices",
  "kcet:math:Determinants": "neet-math-determinants",
  "jee-main:math:Basic Maths": "neet-math-basic-maths",
  "jee-main:math:Set and Relation": "neet-math-set-and-relation",
  "jee-main:math:Matrices": "neet-math-matrices",
  "jee-main:math:Determinants": "neet-math-determinants",
  "jee-adv:math:Basic Maths": "neet-math-basic-maths",
  "jee-adv:math:Set and Relation": "neet-math-set-and-relation",
  "jee-adv:math:Matrices": "neet-math-matrices",
  "jee-adv:math:Determinants": "neet-math-determinants",
};

export default function ExamChapters() {
  const { examId, subjectId, cls } = useParams();
  const navigate = useNavigate();
  const meta = SUBJECT_META[subjectId] || { name: "Subject", Icon: Atom, bg: "bg-slate-700" };
  const Icon = meta.Icon;
  const data = EXAM_CHAPTERS[subjectId] || {};

  // Level 2 — chapters of the selected class
  if (cls) {
    const clsMeta = CLASSES.find((c) => c.key === cls) || CLASSES[0];
    const chapters = data[cls] || [];
    return (
      <div className="min-h-screen bg-[#F8FAFC]">
        <Header showBack title={`${meta.name} · ${clsMeta.label}`} Icon={Icon} bgClass={meta.bg} />
        <main className="mx-auto max-w-2xl px-4 py-8 md:px-6">
          {(examId === "neet" || examId === "kcet") && (
            <button
              data-testid="chapters-full-paper-btn"
              onClick={() => navigate(`/exam/${examId}/papers`)}
              className="group mb-4 flex w-full items-center gap-2.5 rounded-xl bg-[#5B50E6] px-4 py-3.5 shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg"
            >
              <FileText className="h-4 w-4 text-indigo-100" />
              <span className="text-sm font-bold text-white">Full Paper</span>
              <ChevronRight className="ml-auto h-4 w-4 text-indigo-100 transition-transform group-hover:translate-x-1" />
            </button>
          )}
          <div className="mb-4 flex items-center gap-2">
            <span className={`rounded-lg px-2.5 py-1 text-xs font-extrabold text-white ${meta.bg}`}>{clsMeta.label}</span>
            <span className="ml-auto text-xs font-medium text-slate-400">{chapters.length} chapters</span>
          </div>
          <div className="space-y-2.5">
            {chapters.map((name, i) => {
              const locked = LOCK_ALL_SUBJECTS.has(subjectId) || FORCE_LOCK.has(name) || FORCE_LOCK_BY_EXAM.has(`${examId}:${name}`) || (i >= 2 && !EXTRA_FREE.has(name));
              const bankKey = CHAPTER_BANKS[`${examId}:${subjectId}:${name}`];
              const clickable = !locked && !!bankKey;
              return (
                <div
                  key={`${cls}-${i}`}
                  data-testid={`chapter-${cls}-${i + 1}`}
                  data-locked={locked ? "true" : "false"}
                  onClick={() => clickable && navigate(`/exam/${examId}/${subjectId}/practice/${bankKey}`)}
                  className={`flex items-center gap-3 rounded-xl border px-4 py-3 shadow-sm transition-all ${
                    locked ? "border-slate-200 bg-slate-50" : "border-slate-200 bg-white hover:-translate-y-0.5 hover:shadow-md"
                  } ${clickable ? "cursor-pointer" : ""}`}
                >
                  <span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-sm font-extrabold text-white ${locked ? "bg-slate-300" : meta.bg}`}>
                    {i + 1}
                  </span>
                  <span className={`text-sm font-semibold ${locked ? "text-slate-400" : "text-slate-900"}`}>{name}</span>
                  {clickable && (
                    <span className="ml-2 rounded-md bg-blue-50 px-2 py-0.5 text-[11px] font-bold text-blue-700">PYQs</span>
                  )}
                  {locked ? (
                    <span className="ml-auto flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-rose-50 text-rose-500 ring-1 ring-rose-100">
                      <Lock className="h-4 w-4" />
                    </span>
                  ) : clickable ? (
                    <ChevronRight className="ml-auto h-4 w-4 text-slate-400" />
                  ) : null}
                </div>
              );
            })}
          </div>
        </main>
      </div>
    );
  }

  // Level 1 — pick class (1st PUC / 2nd PUC)
  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Header showBack title={meta.name} Icon={Icon} bgClass={meta.bg} />
      <main className="mx-auto max-w-2xl space-y-4 px-4 py-8 md:px-6">
        {(examId === "neet" || examId === "kcet") && (
          <button
            data-testid="class-full-paper-btn"
            onClick={() => navigate(`/exam/${examId}/papers`)}
            className="group flex w-full items-center gap-2.5 rounded-xl bg-[#5B50E6] px-4 py-3.5 shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg"
          >
            <FileText className="h-4 w-4 text-indigo-100" />
            <span className="text-sm font-bold text-white">Full Paper</span>
            <ChevronRight className="ml-auto h-4 w-4 text-indigo-100 transition-transform group-hover:translate-x-1" />
          </button>
        )}
        {CLASSES.map((c) => {
          const count = (data[c.key] || []).length;
          return (
            <button
              key={c.key}
              data-testid={`class-card-${c.key}`}
              onClick={() => navigate(`/exam/${examId}/${subjectId}/chapters/${c.key}`)}
              className="group flex w-full items-center gap-4 rounded-2xl border border-slate-200 bg-white px-5 py-5 text-left shadow-sm transition-all hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
            >
              <span className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-white ${meta.bg}`}>
                <GraduationCap className="h-6 w-6" />
              </span>
              <div>
                <p className="text-base font-extrabold tracking-tight text-slate-900">{c.label}</p>
                <p className="text-sm text-slate-500">{count} chapters</p>
              </div>
              <ChevronRight className="ml-auto h-5 w-5 text-slate-400 transition-transform group-hover:translate-x-1 group-hover:text-slate-900" />
            </button>
          );
        })}
      </main>
    </div>
  );
}
