Highlights:
   - **Intermediate representation**
      - Experimental real function support (Stage 1) (#2306) (by **xumingkuan**)
   - **Language and syntax**
      - Add ti.sym_eig for 2x2 matrices (#2328) (by **Robslhc**)
      - Add ti.eig for 2x2 matrices (#2303) (by **Robslhc**)
   - **LLVM backend (CPU and CUDA)**
      - Add random seed support (#2297) (by **Andrew Sun**)
   - **IR optimization passes**
      - Simplify multiplying/dividing POT (#2332) (by **xumingkuan**)

Full changelog:
   - [IR] Experimental real function support (Stage 1) (#2306) (by **xumingkuan**)
   - [Opt] Simplify multiplying/dividing POT (#2332) (by **xumingkuan**)
   - [Lang] Add ti.sym_eig for 2x2 matrices (#2328) (by **Robslhc**)
   - [perf] Loop-invariant code motion (#2323) (by **Bob Cao**)
   - fix potential bug in test_eig.py (#2329) (by **Robslhc**)
   - [example] Colored triangle rasterizer (#2315) (by **Bob Cao**)
   - [doc] Windows uses backslash for filepath (#2319) (by **Bob Cao**)
   - [gui] Set DPI awareness context to per-monitor-aware to create pixel perfect windows without system scaling. (#2320) (by **Bob Cao**)
   - doc: wrap `for` to avoid confusion (#2322) (by **Ravenclaw-OIer**)
   - [ir] Make BLSAnalyzer testable (#2294) (by **Ye Kuang**)
   - [lang] Add rescale_index() and test (#2313) (by **Kenneth Lozes**)
   - [bugfix] Protect against path with space. (#2318) (by **Bob Cao**)
   - [LLVM] Add random seed support (#2297) (by **Andrew Sun**)
   - [Lang] Add ti.eig for 2x2 matrices (#2303) (by **Robslhc**)
   - support diffRange multiplication (#2310) (by **Kenneth Lozes**)
