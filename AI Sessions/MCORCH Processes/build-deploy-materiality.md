# SOP: Build & Deploy Materiality (Frontend · Edge · DB)

**Status:** ACTIVE · v1.0 · 2026-05-30
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Laws:** Lei 1 (Materialidade) + Lei 2 (Processo Antecipado). Nasce de um falso-sucesso real
de deploy (2026-05-30): `bun run build` rodado num **worktree** escreveu no `dist/` do worktree —
NUNCA no `dist/` servido pelo nginx — e ainda sem `.env` (bundle sem Supabase). "Deployed" foi
declarado sem verificar o **artefato servido**. Esta SOP transforma esse erro em anticorpo.

---

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (ou o subagent `build-deploy-guardian`)
- **Reviewer:** Sovereign (confirma o hard-refresh / valida visualmente)
- **Owner:** Sovereign (blast radius = produção `login.mcorch.com` + atribuição/UX do Usuário Zero)

---

## ⚠️ As duas armadilhas que causaram o falso-sucesso

1. **Worktree dist ≠ nginx dist.** O nginx serve **`/home/gcrUX/htdocs/constellation-orchestra/dist`**
   (repo PRINCIPAL). Uma sessão roda num worktree (`.../.claude/worktrees/<slug>/`). `bun run build`
   ali gera `<worktree>/dist/` — que **ninguém serve**. O CLAUDE.md "build = deploy" só vale no repo principal.
2. **Worktree não tem `.env`.** Vite embute `VITE_*` em build-time. Sem `.env`, o bundle sai **sem
   `VITE_SUPABASE_URL`/key** → app carrega mas **não conecta ao Supabase**. Deploy desse bundle = pior que nada.

---

## Surfaces de deploy (3 caminhos distintos)

| Surface | Como deploya | Materialidade (prova) |
|---------|--------------|------------------------|
| **Frontend** | build → `dist/` servido pelo nginx (repo principal) | bundle no `main/dist` referencia o chunk novo + tem env baked |
| **Edge Functions** | `npx supabase functions deploy <fn> [--no-verify-jwt]` | output `script size: NkB` + `Deployed Functions on project <ref>` |
| **DB (migrations)** | `npx supabase db push` (+ `/security-review` antes do commit) | output do push + query material confirmando o schema |

---

## Sequence — Frontend deploy (a partir de um worktree)

**Path A — Durável (preferido quando o branch vai pro main):**
1. `git push` do branch + merge no `main`.
2. `cd /home/gcrUX/htdocs/constellation-orchestra && bun run build` (repo principal TEM `.env`).
3. nginx serve `main/dist` automaticamente. Source = artefato.

**Path B — Imediato (deploy do worktree sem mexer no git do main):**
1. `cp /home/gcrUX/htdocs/constellation-orchestra/.env <worktree>/.env` (gitignored — nunca commitar).
2. `cd <worktree> && bun run build`.
3. `rsync -a <worktree>/dist/ /home/gcrUX/htdocs/constellation-orchestra/dist/`.
4. **Registrar débito:** o `main/dist` fica à frente do source do `main` → merge do branch é obrigatório
   para durar (senão um `build` futuro no main reverte). Flag isso no handoff.

---

## Verification gates (Lei 1 — NUNCA declarar "deployed" sem TODOS verdes)

| Gate | Comando | Pass |
|------|---------|------|
| **G1 env baked** | `grep -rl "<project-ref>" /home/.../dist/assets/ \| wc -l` | `> 0` (senão bundle sem Supabase) |
| **G2 chunk novo** | `grep -roE "<Page>-[A-Za-z0-9_]+\.js" main/dist/assets/index-*.js` | hash != o anterior (mudança chegou) |
| **G3 origin serve** | `curl -s http://localhost/ -H "Host: login.mcorch.com" \| grep index-` (best-effort) | entry chunk = o novo |
| **G4 Cloudflare** | hard-refresh `Ctrl+Shift+R` no browser | origin atualizado ≠ browser vê (cache) |

**Para edge functions:** o `Deployed Functions on project <ref>` + `script size` SÃO a prova (o bundle
esbuild falha em erro de tipo/sintaxe → deploy OK ⇒ typecheck OK mesmo sem `deno` local).

---

## Recovery path
| Cenário | Detecção | Fix |
|---------|----------|-----|
| Usuário vê estado/UI antigo | chunk servido = hash velho | refazer Path A/B; confirmar G2; pedir hard-refresh (G4) |
| App não conecta Supabase | G1 = 0 files | rebuild COM `.env`; nunca servir bundle env-less |
| Build futuro no main reverteu | source main sem os commits | merge do branch no main + rebuild (Path A) |

## Success signal
G1–G4 verdes + Reviewer confirma visualmente pós hard-refresh. Edge: `supabase functions list` ACTIVE.

## Anti-patterns
- ❌ Declarar "frontend deployed" após `bun run build` no worktree sem verificar o `main/dist` servido.
- ❌ Buildar sem `.env` presente (bundle sem env).
- ❌ Confiar no chunk hash sem conferir que o `index.html`/entry servido o referencia.
- ❌ Esquecer que Cloudflare cacheia HTML → "não mudou" é cache, não deploy.

## Connection to Survival Laws
Lei 1: o artefato SERVIDO é a prova, não o comando que rodou. Lei 2: esta SOP existe porque o erro
aconteceu — todo obstáculo novo vira processo (ver CLAUDE.md "Obstacle → Synthesis").
