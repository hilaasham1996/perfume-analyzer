from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import sqlite3
import os
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "perfumes.db")
DB_PATH = os.path.abspath(DB_PATH)

app = FastAPI(title="Perfume Preference Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeReq(BaseModel):
    favorites: List[str] = None
    notes: List[str] = None

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_perfume_by_name(name: str):
    conn = get_conn()
    cur = conn.execute("SELECT * FROM perfumes WHERE LOWER(name)=?", (name.lower().strip(),))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def notes_for_perfume(perfume_id: int):
    conn = get_conn()
    cur = conn.execute("""SELECT n.name, pn.prominence 
                          FROM perfume_notes pn
                          JOIN notes n ON pn.note_id = n.id
                          WHERE pn.perfume_id = ?""", (perfume_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"name": r["name"], "prominence": r["prominence"]} for r in rows]

def family_for_note(note_name: str):
    conn = get_conn()
    cur = conn.execute("SELECT family_primary, family_secondary FROM note_family_map WHERE LOWER(note)=?", (note_name.lower().strip(),))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None, None
    return row["family_primary"], row["family_secondary"]

def all_perfumes():
    conn = get_conn()
    cur = conn.execute("SELECT * FROM perfumes")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/analyze")
def analyze(req: AnalyzeReq):
    # collect notes either from favorites or from provided notes
    collected = {}  # note -> total prominence
    if req.favorites:
        # try to lookup each perfume
        for name in req.favorites:
            if not name or not name.strip():
                continue
            p = get_perfume_by_name(name)
            if p:
                notes = notes_for_perfume(p["id"])
                for n in notes:
                    key = n["name"].lower()
                    collected[key] = collected.get(key, 0) + (n.get("prominence") or 5)
            else:
                # treat the favorite as free-text: split by commas and assume they listed notes
                parts = [s.strip() for s in name.split(",") if s.strip()]
                for part in parts:
                    key = part.lower()
                    collected[key] = collected.get(key, 0) + 5
    if req.notes:
        for n in req.notes:
            key = n.lower().strip()
            if key:
                collected[key] = collected.get(key, 0) + 5

    if not collected:
        return {"error": "No valid favorites or notes provided."}

    # map notes to families and compute weights
    family_scores = {}
    note_entries = []
    for note, score in collected.items():
        fam1, fam2 = family_for_note(note)
        note_entries.append({"note": note, "score": score, "family_primary": fam1, "family_secondary": fam2})
        if fam1:
            family_scores[fam1] = family_scores.get(fam1, 0) + score * 1.0
        if fam2:
            family_scores[fam2] = family_scores.get(fam2, 0) + score * 0.5

    # normalize family scores to percentages
    total = sum(family_scores.values()) or 1
    profile = [{"family": k, "score": round((v/total)*100,1)} for k,v in sorted(family_scores.items(), key=lambda x: -x[1])]

    # top notes
    top_notes = sorted(note_entries, key=lambda x: -x["score"])[:10]

    # simple recommendation: score perfumes by overlap of notes / families
    perfumes = all_perfumes()
    recs = []
    user_notes = set(n for n in collected.keys())
    user_families = set(k for k in family_scores.keys())
    for p in perfumes:
        pnotes = set(n["name"].lower() for n in notes_for_perfume(p["id"]))
        overlap_notes = len(user_notes.intersection(pnotes))
        # families for perfume
        pfams = set()
        for nn in pnotes:
            f1,f2 = family_for_note(nn)
            if f1: pfams.add(f1)
            if f2: pfams.add(f2)
        overlap_families = len(user_families.intersection(pfams))
        score = overlap_notes*2 + overlap_families*1
        if score>0:
            reason = f"{overlap_notes} shared notes, {overlap_families} shared families"
            recs.append({"name": p["name"], "brand": p.get("brand"), "score": score, "reason": reason})
    recs = sorted(recs, key=lambda x: -x["score"])[:10]

    return {"profile": profile, "top_notes": top_notes, "recommendations": recs}

@app.get("/api/perfumes")
def list_perfumes():
    return all_perfumes()
