"""Streamlit app:  streamlit run app.py"""
import json
from collections import Counter
from pathlib import Path

import streamlit as st

from src import llm_classifier, register
from src.policy import load_policy
from src.triage import triage

st.set_page_config(page_title="AI Use-Case Triage", page_icon="🛡️", layout="wide")
policy = load_policy()
TIER_COLOR = {"prohibited": "🔴", "high": "🟠", "limited": "🟡", "minimal": "🟢"}

st.title("🛡️ AI Use-Case Intake & Risk Triage")
st.caption(f"Policy v{policy['version']} · {policy['disclaimer']}")
mode = "Hybrid (rules + LLM)" if llm_classifier.available() else "Rules only (add ANTHROPIC_API_KEY for hybrid)"
st.caption(f"Mode: {mode}")

intake, portfolio = st.tabs(["New intake", "Portfolio register"])

with intake:
    with st.form("intake"):
        title = st.text_input("Use-case name", "Graduate program shortlist")
        description = st.text_area(
            "What will the AI do, and who does it affect?",
            "Read applications to our graduate program and pick which people move to interviews "
            "based on predicted job success.",
            height=120,
        )
        submitted = st.form_submit_button("Triage")

    if submitted and title and description:
        r = triage(title, description)
        register.add(r)
        st.subheader(f"{TIER_COLOR[r.tier]} {r.tier_label} · {r.decision}")
        st.write(f"Review SLA: **{r.review_sla_days} days** · Approvers: **{', '.join(r.approvers)}**")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Why**")
            for x in r.reasons:
                st.markdown(f"- {x}")
        with c2:
            st.markdown("**Required controls**")
            for x in r.controls:
                st.checkbox(x, key=f"ctl-{x}")
        st.caption("Saved to the register. A human reviewer makes the final decision.")

with portfolio:
    rows = register.load()
    if not rows and st.button("Load sample portfolio (24 example use cases)"):
        for line in Path("eval/eval_set.jsonl").read_text().splitlines():
            c = json.loads(line)
            register.add(triage(c["title"], c["description"]))
        st.rerun()
    if rows:
        counts = Counter(r["tier"] for r in rows)
        cols = st.columns(4)
        for col, t in zip(cols, policy["tiers"]):
            col.metric(f"{TIER_COLOR[t['id']]} {t['label']}", counts.get(t["id"], 0))
        st.dataframe(
            [{"Use case": r["title"], "Tier": r["tier_label"], "Decision": r["decision"],
              "Overlays": ", ".join(r["overlays"]), "Mode": r["mode"], "Triaged": r["triaged_at"][:10]}
             for r in reversed(rows)],
            use_container_width=True, hide_index=True,
        )
