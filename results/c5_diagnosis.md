# Criterion 5 — where the retrieval time goes (diagnosis)

One-off measurement for the Diagnoses section. It times `store.py::search` and the three steps inside it with the repo's own `store` module; it is not part of the system and changes nothing in it. Everything being compared is timed inside the same loop iteration so it all sees the same machine load, and each figure is the median of 50 iterations after a discarded warm-up. Measured 2 times, in the same condition as the run log: battery, Low Power Mode on, no apps closed. The script is listed at the bottom.

- Machine: Apple M4, 10 cores; onnxruntime 1.30.0
- Providers on the embedder's session, as chromadb sets them: `['CoreMLExecutionProvider', 'AzureExecutionProvider', 'CPUExecutionProvider']`
- chromadb's tokenizer pads every input to 256 tokens

## Run 1

- When: 2026-09-29 14:57:51
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 4.48 5.85 4.21 }

### A. `store.search()` and its three steps (median ms, 50 iterations)

| Question | `store.search()` | client + `get_collection` | `store.embed` (the question) | `count` + `query` (lookup) | embed share of the three steps |
|---|---|---|---|---|---|
| When does a grade appeal go to the department? | 86.8 | 3.3 | 76.7 | 4.7 | 91% |
| How to get an urgent health appointment? | 88.6 | 3.3 | 81.2 | 4.8 | 91% |
| What are the assessments for Linear Algebra? | 86.1 | 3.3 | 78.3 | 4.6 | 91% |
| When does Halden Hall close? | 90.3 | 3.4 | 84.9 | 5.0 | 91% |
| What is good about dining at the Atrium? | 94.1 | 3.5 | 84.3 | 5.0 | 91% |

### B. One forward pass of the embedding model (median ms, 50 iterations, order rotated)

| Question | tokens | chromadb providers, padded to 256 | chromadb providers, unpadded | CPU provider only, padded to 256 | CPU provider only, unpadded | cos(padded, unpadded) | cos(chromadb providers, CPU only) |
|---|---|---|---|---|---|---|---|
| When does a grade appeal go to the department? | 12 | 113.4 | 25.7 | 28.3 | 2.6 | 1.000000 | 1.000000 |
| How to get an urgent health appointment? | 10 | 102.2 | 23.2 | 25.7 | 2.3 | 1.000000 | 1.000000 |
| What are the assessments for Linear Algebra? | 10 | 101.9 | 22.5 | 24.6 | 2.3 | 1.000000 | 1.000000 |
| When does Halden Hall close? | 9 | 113.6 | 26.0 | 28.7 | 3.0 | 1.000000 | 1.000000 |
| What is good about dining at the Atrium? | 11 | 108.1 | 24.5 | 26.1 | 2.5 | 1.000000 | 1.000000 |

### C. CPU-seconds used per wall-clock second during a padded forward pass

| chromadb providers | CPU provider only |
|---|---|
| 4.96 | 4.98 |

## Run 2

- When: 2026-09-29 14:59:28
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 7.57 6.47 4.61 }

### A. `store.search()` and its three steps (median ms, 50 iterations)

| Question | `store.search()` | client + `get_collection` | `store.embed` (the question) | `count` + `query` (lookup) | embed share of the three steps |
|---|---|---|---|---|---|
| When does a grade appeal go to the department? | 83.9 | 3.3 | 77.6 | 4.6 | 91% |
| How to get an urgent health appointment? | 85.5 | 3.3 | 76.5 | 4.7 | 90% |
| What are the assessments for Linear Algebra? | 91.5 | 3.3 | 82.9 | 4.8 | 91% |
| When does Halden Hall close? | 86.3 | 3.3 | 77.3 | 4.7 | 91% |
| What is good about dining at the Atrium? | 84.7 | 3.3 | 76.4 | 4.6 | 91% |

### B. One forward pass of the embedding model (median ms, 50 iterations, order rotated)

| Question | tokens | chromadb providers, padded to 256 | chromadb providers, unpadded | CPU provider only, padded to 256 | CPU provider only, unpadded | cos(padded, unpadded) | cos(chromadb providers, CPU only) |
|---|---|---|---|---|---|---|---|
| When does a grade appeal go to the department? | 12 | 98.9 | 22.7 | 24.7 | 2.4 | 1.000000 | 1.000000 |
| How to get an urgent health appointment? | 10 | 103.8 | 22.2 | 25.1 | 2.5 | 1.000000 | 1.000000 |
| What are the assessments for Linear Algebra? | 10 | 98.9 | 24.1 | 26.5 | 2.6 | 1.000000 | 1.000000 |
| When does Halden Hall close? | 9 | 102.4 | 22.8 | 25.9 | 2.4 | 1.000000 | 1.000000 |
| What is good about dining at the Atrium? | 11 | 103.4 | 23.0 | 25.0 | 2.6 | 1.000000 | 1.000000 |

### C. CPU-seconds used per wall-clock second during a padded forward pass

| chromadb providers | CPU provider only |
|---|---|
| 4.65 | 4.97 |

## The script

```python
"""Where do store.search()'s milliseconds go? One-off measurement for criterion 5.

    python diagnose_c5.py <output.md> [runs]

Not part of the system and changes nothing in it: it imports the repo's own
`store` module and times its pieces. Every piece being compared is timed inside
the same loop iteration, so they all see the same machine load; medians over N
iterations after one discarded warm-up. No model calls. The listing of this
script is appended to the output file.
"""

import datetime as dt
import os
import re
import statistics as st
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = "/Users/adri/scripts/projects/codepath/ai-prep/ai201-project1-starter-v2026"
sys.path.insert(0, REPO)

import config  # noqa: E402
import questions as qs  # noqa: E402
import store  # noqa: E402
import onnxruntime as ort  # noqa: E402

N = 50
QS = [q["question"] for q in qs.answered()]
out = []


def say(line=""):
    out.append(line)
    print(line, flush=True)


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def ms(t0, t1):
    return (t1 - t0) * 1000


def conditions():
    low = re.search(r"lowpowermode\s+(\d)", sh("pmset", "-g"))
    return [
        f"- When: {dt.datetime.now():%Y-%m-%d %H:%M:%S}",
        f"- Power: {sh('pmset', '-g', 'batt').splitlines()[0].strip()}; Low Power Mode "
        f"{ {'1': 'on', '0': 'off'}.get(low.group(1) if low else '', 'unknown') }",
        f"- Load average (1/5/15 min): {sh('sysctl', '-n', 'vm.loadavg').strip()}",
    ]


def feed(ids, mask):
    ids = np.array([ids], dtype=np.int64)
    return {"input_ids": ids, "attention_mask": np.array([mask], dtype=np.int64),
            "token_type_ids": np.zeros_like(ids)}


def pooled(session, f):
    """The same mean pooling + normalisation chromadb's embedder applies."""
    hidden = session.run(None, f)[0]
    m = f["attention_mask"][..., None]
    v = (hidden * m).sum(1) / np.clip(m.sum(1), 1e-9, None)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


name = config.collection_name(None, "default")
ef = store._embedder()._ef                     # chromadb's ONNXMiniLM_L6_V2
model_path = os.path.join(ef.DOWNLOAD_PATH, ef.EXTRACTED_FOLDER_NAME, "model.onnx")
so = ort.SessionOptions()
so.log_severity_level = 3
cpu_only = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"], sess_options=so)


def split_search(q):
    """store.search() itself, plus the same three steps it takes, per iteration."""
    store.search(q)  # warm-up, discarded
    s = {"search": [], "client": [], "embed": [], "lookup": []}
    for _ in range(N):
        t0 = time.perf_counter()
        store.search(q)
        t1 = time.perf_counter()
        col = store._client().get_collection(name)
        t2 = time.perf_counter()
        vec = store.embed([q])
        t3 = time.perf_counter()
        col.query(query_embeddings=vec, n_results=min(5, col.count()))
        t4 = time.perf_counter()
        for key, value in zip(s, (ms(t0, t1), ms(t1, t2), ms(t2, t3), ms(t3, t4))):
            s[key].append(value)
    return {k: st.median(v) for k, v in s.items()}


def forward_passes(q):
    enc = ef.tokenizer.encode(q)
    real = sum(enc.attention_mask)
    f256 = feed(enc.ids, enc.attention_mask)
    freal = feed(enc.ids[:real], enc.attention_mask[:real])
    variants = [
        ("chroma256", lambda: ef.model.run(None, f256)),
        ("chromareal", lambda: ef.model.run(None, freal)),
        ("cpu256", lambda: cpu_only.run(None, f256)),
        ("cpureal", lambda: cpu_only.run(None, freal)),
    ]
    for _, fn in variants:
        fn()  # warm-up, discarded
    s = {key: [] for key, _ in variants}
    for i in range(N):
        for key, fn in variants[i % 4:] + variants[: i % 4]:   # rotate the order
            t0 = time.perf_counter()
            fn()
            s[key].append(ms(t0, time.perf_counter()))
    cos_pad = float((pooled(ef.model, f256) * pooled(ef.model, freal)).sum())
    cos_prov = float((pooled(ef.model, f256) * pooled(cpu_only, f256)).sum())
    return real, {k: st.median(v) for k, v in s.items()}, cos_pad, cos_prov


def cpu_per_wall(fn):
    """CPU-seconds used per wall-clock second: about 1 means one core busy."""
    fn()
    w, c = time.perf_counter(), time.process_time()
    for _ in range(N):
        fn()
    return (time.process_time() - c) / (time.perf_counter() - w)


def one_run(k):
    say(f"## Run {k}")
    say()
    for line in conditions():
        say(line)
    say()
    say(f"### A. `store.search()` and its three steps (median ms, {N} iterations)")
    say()
    say("| Question | `store.search()` | client + `get_collection` | `store.embed` (the question) | `count` + `query` (lookup) | embed share of the three steps |")
    say("|---|---|---|---|---|---|")
    for q in QS:
        r = split_search(q)
        share = r["embed"] / (r["client"] + r["embed"] + r["lookup"])
        say(f"| {q} | {r['search']:.1f} | {r['client']:.1f} | {r['embed']:.1f} | {r['lookup']:.1f} | {share:.0%} |")
    say()
    say(f"### B. One forward pass of the embedding model (median ms, {N} iterations, order rotated)")
    say()
    say("| Question | tokens | chromadb providers, padded to 256 | chromadb providers, unpadded | CPU provider only, padded to 256 | CPU provider only, unpadded | cos(padded, unpadded) | cos(chromadb providers, CPU only) |")
    say("|---|---|---|---|---|---|---|---|")
    for q in QS:
        real, r, cos_pad, cos_prov = forward_passes(q)
        say(f"| {q} | {real} | {r['chroma256']:.1f} | {r['chromareal']:.1f} | {r['cpu256']:.1f} | {r['cpureal']:.1f} | {cos_pad:.6f} | {cos_prov:.6f} |")
    say()
    enc = ef.tokenizer.encode(QS[0])
    f256 = feed(enc.ids, enc.attention_mask)
    say("### C. CPU-seconds used per wall-clock second during a padded forward pass")
    say()
    say("| chromadb providers | CPU provider only |")
    say("|---|---|")
    say(f"| {cpu_per_wall(lambda: ef.model.run(None, f256)):.2f} | {cpu_per_wall(lambda: cpu_only.run(None, f256)):.2f} |")
    say()


if __name__ == "__main__":
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    say("# Criterion 5 — where the retrieval time goes (diagnosis)")
    say()
    say("One-off measurement for the Diagnoses section. It times `store.py::search` "
        "and the three steps inside it with the repo's own `store` module; it is not "
        "part of the system and changes nothing in it. Everything being compared is "
        "timed inside the same loop iteration so it all sees the same machine load, "
        f"and each figure is the median of {N} iterations after a discarded warm-up. "
        f"Measured {runs} times, in the same condition as the run log: battery, "
        "Low Power Mode on, no apps closed. The script is listed at the bottom.")
    say()
    say(f"- Machine: {sh('sysctl', '-n', 'machdep.cpu.brand_string').strip()}, "
        f"{sh('sysctl', '-n', 'hw.ncpu').strip()} cores; onnxruntime {ort.__version__}")
    say(f"- Providers on the embedder's session, as chromadb sets them: `{ef.model.get_providers()}`")
    say(f"- chromadb's tokenizer pads every input to "
        f"{len(ef.tokenizer.encode('x').ids)} tokens")
    say()
    for k in range(1, runs + 1):
        one_run(k)
    say("## The script")
    say()
    Path(sys.argv[1]).write_text(
        "\n".join(out + ["```python", Path(__file__).read_text().rstrip(), "```", ""]),
        encoding="utf-8",
    )
    print(f"\nwrote {sys.argv[1]}")
```
