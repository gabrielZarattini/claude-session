# CRM Inbox FR-CRM-028: reações de emoji e omnichannel
**Date:** 2026-07-19 | **Session ID:** `0e87b092-eef3-4a4b-9429-5c24b11f9bf6`

---

## 👤 User *(03:25:20)*

<command-message>handson</command-message>
<command-name>/handson</command-name>
<command-args>Contexto: a sessão anterior selou o handoff commit 20daaee (milestone 9ad13522, malha 9190, README v6.109.0). Leia HANDOFF.md (Task State + o Record "CRM Inbox Amendment 10 — composer + realtime + ficha rica Record (2026-07-19)").

O que está VIVO em produção (não reconstruir):
- CRM Inbox composer COMPLETO: texto/template + envio de mídia (FR-CRM-025, upload owner-scoped crm-media/${uid}/outbound → action `send` modo media → Meta /media multipart; migration 20260718270000 policy storage INSERT owner-scoped + guard media_key.startsWith(uid)) + emoji picker (FR-CRM-030) + marcar-lida ✓✓-azul (FR-CRM-029, action `mark_read`).
- Recibos e swap de mídia AO VIVO: migration 20260718260000 REPLICA IDENTITY FULL em messages/conversations + merge de payload.new no useMessages (FR-CRM-013); whatsapp-webhook processa o array `statuses` → messages.status forward-only (FR-CRM-024).
- Ficha rica do lead (FR-CRM-032): migration aditiva 20260718250000 (email/company/title/notes/tags[] em leads + customer_360 estendida security_invoker); ContactPanel form editável + LeadDetailDialog; hooks useLead/updateLeadEnrichment.
- Render de location/contacts inbound (FR-CRM-027). Menu dividido CRM × Marketing (DashboardSidebar). Settings título com font-heading.
- HyperFrames mcorch-demo: lint 0/0 (removi TODO pointer-events; arquivos do host, fora do repo — não reintroduzir pointer-events:none em composição).

Trabalho a continuar (loop CRM — diretiva Sovereign "1+2+3"):
1. FR-CRM-028: envio de reação a um balão (action `reaction` no whatsapp-templates {message_id, emoji} — grátis/window-agnostic + UI hover no balão inbound). Reações inbound JÁ renderizam.
2. FR-CRM-033: registry omnichannel + UI "Conectar nova caixa" (deriva de social_accounts/meta_config; WhatsApp vivo, demais canais gated). FR-CRM-031: espelho WhatsApp toggle lazy.
3. Settings: passe MIV profundo — VOU ENVIAR o print/referência (hoje só o título foi ajustado; os cards já usam tokens). Não redesenhar no escuro.

Constraints HONESTOS (Lei 1):
- Witness E2E dos envios (mídia/emoji/marcar-lido) é do Sovereign: HMAC/token no vault + CF barra o browser de datacenter. O plumbing está provado por eszip (strings|grep) + bundle env-baked; o teste real live é meu.
- Cap de 100 edge fns → tudo é ACTION nova em whatsapp-webhook/whatsapp-templates, NUNCA fn nova (NFR-CRM-005). Deploy single-fn é isento do cap; eszip é binário (verificar com strings|grep, o "No change found" do CLI mente).
- Bucket crm-media é privado; cliente escreve só sob ${uid}/. Toda migration nova → /security-review obrigatório.
- Reuso à la HyperFrames p/ CRM = decidido NÃO (OTD-CRM-001: ecossistema inbox open-source é AGPL contaminante; caminho = soberano nativo estendendo marketing-hub). Chatwoot só referência clean-room.
- Fatia 3 (agente de reply/comentários, FR-CRM-006/007/008) segue GATED no jurídico AI Act Art.50 (prazo 2026-08-02).

Diretivas de operação:
- TETO DE CONTEXTO ~70%, então /handoff. Medir com bun run .claude/scripts/session-inspect.ts.
- Mão na massa, foreground — evitar workflows de fundo com fan-out de vários agentes.
- Commit milestone-oriented, SEM Co-Authored-By.

Pendente Sovereign (não é código): rotacionar credenciais expostas (META_APP_SECRET/EAA/IG) — lembrete critical no banner do /dashboard/admin.</command-args>

## 👤 User *(03:25:20)*

# ShakeHands — Session Pick-Up Protocol v3

Execute the ShakeHands /handson ritual for this project.

> **v3 (2026-05-08):** Added BoK Gate enforcement per MCORCH Master Execution Protocol — alert when active module work has no sealed BoK suite at `docs/bok/<slug>/`.

---

## PRE-FLIGHT (execute ALL in parallel before reading anything)

```bash
git log --oneline -7                        # recent history + commit style
git status --short                          # uncommitted changes
git diff HEAD --stat                        # change scope
npx tsc --noEmit 2>&1 | tail -20           # TypeScript strict check
docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
docker ps --filter "name=mega-brain" --format "{{.Names}}: {{.Status}}"
curl -s http://localhost:8001/api/v2/heartbeat  # Chroma API v2 health
ls docs/bok/ 2>/dev/null                    # BoK suites disponíveis
wc -l HANDOFF.md                            # total lines — drives the read-from-end offset
```

Read in parallel (HANDOFF.md uses **read-from-end strategy** — SSP-01 v6.5.0; arquivo monolítico newest-first em ~3170+ linhas, leitura completa estoura limite de 25k tokens):
- `HANDOFF.md` with `limit=71` → Task State header + FIRST ACTION FOR NEXT AGENT (sempre estável, contém summary da fase atual selada)
- `HANDOFF.md` with `offset=<total_lines - 400>` `limit=400` → últimas 1-2 Records + Pending Actions + GraphRAG State + Infrastructure + Key Files (suffix sections always at the tail)
- `CLAUDE.md` (architecture rules, data flow, key files — incluindo MCORCH Master Execution Protocol + Survival Laws link)
- `.claude/context/sprint-priorities.md` (sprint goal, 4Cs snapshot, top gaps)
- `/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md` (memory index)

> ⚠️ **Auditoria histórica de seals antigos:** usar `Read` com offset arbitrário em HANDOFF.md (fora do fluxo padrão de pickup). Ordering newest-first: seal mais antigo ≈ linha 2805, seal mais recente logo após linha 71. Cada `## <Phase> Record (YYYY-MM-DD)` marca um seal. Manter o Read em chunks ≤ 400 linhas para preservar budget de tokens.

Also check for loose files in scratch/:
```bash
ls scratch/ 2>/dev/null && echo "⚠️ scratch/ has files — consider moving to .claude/scripts/db/" || echo "scratch/ clean ✅"
```

### BoK Gate check (v3 — MCORCH Master Execution Protocol)

For each BoK suite in `docs/bok/<slug>/`, verify completeness:
```bash
for slug in $(ls docs/bok/ 2>/dev/null); do
  if [ "$slug" = "security" ]; then
    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)
    missing=()
    for doc in "${required_sec[@]}"; do
      [ -f "docs/bok/security/$doc.md" ] || missing+=("$doc")
    done
    [ ${#missing[@]} -eq 0 ] && echo "✅ security — BoK complete (ciso-4-artifact)" || echo "⚠️ security — missing: ${missing[*]}"
    continue
  fi
  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)
  missing=()
  for doc in "${required[@]}"; do
    [ -f "docs/bok/$slug/$doc.md" ] || missing+=("$doc")
  done
  [ ${#missing[@]} -eq 0 ] && echo "✅ $slug — BoK complete" || echo "⚠️ $slug — missing: ${missing[*]}"
done
```

If the user mentions working on a **new module / complex feature / integration / architectural change**:
- Check whether `docs/bok/<expected-slug>/` exists with all 9 docs.
- If missing: surface in the **ALERTAS** section as a critical block per CLAUDE.md MCORCH Master Execution Protocol.
- Recommend `/bok-scribe <idea summary>` before any code is written.

---

## BRIEF OUTPUT

After gathering all context, produce a structured brief in **Portuguese (Brasil)**:

```
═══════════════════════════════════════════════════════════
  HANDSON — <FASE SELADA> (<data do último seal>)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: <nome da última fase — do Task State header>
  Últimos commits:
    <hash> — <mensagem>
    <hash> — <mensagem>
    <hash> — <mensagem>

📂 MUDANÇAS PENDENTES
  <lista de arquivos M/?? com descrição do que contém, ou "Worktree limpo ✅">

🏗️ INFRA
  mcorch_chroma:     <status> — Chroma API: <OK / ERRO>
  mcorch_claude_mem: <status>
  mega-brain-*:      <status resumido>

🧠 KNOWLEDGE MESH
  <totalNodes> nós · <totalEdges> arestas (fonte: HANDOFF.md GraphRAG State)
  Top tipos: <milestone:N · architecture:N · decision:N ...>

🔧 TYPESCRIPT
  <"Zero erros ✅" ou lista dos erros críticos>

📚 BoK SUITES (v3 — MCORCH Master Execution Protocol)
  Sealed: <list of docs/bok/<slug>/ com 9 docs completos>
  Incomplete: <slugs com docs faltando ou "nenhum">
  Mesh seal nodes:
    <slug> → <node_id> (stability X.XX)

⚠️ **GATE alert:** se sessão tocar módulo significativo sem BoK selada,
    listar como bloqueador crítico e sugerir /bok-scribe antes de qualquer commit.

📌 SPRINT
  Goal: <Sprint Goal de sprint-priorities.md, ou "⚠️ Sprint goal não definido — rode /audit">
  Top gap: <Gap #1 da seção "Top 3 Gap Closures", ou "não definido">

⚡ PRÓXIMOS PASSOS (prioridade)
  1. <item de maior prioridade do Pending Actions — com contexto de por que é urgente>
  2. <segundo item>
  3. <terceiro item>

⚠️ ALERTAS
  <containers unhealthy, TS errors, uncommitted changes que conflitam, scratch/ com arquivos, ou "Nenhum alerta ✅">

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

---

## Rules

- **TypeScript errors → report immediately.** If there are TS errors, list them under ALERTAS. Do not start implementing new features until errors are resolved (unless the user explicitly asks to proceed despite errors).
- **Unhealthy containers → report with triage.** Suggest the fix command if known (e.g., `docker compose restart mcorch-vector-engine` for chroma).
- **Uncommitted changes → describe, do not commit.** Only describe what exists in the working tree; committing is the user's call.
- **Keep the brief tight.** No padding. No repetition of CLAUDE.md architecture. The user already knows the architecture — they need the delta: what changed, what's broken, what's next.
- **Pending Actions priority order:** CRITICAL (before first client) > NON-CRITICAL > Phase Zeta > Core v3 > Epsilon v9.
- **Knowledge Mesh numbers:** use `GraphRAG State` section from HANDOFF.md as the source. Do not invent counts.


ARGUMENTS: Contexto: a sessão anterior selou o handoff commit 20daaee (milestone 9ad13522, malha 9190, README v6.109.0). Leia HANDOFF.md (Task State + o Record "CRM Inbox Amendment 10 — composer + realtime + ficha rica Record (2026-07-19)").

O que está VIVO em produção (não reconstruir):
- CRM Inbox composer COMPLETO: texto/template + envio de mídia (FR-CRM-025, upload owner-scoped crm-media/${uid}/outbound → action `send` modo media → Meta /media multipart; migration 20260718270000 policy storage INSERT owner-scoped + guard media_key.startsWith(uid)) + emoji picker (FR-CRM-030) + marcar-lida ✓✓-azul (FR-CRM-029, action `mark_read`).
- Recibos e swap de mídia AO VIVO: migration 20260718260000 REPLICA IDENTITY FULL em messages/conversations + merge de payload.new no useMessages (FR-CRM-013); whatsapp-webhook processa o array `statuses` → messages.status forward-only (FR-CRM-024).
- Ficha rica do lead (FR-CRM-032): migration aditiva 20260718250000 (email/company/title/notes/tags[] em leads + customer_360 estendida security_invoker); ContactPanel form editável + LeadDetailDialog; hooks useLead/updateLeadEnrichment.
- Render de location/contacts inbound (FR-CRM-027). Menu dividido CRM × Marketing (DashboardSidebar). Settings título com font-heading.
- HyperFrames mcorch-demo: lint 0/0 (removi TODO pointer-events; arquivos do host, fora do repo — não reintroduzir pointer-events:none em composição).

Trabalho a continuar (loop CRM — diretiva Sovereign "1+2+3"):
1. FR-CRM-028: envio de reação a um balão (action `reaction` no whatsapp-templates {message_id, emoji} — grátis/window-agnostic + UI hover no balão inbound). Reações inbound JÁ renderizam.
2. FR-CRM-033: registry omnichannel + UI "Conectar nova caixa" (deriva de social_accounts/meta_config; WhatsApp vivo, demais canais gated). FR-CRM-031: espelho WhatsApp toggle lazy.
3. Settings: passe MIV profundo — VOU ENVIAR o print/referência (hoje só o título foi ajustado; os cards já usam tokens). Não redesenhar no escuro.

Constraints HONESTOS (Lei 1):
- Witness E2E dos envios (mídia/emoji/marcar-lido) é do Sovereign: HMAC/token no vault + CF barra o browser de datacenter. O plumbing está provado por eszip (strings|grep) + bundle env-baked; o teste real live é meu.
- Cap de 100 edge fns → tudo é ACTION nova em whatsapp-webhook/whatsapp-templates, NUNCA fn nova (NFR-CRM-005). Deploy single-fn é isento do cap; eszip é binário (verificar com strings|grep, o "No change found" do CLI mente).
- Bucket crm-media é privado; cliente escreve só sob ${uid}/. Toda migration nova → /security-review obrigatório.
- Reuso à la HyperFrames p/ CRM = decidido NÃO (OTD-CRM-001: ecossistema inbox open-source é AGPL contaminante; caminho = soberano nativo estendendo marketing-hub). Chatwoot só referência clean-room.
- Fatia 3 (agente de reply/comentários, FR-CRM-006/007/008) segue GATED no jurídico AI Act Art.50 (prazo 2026-08-02).

Diretivas de operação:
- TETO DE CONTEXTO ~70%, então /handoff. Medir com bun run .claude/scripts/session-inspect.ts.
- Mão na massa, foreground — evitar workflows de fundo com fan-out de vários agentes.
- Commit milestone-oriented, SEM Co-Authored-By.

Pendente Sovereign (não é código): rotacionar credenciais expostas (META_APP_SECRET/EAA/IG) — lembrete critical no banner do /dashboard/admin.

## 🤖 Claude *(03:25:26)*

<details>
<summary>💭 Thinking Process</summary>

I'm starting the handshake protocol by running the pre-flight bash commands in parallel, then I'll read through the key files.

</details>


## 🤖 Claude *(03:25:26)*

Vou executar o ritual ShakeHands /handson. Começo com o pre-flight completo em paralelo.

## 🤖 Claude *(03:25:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7",
  "description": "Recent commit history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 20daaee docs(handoff): seal CRM Inbox Amendment 10 — composer completo + swap/recibos ao vivo + ficha rica (malha 9190)
> 0629280 docs(readme): v6.109.0 — CRM Inbox Amendment 10 composer completo + swap/recibos ao vivo (malha 9190)
> 37863f0 feat(crm-inbox): render de localização e contatos inbound (FR-CRM-027)
> db1763e feat(crm-inbox): envio de mídia no composer (FR-CRM-025 — anexo owner-scoped → Meta)
> b31c062 style(settings): título com a serifa de marca (font-heading) — consistência MIV com o inbox
> 0b2b244 feat(crm-inbox): marcar como lida ao abrir a thread — ✓✓ azul p/ o contato (FR-CRM-029)
> dc8533b feat(crm-inbox): emoji picker no composer (FR-CRM-030)
> ```

## 🤖 Claude *(03:25:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status --short",
  "description": "Uncommitted changes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(03:25:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff HEAD --stat",
  "description": "Change scope"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(03:25:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker mesh health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 3 days (healthy)
> mcorch_claude_mem: Up 4 weeks (healthy)
> mcorch_chroma: Up 4 weeks (healthy)
> ---
> mega-brain-dashboard: Up 4 weeks
> mega-brain-webhook: Up 4 weeks (healthy)
> mega-brain-daemon: Up 4 weeks (healthy)
> ```

## 🤖 Claude *(03:25:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat; echo \"\"",
  "description": "Chroma API v2 health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1784431529313292647}
> ```

## 🤖 Claude *(03:25:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"WARN scratch has files\" || echo \"scratch clean\"; echo \"--- HANDOFF lines ---\"; wc -l HANDOFF.md",
  "description": "BoK suites, scratch, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> agentic-governance
> agentic-workspace
> aios-sql-bridge
> authenticated-browser-operator
> avatar-clone-ai
> canvas-design
> constellation-v2
> content-intel
> content-provenance
> conteudo-v2
> crm-inbox
> e2e-user-zero
> gamificacao-nodes
> identity-fabric
> landing-factory
> marketing-hub
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> post-engine
> predictive-swarm
> security
> spaces-cadence
> spaces-evolution
> tiktok-login
> video-repurpose
> video-studio
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> youtube-studio
> --- scratch ---
> WARN scratch has files
> --- HANDOFF lines ---
> 10374 HANDOFF.md
> ```

## 🤖 Claude *(03:25:36)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the scratch directory and reading through HANDOFF.md to understand the current task state and priorities, starting with the first 71 lines for context and then jumping to the end for recent records. I'll also run a TypeScript check and review the sprint priorities in parallel.

</details>


## 🤖 Claude *(03:25:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null",
  "description": "Inspect scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxrwxr-x  2 gcrUX gcrUX 4096 Jun 30 01:44 .
> drwxrwx--- 33 gcrUX gcrUX 4096 Jul 19 00:16 ..
> ```

## 🤖 Claude *(03:25:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(03:25:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 71
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (26288 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(03:25:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9974,
  "limit": 400
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (26961 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(03:25:45)*

<details>
<summary>💭 Thinking Process</summary>

The TypeScript compiler passed without errors, so now I need to work through the HANDOFF.md file more systematically since it's quite large. I'll start by reading the first section in smaller chunks and then examine the tail end more carefully to get a complete picture.

</details>


## 🤖 Claude *(03:25:45)*

TSC limpo (zero erros). HANDOFF.md tem 10374 linhas — vou ler em chunks menores.

## 🤖 Claude *(03:25:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 55
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (25351 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(03:25:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 56,
  "limit": 200
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 56	
> 57	Sessão-loop GO'd pelo Sovereign para "terminar de implantar tudo sobre o CRM completo". Probe-first respondeu a pergunta-âncora (reuso à la HyperFrames) com a pesquisa já selada: **NÃO** — o ecossistema inbox open-source é AGPL contaminante; o caminho é código soberano estendendo o módulo nativo (Chatwoot só referência clean-room). Drenou o composer do inbox a **completo** + fechou o caveat de realtime na **raiz**. Disciplina de materialidade: cada slice provado por migration aplicada+verificada, eszip deployado (`strings|grep`), bundle env-baked, e E2E DB zero-resíduo na ficha. Honestidade Lei 1: os envios reais à Meta (mídia/mark-read) e o visual das telas são **cérebro-sem-mãos** (HMAC/token no vault + CF barra o browser de datacenter) → witness do Sovereign.
> 58	
> 59	| Ação | Resultado |
> 60	|------|-----------|
> 61	| migration `20260718250000` + `useLeads.ts` + `ContactPanel`/`LeadDetailDialog` | ✅ Ficha rica do lead FR-CRM-032 (email/company/title/notes/tags[]); `customer_360` estendida; E2E DB zero-resíduo |
> 62	| migration `20260718260000` + `useConversations.ts` | ✅ FR-CRM-013 REPLICA IDENTITY FULL + merge `payload.new` → swap/recibos ao vivo |
> 63	| `supabase/functions/whatsapp-webhook/index.ts` | ✅ FR-CRM-024 processa `statuses` → `messages.status` forward-only tenant-scoped |
> 64	| `supabase/functions/whatsapp-templates/index.ts` + migration `20260718270000` + `useSendMessage`/`MessageComposer` | ✅ FR-CRM-025 envio de mídia owner-scoped→Meta /media + FR-CRM-029 `mark_read` + FR-CRM-030 emoji |
> 65	| `ThreadView.tsx` | ✅ FR-CRM-027 render de location (link mapa) + contacts (vCard) |
> 66	| `DashboardSidebar.tsx` + `SettingsPage.tsx` | ✅ Menu CRM×Marketing + Settings título font-heading |
> 67	| `~/.mcorch/video-studio/projects/mcorch-demo/*` (host) | ✅ HyperFrames lint 0/0 (0.7.22 Studio + 0.7.64) |
> 68	
> 69	| Commit | Conteúdo |
> 70	|--------|----------|
> 71	| `8d05fdd` | feat(crm-inbox): ficha rica do lead no painel de contato |
> 72	| `e4db1fc` | feat(nav): separa "Conteúdo & Campanhas" em CRM e Marketing |
> 73	| `f92b3a8` | fix(crm-inbox): swap/recibos ao vivo (REPLICA IDENTITY FULL + merge) |
> 74	| `c621f7d` | feat(crm-inbox): recibos de entrega (FR-CRM-024 statuses) |
> 75	| `dc8533b` | feat(crm-inbox): emoji picker (FR-CRM-030) |
> 76	| `0b2b244` | feat(crm-inbox): marcar como lida ✓✓-azul (FR-CRM-029) |
> 77	| `b31c062` | style(settings): título font-heading MIV |
> 78	| `db1763e` | feat(crm-inbox): envio de mídia (FR-CRM-025) |
> 79	| `37863f0` | feat(crm-inbox): render location/contacts inbound (FR-CRM-027) |
> 80	| `0629280` | docs(readme): v6.109.0 |
> 81	
> 82	**Prova material:** 4 migrations aplicadas+verificadas (colunas/policy/replica-identity via SQL Management API); eszips deployados contêm `FR-CRM-024`/`mark_read`/`FR-CRM-025`/`OUTBOUND ATTACHMENT` (`strings|grep`); bundles env-baked com os strings novos; E2E DB da ficha write→view→delete residue=0; HyperFrames `npx hyperframes@0.7.22 lint` = 0/0. milestone `9ad13522` · malha 9190.
> 83	
> 84	---
> 85	
> 86	## CRM Fatia A + AI Act Fatia 2 + Inbox WhatsApp×MIV — ATIVADOS & WITNESSED Record (2026-07-18)
> 87	
> 88	**ORO:** Operator = MCORCH Master Execution Agent (+subagents) · Reviewer = `/security-review` (NO FINDINGS ×2) + Sovereign (witness ao vivo + GO do cert) · Owner = Sovereign (blast radius: número WhatsApp LIVE +39, PII/LGPD, deadline AI Act, marcação legal em prod).
> 89	
> 90	Sessão-loop GO'd pelo Sovereign para atacar a fila (alertas + próximos passos) e depois evoluir a UI. Probe-first fechou 3 itens já-prontos sem retrabalho (swarm:read já em prod, witness Cadência já selado no `885fa77`, UI de rotação já fiada). Os 2 grandes — CRM ingest de mídia e AI Act C2PA — foram levados de código a **produção ATIVA + witnessed** junto com o Sovereign. A Fatia 2 do C2PA foi ligada com cert self-signed (beachhead aceito, OTD-CP-012), dando à **voz seu primeiro marcador machine-readable do AI Act**. Fechou com a UI do inbox re-skinada ao MIV no espírito WhatsApp + painel de perfil do lead. Disciplina de materialidade pegou 2 falsos-sucessos (o "No change found" do deploy do webhook, provado pelo eszip; e o cert, provado com sign+verify antes de fiar no daemon).
> 91	
> 92	| Ação | Resultado |
> 93	|------|-----------|
> 94	| `scripts/crm-media-bridge.ts` + `scripts/lib/fetch-public-url.ts` + webhook enqueue + migration `20260718240000` | ✅ CRM Fatia A: worker host, SSRF-safe Bearer-só-Meta, ATIVADO (systemd) + witness real (image/video/audio `→ stored`, 0 falhas) |
> 95	| `scripts/provenance/embed-c2pa-core.ts` + `scripts/provenance-bridge.ts` + cert self-signed + drop-in systemd | ✅ AI Act Fatia 2 C1 C2PA ATIVADO cert-gated; 3 assets de voz `embedded layers=[c2pa]`; WAV real c2patool `validation_state=Valid` |
> 96	| `src/components/inbox/{ThreadView,ConversationList,ContactPanel}.tsx` + `InboxPage` + `MessageComposer` | ✅ Inbox WhatsApp×MIV (balões/recibos/avatares/malha, tokens MIV) + painel de contato (nome editável, funil, galeria de mídias) |
> 97	| Alertas: branches OpenClaw · swarm:read · lembrete rotação · witness Cadência | ✅ deletadas · já em prod · `admin_reminders` critical semeado · smoke 7/7 |
> 98	| `public/brand/inbox-mockup.png` | ✅ mockup de referência gerado via BYOK Nano Banana + prompt reusável entregue |
> 99	
> 100	| Commit | Conteúdo |
> 101	|--------|----------|
> 102	| `ab86778` | feat(crm-inbox): Fatia A — ingest de mídia inbound do WhatsApp (worker + enqueue + render) |
> 103	| `ca7bffd` | feat(content-provenance): Fatia 2 — camada C1 C2PA (imagem/vídeo/voz) cert-gated |
> 104	| `65b48b5` | feat(crm-inbox): UI WhatsApp × MIV — balões/recibos/avatares + painel de contato do lead |
> 105	
> 106	**Prova material:** eszip do `whatsapp-webhook` deployado contém `wa_media`/`media_status` (`strings|grep`); worker log `→ stored` (image/jpeg 111KB · video/mp4 4.3MB · audio/ogg); C2PA smokes 10/10 + pii-reject 4/4 + IPTC regressão 6/6; WAV de voz real `6ca26b59` → c2patool `validation_state=Valid` digitalSourceType=trainedAlgorithmicMedia; build inbox env-baked + `Dados do contato`/`ContactPanel` no bundle. milestone `e29f0f52` embedado 768d · malha 9185.
> 107	
> 108	## CRM Inbox Fatia 1/2 + witness E2E + rich-media foundation Record (2026-07-18, FORK)
> 109	
> 110	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` (2× NO FINDINGS) + Sovereign (witness E2E ao vivo) · Owner = Sovereign (blast radius: número WhatsApp LIVE +39, dados de contatos/PII LGPD, custo per-message).
> 111	
> 112	Sessão-fork (a original estourou 2M de janela de contexto). Retomou o trabalho de CRM Inbox que o outro modelo declarou "concluído" mas estava materialmente **DOA** — o gate de review (4 revisores adversariais) + um smoke novo + `/security-review` expuseram bugs bloqueantes que o "tsc exit 0" não via (o `tsc` da raiz é no-op; o gate real é o `vite build`). Corrigido, verificado, selado; witness E2E do WhatsApp passou; evolução governada (Amendment 10 + Fatia A/B fundação) iniciada. Trabalho do Pantheon (OpenClaw) integrado.
> 113	
> 114	| Ação | Resultado |
> 115	|------|-----------|
> 116	| `src/pages/InboxPage.tsx` + hooks `useConversations`/`useSendMessage`/`useTemplates` + componentes inbox | ✅ Página corrigida (default export, shapes de hook, mutateAsync, MIV, pt-BR); build verde (chunk `InboxPage`) |
> 117	| `supabase/functions/whatsapp-templates/index.ts` (action `send`) | ✅ Money-path corrigido (`deduct_mco_coins` void/params reais; refund idempotente); window-gate 409 + consent 403 server-side; categoria resolvida na WABA; `to` da thread |
> 118	| `supabase/functions/whatsapp-webhook/index.ts` | ✅ `content_type` mapeado ao CHECK (tipos WA não-mapeados não descartados) |
> 119	| `supabase/migrations/20260718210000_crm_inbox_guard_fix.sql` | ✅ Guard `auth.role()` (o `request.jwt.claim.role` vazio bloqueava o service-role — webhook quebraria no 2º inbound) |
> 120	| `supabase/migrations/20260718230000_crm_inbox_rich_media_status.sql` | ✅ Fundação rich-media: colunas status/mídia/reação + bucket privado `crm-media` owner-scoped |
> 121	| `scripts/qa/smoke-crm-inbox.ts` | ✅ 12/12 (cross-tenant · dedup · append-only · window client-proof · service-role exempt · FK · erasure) |
> 122	| `docs/bok/crm-inbox/{01..09}` + `10-amendment-rich-media-omnichannel.md` + `docs/processes/crm-inbox-window-state.md` | ✅ BoK 9/9 selada + Amendment 10 + SOP Lei 2 |
> 123	| `src/hooks/useConversations.ts` (`useMessages`) | ✅ Realtime da thread (subscription própria por `conversation_id`) |
> 124	| Witness E2E WhatsApp (Sovereign) | ✅ PASSOU — causa raiz `META_APP_SECRET` defasado (`invalid_signature`); trocado o App Secret → inbound flui |
> 125	| `HEARTBEAT.md` + `scripts/validate-wiki-links.ts` (OpenClaw) | ✅ Integrado; validador teve o erro de sintaxe corrigido |
> 126	
> 127	| Commit | Conteúdo |
> 128	|--------|----------|
> 129	| `e47dc93` | fix(crm-inbox): Fatia 1/2 — página funcional + money-path seguro + guard corrigido |
> 130	| `d6e21a3` | chore(crm-inbox): seal BoK 9/9 na malha (Phase 7) |
> 131	| `3cc80c7` | fix(crm-inbox): thread atualiza em tempo real (subscription própria no useMessages) |
> 132	| `853dfb0` | docs(crm-inbox): Amendment 10 — rich media/recibos/reações + omnichannel + espelho oficial |
> 133	| `df50024` | feat(crm-inbox): Fatia A/B fundação — colunas status/mídia/reação + bucket privado crm-media |
> 134	| `9eccf37` | fix(scripts): validate-wiki-links roda (corrige sintaxe do contributo OpenClaw) |
> 135	| `5f7f441` | docs(readme): v6.108.0 — CRM Inbox WhatsApp E2E ✓ + BoK 9/9 + rich-media foundation |
> 136	
> 137	**Malha:** milestone `973d249d-cb98-4d40-a5b3-c830b294e528` (handoff, embedado 768d) · seal BoK `2dff4a5a-bf4c-482e-972a-d960d7f338b5` (documentation_suite) · total **9165** nós.
> 138	
> 139	**Survival Laws Self-audit:** Lei 1 ✅ (todo SUCCESS ancorado — smoke 12/12, /security-review, build verde, HTTP dos deploys, UUIDs reais; o witness foi prova ocular do Sovereign; nenhuma fabricação — a contradição do eszip-grep foi resolvida via `strings`). Lei 2 ✅ (SOP `crm-inbox-window-state.md` + Amendment 10 antes do código das fatias). Lei 3 ✅ (poda contínua; sessão-fork por estouro de 2M). Lei 4 ✅ (ORO declarado).
> 140	
> 141	---
> 142	
> 143	## Meta app-review privacidade + WhatsApp rail E2E + AI Act badge/reframe + CRM seed Record (2026-07-18)
> 144	
> 145	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` (SOUND/NO FINDINGS em 4 fns credential-touching) + Vision-agnostic reviewers focados · Owner = Sovereign (decisões ao vivo: colar tokens no console Meta, autorizar o número de teste BR +55…, GO da deepresearch do CRM).
> 146	
> 147	Sessão-maratona interativa iniciada pelo `/handson` + GO "todos os próximos passos" e drenada ao longo de um dia inteiro com o Sovereign ao vivo no console do Meta (app-review, WhatsApp, tokens). Fechou o rail de WhatsApp ponta-a-ponta, o endpoint de privacidade do app-review, a Fatia 2 da proveniência (surfacing) e semeou o módulo CRM. Console de dev do Meta provou-se **não-automatizável** para *commits* de config (screenshots/injeção de script timeout, refs invalidam) — reads via JS funcionam; adds de use-case o Sovereign fez nativo. Selada por `/handoff`.
> 148	
> 149	| Ação | Resultado |
> 150	|------|-----------|
> 151	| `supabase/functions/meta-privacy/index.ts` + `supabase/functions/_shared/meta-signed-request.ts` + migration `20260717120000` | ✅ Deauth + data-deletion callbacks do Meta (signed_request HMAC fail-closed); smoke 4/4 live |
> 152	| `supabase/functions/connect-instagram-token/index.ts` + `InstagramTokenCard` | ✅ Colar token IG manual → `social_accounts` (Caminho 1), validado no /me |
> 153	| `whatsapp-webhook` config.toml `verify_jwt=false` | ✅ **Fix: rail inbound estava morto** (gateway 401ava o Meta); smoke handshake 200/403/401 |
> 154	| `meta_config` WhatsApp wiring (`MetaConfigCard` + `useMetaConfig`) + `POST subscribed_apps` | ✅ Inbound 100% fiado (token EAA + CLOUD_API/LIVE + app inscrito na WABA) |
> 155	| `whatsapp-templates` (list/create/delete/**send**) + `WhatsappTemplatesCard` + `WhatsappSendCard` | ✅ Gestão de templates + envio no dashboard; template E2E provado; send plumbing provado até o Meta |
> 156	| `provenance.ts describeProvenance` + `ProvenanceBadge` + `reshape-pillar` re-mark | ✅ Badge AI Act (WS-C) + variante reenquadrada re-marcada (WS-D, RPN 294) |
> 157	| `docs/bok/crm-inbox/00-deepsearch-blueprint.md` | ✅ Blueprint-semente CRM/inbox (deepsearch, 24 URLs, licenças + AI Act) |
> 158	| `src/integrations/supabase/types.ts` | ✅ Regenerado do schema (estava stale por várias migrations) |
> 159	
> 160	| Commit | Conteúdo |
> 161	|--------|----------|
> 162	| `15810be` | meta-privacy — URLs deauth/exclusão de dados (app review + LGPD) |
> 163	| `afd10fa` | provenance — badge "Conteúdo gerado por IA" (WS-C) |
> 164	| `a72500c` | provenance — variante reenquadrada re-marcada (WS-D, RPN 294) |
> 165	| `b1568e6` | instagram — colar token manual → social_accounts |
> 166	| `c66bc60` | whatsapp — wiring inbound no meta_config |
> 167	| `d941208` | whatsapp-webhook — verify_jwt=false (rail inbound estava morto) |
> 168	| `c12b997` | whatsapp — gestão de templates no dashboard |
> 169	| `68f8d18` | whatsapp — envio de mensagem (template/texto livre) |
> 170	| `2de10cb` | crm-inbox — blueprint-semente deepsearch |
> 171	
> 172	### Arquitetura — WhatsApp Cloud API rail (Caminho 2)
> 173	```
> 174	Inbound:  Meta → whatsapp-webhook (verify_jwt=false + X-Hub-Signature-256)
> 175	          → resolve tenant por meta_config.whatsapp_phone_number_id/waba_id (auth.uid())
> 176	          → whatsapp_leads + nó na malha
> 177	Pré-req:  POST /{waba_id}/subscribed_apps (senão subscribed_apps:[] = webhook não dispara)
> 178	Token:    meta_config.long_lived_token = EAA (Facebook system-user), NÃO IGAA (Instagram Login)
> 179	Templates/Send: whatsapp-templates (JWT, per-user via decrypted_meta_config) → Graph API
> 180	          list/create/delete + action=send (POST /{phone_id}/messages: template | text 24h)
> 181	```
> 182	
> 183	## Credenciais globais de app + AI Act Fatia 0-1 + content-intel BoK 9/9 + wildcard gcrux.com Record (2026-07-17)
> 184	
> 185	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` (NO FINDINGS ×3) + reviewer independente (pegou bug de preserve do status + o WORKER_RESOURCE_LIMIT) + Vision QA · Owner = Sovereign (decisões: colar chaves globais, GO do backfill, DNS wildcard, gates de app-review, GO do módulo content-intel com revisão jurídica).
> 186	
> 187	Sessão-maratona interativa iniciada por diretiva do Sovereign ("os escopos Google aprovados + Pinterest aprovado, preciso colar a chave em /dashboard/admin sem .env/CLI") e drenada ao longo do dia com o Sovereign ao vivo (colando credenciais, gravando vídeos de app-review Pinterest/TikTok, otimizando o EP01 no YouTube). Fechou 5 frentes com prova material (Lei 1) e commit granular. Selada por `/handoff` explícito.
> 188	
> 189	| Frente | Resultado |
> 190	|--------|-----------|
> 191	| Tier global de credenciais (FR-PE-017..021) | ✅ Admin cola chave de app no `/dashboard/admin` sem .env; resolver 4 degraus 6 plataformas; seed env→global 6/6; smoke 13/13; `/security-review` NO FINDINGS (`9d94771`/`df98397`/`f4dd523`) |
> 192	| Pinterest/X reconectados + UI boards | ✅ credencial global (OTD-PE-SOCIAL-APPCREDS fechada); anticorpo per-user-shadow; `pinterest-boards` edge fn + card (`9214df7`) |
> 193	| AI Act Art.50 Fatia 0-1 VIVO | ✅ 5 colunas na spine + writer 26 args + ExifTool IPTC + worker; **101 assets marcados**, witness real; `/security-review` NO FINDINGS (`fa30a69`/`68d9163`/`7226717`) |
> 194	| `*.gcrux.com` wildcard | ✅ vhost servindo `hello.gcrux.com` HTTP 200 (`f462173`) |
> 195	| content-intel BoK 9/9 | ✅ módulo novo; blueprint deepsearch → Scribe 9/9; Pattern Conformance 21; seal `2e918a8c` (`91f1222`) |
> 196	| Fixes | ✅ morning-briefing security ciso-4 falso + pin repo (`3d5a2f4`); WORKER_RESOURCE_LIMIT megapixels (`42ca370`); lint herdado (`b5c5474`) |
> 197	
> 198	### Arquitetura — resolver 4 degraus de credencial de app (Amendment 16)
> 199	```
> 200	social-auth-{init,callback} + refresh-social-token (6 plataformas)
> 201	  → resolveSocialAppCreds(platform):
> 202	      (1) social_app_config per-user (auth.uid(), is_active)   ← tenant BYOK
> 203	      (2) social_app_config GLOBAL  (user_id IS NULL, is_active) ← admin /dashboard/admin (NOVO)
> 204	      (3) Deno.env fallback (legado/emergência)
> 205	      (4) SocialAppConfigError 402 { <platform>_not_configured }
> 206	  linha global = Vault-cifrada · masked view · admin-gated 2× (RLS has_role + INSTEAD OF guard composto)
> 207	```
> 208	
> 209	### Arquitetura — AI Act marcação (content-provenance Fatia 0-1)
> 210	```
> 211	render → register_creative_asset (spine creative_assets, provenance_status='pending')
> 212	  → provenance-bridge (systemd worker, molde video-bridge):
> 213	      sweep pending image/video → download bucket → embed-iptc-core (ExifTool XMP-iptcExt:DigitalSourceType)
> 214	      → verify-before-claim (relê) → re-upload in-place → UPDATE status='embedded'
> 215	  external/local EXCLUÍDOS (MCORCH não gerou → não afirmar, Lei 1)
> 216	```
> 217	
> 218	## Loop MAPE-K: UX-Explorer + landing-bundler + BoKs 9/9 retroativas + swarm:read PAT Record (2026-07-16)
> 219	
> 220	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` (NO FINDINGS na it.4) + 2 critics adversariais das BoKs + verificação mecânica independente + Vision QA ocular · Owner = Sovereign (decisões de escopo YTS, apply da migration, gates de credencial/domínio).
> 221	
> 222	Loop autônomo MAPE-K re-armado pelo Sovereign, mais o pedido paralelo de auditoria de prontidão BoK 9/9 de video-repurpose/youtube-studio. O ritual (git fetch → incidentes → Fila) rodou a cada retomada. A sessão fechou **it.0 a it.4** da diretiva 2026-07-16 + a task de idempotência dos seed scripts, tudo com prova material (Lei 1) e commit granular. Selada por `/handoff` explícito do Sovereign após a pergunta "precisamos fazer /handoff oficialmente aqui?" — ponto de parada natural (bloco coeso fechado + cluster de gates Sovereign à frente).
> 223	
> 224	| Frente | Resultado |
> 225	|--------|-----------|
> 226	| it.0 — UX-Explorer (INC-39626fcd) | ✅ 4 causas empilhadas (PATH cron · regex `/auth` · `wait` sem `--load` · sem `--state`) → 6/7 flows verdes; nunca tivera run verde antes (`50bd550`) |
> 227	| it.0 — P1 real (INC-8cba901a) | ✅ Controls ReactFlow brancos → vars `--xy-*` MIV (override de classe perde pro chunk lazy); Vision re-run APROVADO (`7a00511`) |
> 228	| it.1 — landing-bundler | ✅ FR-LF-002/003; 15/15 unit + G5 real (331B→150KB, data:image+data:font, 0 refs externas); SOP Lei 2 primeiro (`762c641`) |
> 229	| it.2 — witness cadência | ✅ 7/7 dispatch real→scheduled_posts sem publicar; fecha ressalva `c994c363` (`885fa77`) |
> 230	| it.3 — BoK video-repurpose 9/9 | ✅ critic APPROVE 0 violations; seal `a6df1548` DERIVES_FROM landing-factory |
> 231	| it.3 — BoK youtube-studio 9/9 | ✅ guarda-chuva 2 tracks (GO Sovereign); 2 violations do critic corrigidas; seal `9a923887` |
> 232	| it.4 — swarm:read PAT | ✅ migration `20260716190000` fail-closed; `/security-review` NO FINDINGS (`1b30fc3`) |
> 233	| Task idempotência | ✅ 24 seed scripts CHECK-BEFORE-INSERT; 23/23 re-run malha estável (`76e5a8a`) |
> 234	
> 235	| Commit | Conteúdo |
> 236	|--------|----------|
> 237	| `50bd550` | fix(qa): UX-Explorer enxerga — 4 causas do INC-39626fcd |
> 238	| `7a00511` | fix(ui): ReactFlow Controls MIV via --xy-* vars (INC-8cba901a) |
> 239	| `a729f83` | fix(edge): micro-reparos pré-BoK (mesh mandate youtube-data + gate Gemini-only) |
> 240	| `762c641` | feat(landing-factory): landing-bundler core (FR-LF-002/003) |
> 241	| `885fa77` | test(spaces-cadence): witness E2E de despacho 7/7 |
> 242	| `a8265eb` | docs(bok): video-repurpose + youtube-studio 9/9 retroativas |
> 243	| `0718101` | chore(mesh): seal nodes retroativos + anticorpo idempotência |
> 244	| `76e5a8a` | fix(scripts): idempotência CHECK-BEFORE-INSERT nos 13 seed seals restantes |
> 245	| `1b30fc3` | feat(predictive-swarm): swarm:read no allowlist do PAT |
> 246	
> 247	### Arquitetura landing-bundler (Fatia 1)
> 248	```
> 249	[HTML do Open Design v0.10.0 — CSS/JS de topo inlinados, refs externas soltas]
> 250	   │  bundleHtml(html, {baseUrl, guardDeps})
> 251	   ▼
> 252	[extrai refs: img/source/video/audio/link-stylesheet/script/url()/@import]
> 253	   │  p/ cada ref → resolveRef (rejeita http:/data:/blob:, upgrade //host→https)
> 254	   ▼
> 255	[fetchAsset → fetchPublicUrl]  (anti-SSRF host: re-valida CADA salto 3xx · DNS→IP privado · piso/teto/timeout)
> ```

## 🤖 Claude *(03:25:57)*

<details>
<summary>💭 Thinking Process</summary>

I'm trying to read the Task State header from the HANDOFF.md file, but the first attempt to read lines 1-55 consumed an unexpectedly large number of tokens, suggesting those lines might be unusually long. Let me try reading just the first 30 lines instead to get the information I need.

</details>


## 🤖 Claude *(03:25:57)*

Preciso do Task State header (linhas 1-55 estouraram — devem ter conteúdo denso). Vou ler em fatia menor.

## 🤖 Claude *(03:25:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 30
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# HANDOFF — MCORCH Constellation Orchestra
> 2	
> 3	## ⚡ FIRST ACTION FOR NEXT AGENT
> 4	
> 5	```bash
> 6	git log --oneline -5
> 7	# Then explore the codebase — do NOT start from the file tree
> 8	```
> 9	
> 10	---
> 11	
> 12	## Task State
> 13	
> 14	| **CRM Inbox Amendment 10 — composer completo + swap/recibos ao vivo + ficha rica do lead + menu CRM×Marketing + HyperFrames lint (2026-07-19)** | ✅ Sessão-loop GO'd (Sovereign: "1+2+3"). **10 commits `8d05fdd..37863f0` + README `0629280` + este seal.** **Reuso à la HyperFrames DECIDIDO NÃO** (OTD-CRM-001: ecossistema inbox open-source é AGPL contaminante; único MIT Chatwoot é monólito Rails; caminho = **soberano nativo** estendendo marketing-hub). **(1) Ficha rica do lead FR-CRM-032:** migration aditiva `20260718250000` (email/company/title/notes/tags[] em `leads` + GIN + `customer_360` estendida security_invoker preservado; `erase_lead` já deleta a linha ⇒ zero-residue) + form editável `ContactPanel` (chips) + `LeadDetailDialog` espelha; hooks `useLead`/`updateLeadEnrichment`; /security-review NO FINDINGS + E2E DB write→view→delete zero-resíduo. **(2) Realtime FR-CRM-013:** causa-raiz = `messages`/`conversations` em REPLICA IDENTITY **DEFAULT** → UPDATE filtrado não entregue pelo Realtime (só INSERT); fix migration `20260718260000` **REPLICA IDENTITY FULL** + merge de `payload.new` no `useMessages` — **fecha o caveat "mídia só no reload"**. **(3) Recibos FR-CRM-024:** `whatsapp-webhook` passa a processar o array `statuses` → `messages.status` (sent/delivered/read/failed) por wamid, forward-only, tenant-scoped, erro Meta em metadata. **(4) Composer completo:** emoji picker FR-CRM-030 (nativo) + marcar-lida ✓✓-azul FR-CRM-029 (action `mark_read` + trigger fire-and-forget) + **envio de mídia FR-CRM-025** (Paperclip→upload owner-scoped `crm-media/${uid}/outbound/`→action send modo `media`→Meta `/media` multipart; migration `20260718270000` policy storage INSERT owner-scoped espelha a de leitura + guard `media_key.startsWith(uid)`; window-gate 409; 0 mco; /security-review inline NO FINDINGS) + render location/contacts inbound FR-CRM-027. **(5) Menu CRM×Marketing** (`DashboardSidebar`) + Settings título → font-heading (cards já MIV). **(6) HyperFrames `mcorch-demo`** lint **0/0** em 0.7.22 (versão do Studio) E 0.7.64: `<template>`→HTML completo + `data-start` + seletores por `#id` + `overwrite:auto` + pointer-events realocado (host, fora do repo git). tsc-app só erros pré-existentes · builds verdes env-baked · eszips material-verificados (`strings\|grep`) · milestone `9ad13522` · malha **9190**. ⚠️ Pendente Sovereign: FR-CRM-028 (reações-send), FR-CRM-033 (omnichannel registry + "Conectar nova caixa"), FR-CRM-031 (espelho WhatsApp); **Fatia 3 (agente) gated AI Act Art.50 2026-08-02**; **print de Settings** p/ passe MIV profundo; **witness E2E dos envios** (mídia/mark-read) live (HMAC/token no vault = cérebro-sem-mãos p/ E2E local; plumbing provado por eszip/bundle). |
> 15	| **CRM Fatia A LIVE+WITNESSED + AI Act Fatia 2 C2PA LIVE+WITNESSED + Inbox WhatsApp×MIV + painel de contato (2026-07-18)** | ✅ Sessão-loop GO'd (fila Sovereign + evolução de UI). **3 commits `ab86778`/`ca7bffd`/`65b48b5` + este seal.** Probe-first fechou 3 itens já-prontos sem retrabalho. **(1) CRM Fatia A ATIVADO + WITNESSED E2E:** worker host `scripts/crm-media-bridge.ts` (cap de 101 edge fns → worker, não fn nova; OTD-CRM-019 resolvida) + port SSRF-safe Bun `scripts/lib/fetch-public-url.ts` (**Bearer só p/ hosts Meta**, dropado cross-host — o Deno vazaria) + enqueue no webhook + render; migration aditiva `20260718240000` aplicada; witness real (Milena: image/jpeg 111KB, video/mp4 4.3MB, audio/ogg `→ stored`, **0 falhas**). "No change found" do deploy era **falso** — provado pelo eszip deployado (`strings|grep wa_media`). **(2) AI Act Fatia 2 C1 C2PA ATIVADO + WITNESSED:** `c2patool 0.27` compilado no host aarch64 (cargo, USD=0) + motor `scripts/provenance/embed-c2pa-core.ts` cert-gated (verify-before-claim + preservar-e-anexar + só uuid opaco) + cert self-signed prod `mcorch-c2pa-es256` (GO Sovereign, OTD-CP-012 aceito) via **drop-in systemd host-only**; **voz marcada pela 1ª vez** (3 assets `embedded layers=[c2pa]`; WAV real `6ca26b59` c2patool `validation_state=Valid`). SAFE-BY-DEFAULT: sem cert → dormante. **(3) UI inbox WhatsApp×MIV** (`ThreadView`/`ConversationList`/`InboxPage`/`MessageComposer` migrados de slate/cyan cru → tokens MIV; balões+rabinho, recibos ✓✓, avatares gradiente, malha de constelação) + **painel de contato do lead** (`ContactPanel`: clique no nome → sidebar; nome editável→`leads`, etapa do funil reusa marketing-hub, galeria "Mídia, links e docs"; **validação honesta**: a Cloud API NÃO expõe foto/e-mail/endereço/horários do contato — privacidade Meta, só nome+telefone). Mockup de referência via BYOK Nano Banana + prompt reusável. **(4) Alertas:** branches OpenClaw deletadas · swarm:read já em prod · lembrete de rotação semeado (`admin_reminders` critical) · witness Cadência 7/7. 2× `/security-review` NO FINDINGS · tsc 0 (root no-op; app tsc só erros pré-existentes) · milestone `e29f0f52` embedado 768d · malha **9185**. ⚠️ Pendente Sovereign: **rotacionar credenciais expostas** (`META_APP_SECRET`/EAA/IG — lembrete no banner); **enriquecimento rico do lead** (email/empresa/notas = extensão enxuta do schema `leads` + form); **realtime do swap de mídia** (hoje retroativo/reload — aceito, fix trivial: tratar UPDATE no merge do `useMessages`); cert C2PA trust-list (upgrade opcional OTD-CP-003 = trocar arquivo do cert). |
> 16	| **CRM Inbox Fatia 1/2 corrigida+verificada · witness E2E WhatsApp ✓ · Realtime fix · Amendment 10 rich-media/omnichannel · Fatia A/B fundação (2026-07-18, FORK)** | ✅ Sessão-fork (a original estourou 2M de contexto). **9 commits `e47dc93..9eccf37` + README `5f7f441`.** O trabalho herdado do outro modelo estava **DOA**: página crashava (sem `default export`; `useMarkRead` inexistente; `useMessages` retorna `{messages,hasMore}` tratado como array → `reduce is not a function`; `useTemplates` UseQueryResult lido como `.templates`; template literal `}">` quebrado = o real "bloqueio de build" mal-atribuído ao classificador nemotron — o `tsc --noEmit` na raiz é **no-op** (`files:[]`+references), gate real = `vite build`). Money-path 402 sempre (`deduct_mco_coins` com params `p_description`/`p_metadata` inexistentes → PGRST202); gates de janela/consent puláveis omitindo `conversation_id`. **Bug BLOQUEANTE pego pelo smoke novo:** `guard_conversation_server_columns` usava `current_setting('request.jwt.claim.role')` (GUC vazio) → bloqueava ATÉ o service-role → o webhook quebraria no **2º inbound** de qualquer contato recorrente; fix = migration forward `20260718210000` (`auth.role()` NULL-safe). Tudo corrigido: `scripts/qa/smoke-crm-inbox.ts` **12/12** (cross-tenant=0 · dedup redelivery `provider_message_id` · append-only · janela client-proof · service-role exempt · FK tenant-safe · erasure zero-residue), **2× `/security-review` NO FINDINGS** (money-path + fundação rich-media), build verde, 2 edge fns deployadas in-place (`deploy fn1 fn2` bulk = **402** no cap de 100 fns → single `deploy <fn>`). **BoK crm-inbox 9/9 SELADA** (nó `2dff4a5a` DERIVES_FROM marketing-hub) + SOP `docs/processes/crm-inbox-window-state.md` + `types.ts` regenerado (conversations/messages estavam ausentes). **Witness E2E do WhatsApp PASSOU:** causa raiz do "não chega nada" = `META_APP_SECRET` defasado → `invalid_signature` HMAC em TODO inbound (a Meta entregava; logs sob `service=crm-inbox`, não `whatsapp-webhook`); Sovereign trocou o App Secret no console → mensagens fluem (+39 351 571 2281 CLOUD_API). **Realtime da thread corrigido** (`useMessages` ganha subscription `postgres_changes` própria filtrada por `conversation_id` — antes só a lista atualizava). **Amendment 10** (`10-amendment-rich-media-omnichannel.md`): rich media/recibos/reações + hub **omnichannel** (WhatsApp vivo + redes/email como canais futuros + "conectar nova caixa") + **espelho oficial WhatsApp** (toggle lazy, só WhatsApp) + matriz honesta do teto da Cloud API (mídia/status/reações SIM; foto/horários/mapa do contato NÃO — privacidade). **Fatia A/B fundação landed** (migration `20260718230000`): `messages` +`status`(✓✓)/`media_asset_path`/`media_mime`/`reaction_*` + `content_type` +video/sticker/reaction/location/contacts + bucket privado **`crm-media`** owner-scoped. **Trabalho OpenClaw (Pantheon) integrado** linearmente: heartbeat repo-health (`HEARTBEAT.md`) + wiki validator (`scripts/validate-wiki-links.ts` — corrigido erro de sintaxe do contributo `2abe650`). tsc 0 · smoke 12/12 · milestone `973d249d` embedado (768d) · malha **9165**. ⚠️ Pendente Sovereign: **continuar Fatia A** (pipeline ingest de mídia — decisão worker-vs-edge OTD-CRM-019 pelo cap de 100 fns; SSRF-safe `fetchPublicUrl`); **rotacionar** `META_APP_SECRET`/tokens EAA/IG expostos; branches OpenClaw no remoto (`feature/enhance-heartbeat-repo-health`, `feature/add-wiki-link-validator`) são **redundantes** (commits já no main via push). |
> 17	| **Meta app-review privacidade + WhatsApp rail E2E + AI Act badge/reframe + IG token manual + CRM seed (2026-07-18)** | ✅ Sessão-maratona interativa (Sovereign ao vivo no console do Meta, colando tokens, aprovando envios). **11 commits `15810be..2de10cb`.** **(1) Meta app-review — privacidade** (`meta-privacy`): contrato `signed_request` HMAC do Meta (verify_jwt=false, HMAC do app secret = única fronteira de confiança, fail-closed) roteando `deauthorize`/`data-deletion`/`status` por path; migration `20260717120000` (`meta_deletion_requests` ledger RLS default-deny + RPC `meta_erase_social_account` service-role-only espelhando `disconnect_social`, revoga Vault double-bound); `_shared/meta-signed-request.ts` (verificador multi-candidato). `/security-review` NO FINDINGS · anticorpo 7/7 · smoke 4/4 live. As 2 URLs de callback prontas p/ submissão. **(2) IG token manual** (`connect-instagram-token`, Caminho 1): valida no `graph.instagram.com/me` server-side → grava `social_accounts`; identity sempre `auth.uid()`; `/security-review` SOUND. **(3) WhatsApp Cloud API — rail E2E.** Fix decisivo: `whatsapp-webhook` sem `verify_jwt=false` no config.toml = gateway 401ava o Meta → **rail inbound estava MORTO**; + `POST /{waba}/subscribed_apps` que faltava (`subscribed_apps:[]` = webhook não dispara); + `meta_config` fiado (card WhatsApp em Settings→Meta) com token **EAA** (não IGAA — gotcha: IGAA é Instagram Login, `graph.facebook.com` rejeita)/phone_number_id `101816505976112`/WABA `112707461538251`; número provado **CLOUD_API/LIVE** via `GET /me`. **Templates** (`whatsapp-templates`: create/list/delete via Graph API, **E2E provado** create→PENDING·list·delete) + **envio** (ação `send` fundida na mesma fn — limite de edge functions atingido; template/texto livre, plumbing provado até o Meta: send real p/ +55… autentica, só falta aprovação do `promo_semana` → erro 132001). 2× `/security-review` SOUND. **(4) AI Act Fatia 2** (surfacing): badge "Conteúdo gerado por IA" (WS-C, `describeProvenance` verify-before-claim + chips por camada; 101 assets exibem o disclosure; unit 6/6) + variante reenquadrada re-marcada (WS-D, fecha RPN 294 — reframe dropava XMP; `reshape-pillar` registra na spine `pending`). **(5) CRM + Caixa de Entrada Omnichannel — blueprint-semente deepsearch** (`docs/bok/crm-inbox/`, 38.865B, 24 URLs, 14 OTD·14 FM): licenças (só Chatwoot MIT limpo; Twenty/Erxes/NocoDB AGPL contamina) · WhatsApp per-mensagem desde 2025-07-01 · agente de comentários = triagem+rascunho+gate humano (AI Act Art.50). Gate de código FECHADO até BoK 9/9 + jurídico. **types.ts regenerado** (estava stale por várias migrations, +384 linhas, superset limpo). tsc 0 · vitest **634** verde · gitleaks clean · milestone `aa4ed885` embedado (768d) · malha **9135**. ⚠️ Pendente Sovereign: aprovação Meta do `promo_semana` → testar envio real pela UI; `/bok-scribe crm-inbox` + jurídico do agente automatizado; rotação de credenciais expostas no chat (token EAA/IG). |
> 18	| **Credenciais globais de app (admin) + AI Act Fatia 0-1 VIVO + content-intel BoK 9/9 + wildcard gcrux.com (2026-07-17)** | ✅ Sessão-maratona interativa (Sovereign ao vivo colando chaves, gravando vídeos de app-review, otimizando YouTube). **12 commits `b5c5474..91f1222`.** **(1) Tier global de credenciais de app OAuth** (post-engine Amendment 16, FR-PE-017..021): o Sovereign cola as chaves secretas de app direto no `/dashboard/admin` → aba **Chaves** (sem `.env`/CLI) — linha `user_id IS NULL` cifrada no Vault, admin-gated 2× (RLS `has_role` single-arg + exemption no INSTEAD OF guard); resolver vira **4 degraus** (per-user → global → env → 402) cobrindo as 6 plataformas (LinkedIn/IG/X saem do `Deno.env` cru nos 3 estágios). Edge fn `seed-global-app-creds` seed env→global 6/6. Banner de rotação (`admin_reminders`). `/security-review` NO FINDINGS · smoke 13/13 (cross-tenant BLOCKED ao vivo: 42501/Vault-UUID/23505). **Anticorpo per-user-shadow:** linha per-user stale sombreava a global no callback Pinterest (Sovereign redefiniu o secret no console → 401 do próprio Pinterest); sonda discriminante por code-falso; fix = desativar per-user. **Pinterest `@uxandai` + X `@gabrielOrchAI` reconectados** via credencial global (OTD-PE-SOCIAL-APPCREDS fechada) + **UI de gestão de boards** no `/dashboard/social` (`pinterest-boards` edge fn) para a demo do Standard. **(2) AI Act Art.50 Fatia 0-1 VIVO** (content-provenance): migration `20260716230000` (5 colunas `provenance_*` na spine + `register_creative_asset` 21→26 args, DROP+CREATE+re-GRANT service_role, `/security-review` NO FINDINGS, bug de preserve pego pelo reviewer + corrigido/provado) + `src/lib/provenance.ts` (enum IPTC) + motor `embed-iptc-core` (ExifTool `XMP-iptcExt:DigitalSourceType`, verify-before-claim) + worker `provenance-bridge` (systemd habilitado) → **backfill 101 assets MCORCH marcados** (witness real `bc03a65a` imagem + `d57e3341` vídeo baixados do bucket carregam a URI IPTC); external/local excluídos (Lei 1). Smoke 6/6. **(3) `*.gcrux.com` wildcard VIVO** — DNS wildcard (Sovereign) + `nginx/lp.gcrux.com.conf` (symlink+reload) → `hello.gcrux.com` serve landing real HTTP 200; trilho de hosting da landing-factory operacional. **(4) content-intel BoK 9/9 selada** (módulo NOVO): usuário compartilha link de vídeo existente (IG/TikTok/YT) → resolve+analisa server-side via Vision MCP → modela estratégia. Blueprint deepsearch 5 frentes (`wf_609b48ad`) → BoK Scribe 9/9 (`wf_658b10a1`, fix stage morreu no session-limit → **resumeFromRunId** recuperou); FR-CI-001..026 · OTD-CI-001..008 · FM-CI-01..20 · Pattern Conformance **21 padrões** (12y/3d/6na); seal `2e918a8c` DERIVES_FROM vision-mcp. **(5) Fixes:** morning-briefing tratava `security` (ciso-4-artifact) como BoK 0/9 falso + pin do repo canônico (`3d5a2f4`); `WORKER_RESOURCE_LIMIT` no reframe (guard de megapixels pré-decode, `42ca370`). tsc 0 · vitest **621** verde · gitleaks clean · milestone `9aa1b522` embedado (768d) · malha **9133**. ⚠️ Pendente Sovereign: Pinterest Trial→Standard (vídeo enviado) + Meta redirect URI; revisar legendas pt-BR do EP01 (master do dub); rotação de credenciais (SA Vertex/Gemini/Telegram — banner criado); código do `content-intel` (GO + jurídico); OTD-CI-002 (sondar IG/TikTok resolver); OTD-PSW-001 (GPU, adiado até créditos Vertex acabarem). |
> 19	| **Loop MAPE-K: UX-Explorer + [[landing-bundler|landing-bundler]] + BoKs 9/9 retroativas + swarm:read PAT (2026-07-16)** | ✅ Loop GO'd pelo Sovereign ("pode armar o loop para atacar os próximos passos") + pedido paralelo de auditoria de prontidão BoK 9/9. Drenou it.0→it.4 da diretiva. **(it.0) UX-Explorer enxerga pela 1ª vez da vida** — o auditor nightly nunca tivera run verde (exit 4 maiden + exit 3 ×9 dias); o "auth expirado" era FALSO diagnóstico em cadeia de **4 causas**: PATH do cron sem `agent-browser` (spawn ENOENT), regex do runner casando `/auth` da URL, `wait networkidle` sem `--load` (CLI tratava como seletor → timeout 30s), cron sem `--state` (tour DESLOGADO). Fix + auth state via magiclink (PROC-E2E-006) → cron simulado 6/7 verdes + **1º finding P1 REAL da história** (Vision QA: Controls do ReactFlow brancos sobre o void → `INC-8cba901a` RESOLVIDO `7a00511`: vars `--xy-*` MIV, override de classe perde pro chunk lazy; Vision re-run APROVADO). 2 incidentes fechados, fila zerada. **(it.1) [[landing-bundler|landing-bundler]] core (`762c641`)** — o P0 da landing-factory: SOP Lei 2 ANTES do código → `scripts/landing-bundler/{bundle-core,public-url,cli}.ts` (magic-bytes mandam · CSS recursivo `@font-face` · fail-open por ref/fail-closed estrutural · guard anti-SSRF host re-valida cada 3xx · seam `injectHead` FR-LF-003); **15/15 unit** (G1 SSRF-302 sem emissão interna · G3 CF-challenge · G4 idempotência) + **G5 run real** 331B→150.802B, data:image+data:font REAIS (Google Fonts recursivo), 0 refs externas. **(it.2) witness cadência 7/7 (`885fa77`)** — dispatch real `cadence_dispatches`→`scheduled_posts` queued linkados, re-arm UTC, idempotência, tenant-bind, cleanup 0 resíduo (fecha ressalva do seal `c994c363`; smoke que o SOP nomeava agora existe). **(it.3) BoKs 9/9 retroativas — 32/32 famílias (`a8265eb`+`0718101`)** — método audit-first (`wf_2998d4c7`, 4 agentes, 18 drifts verificados adversarialmente, ground truth em `.claude/context/bok-readiness-audit-2026-07-16.json`) → micro-reparos `a729f83` (mesh mandate youtube-data + gate Gemini-only detector) → 6 writers + 2 critics (`wf_182e0145`; video-repurpose APPROVE 0 violations · youtube-studio 2 violations corrigidas) → verificação mecânica independente. YTS = **guarda-chuva 2 tracks** (GO Sovereign AskUserQuestion): Track A painel SHIPADO + Track B fábrica ROADMAP; estado vivo DATADO (gate Y3 satisfeito, rows=[[61]]). Seals malha `a6df1548`/`9a923887`. **(it.4) swarm:read no PAT allowlist (`1b30fc3`)** — predictive-swarm Fatia 2 sub-fatia; migration `20260716190000` estende o CHECK de vocabulário fechado (fail-closed: scope só entra com tool vivo); `/security-review` NO FINDINGS. **Task idempotência (`76e5a8a`)** — `mcorch_nodes.name` SEM UNIQUE → 24 seed scripts migrados p/ CHECK-BEFORE-INSERT (23/23 re-executados, malha estável). **11 commits** `50bd550..1b30fc3` · tsc 0 · vitest **601** verde · gitleaks clean · milestone `3a23fe00` embedado (768d) · malha **9127**. ⚠️ Pendente Sovereign: aplicar migration `swarm:read` em prod; predictive-swarm Fatia 2-resto (OTD-PSW-001 GPU decision); rotação de credenciais (SA Vertex/Gemini/Telegram); registrar `gcrux.com`+wildcard; 3 chaves Gmail; reconexão X + app-audit IG/TikTok. |
> 20	| **landing-factory BoK 9/9 + fix imagem quebrada + fix egress (2026-07-16)** | ✅ Sessão-maratona interativa (2 vídeos Maestros da IA → operação de marketing agêntica no Spaces; motor de conteúdo de 2 máquinas). **(1) landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte agência-dentro-da-plataforma; deepsearch verify-adversarial (`wf_1f7d1113`→`wf_b8cb767d`) → blueprint v0.2 (superset gate PASS) → **BoK Scribe 9/9** (`wf_d540ceb4`; MR14→BR18→PR18→FR20+NFR10+OTD15+FM14; **Pattern Conformance 15/5/1**; seal `b65e94b1` DERIVES_FROM constellation, embedado). Decisões Owner: Open Design **v0.10.0 pinado** (export single-file NÃO existe upstream — issue #368, `inline-assets.ts` byte-idêntico v0.10→main) → **asset-bundler próprio** (`landing-bundler` host worker) é o P0 da Fatia 1; hosting em **`gcrux.com`** (domínio registrável SEPARADO cookie-isolado, `<slug>.gcrux.com`; NUNCA `*.mcorch.com` — cookie SSO `sb-mcorch-session` `.mcorch.com`-scoped + access token + não-`HttpOnly` [`sso-cookie.ts:13,44`] = account takeover, FM-LF-013 RPN280) + Netlify/Vercel BYOK; WordPress-page-first; PostHog self-host/BYOK (gate humano→autônomo). **Gate Closed-Loop ABERTO** pro código. **(2) fix imagem quebrada** — inspetores Gerar Imagem/Vídeo re-assinam bucket privado (`useDisplayUrl`/`StorageVideo`, superfície faltante do Fix Assets; objeto do nó `n_8rsn4w3l` 400→200 image/png 1,1MB). **(3) fix egress** — signed URL reusável 24h (cache localStorage por uid, clear no logout) vs re-assinar a cada render → corta o cache-buster; `/security-review` NO FINDINGS · 13/13 testes. **(4) roadmap** artefato 2-máquinas salvo como asset do User 0. **6 commits** `9ccfeb7..10444b7` · tsc 0 · suíte **586** verde · gitleaks clean · milestone `56670e5c` · malha **9122**. ⚠️ Pendente: código do `landing-bundler` (Fatia 1); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95%; provisionar 3 chaves Gmail (fila anterior); auditoria de agentes OpenClaw (free-first). |
> 21	| **Loop autônomo: Cadência + Enxame Fatia 1 em PROD + AI Act BoK (2026-07-15)** | ✅ Loop GO'd pelo Sovereign (migration+deploy autorizados) drenou os 4 itens da Fila. **(1) Veo via Vertex PROVADO REAL** — role Vertex AI User concedida → witness pago (gen `2659d78b`, `engine=veo-vertex`, 267 mco exatos 4263→3996, identidade preservada Read+Vision MCP; nó `4e8902d2`) + UI multi-key Vertex (preview do SA JSON, `8772f0d`). **(2) Cadência Fatia 1 SHIPPADA** (`spaces-cadence`, FR-CAD-001..011): motor de recorrência que ESTENDE `autopilot_plans` (plan_kind/recurrence/program/quiet_hours/…) + tabela `cadence_dispatches` (RLS default-deny + índice único parcial de idempotência) + roteia o tick vivo por `plan_kind` (**ZERO pg_cron novo**); `cadence-plan`/`cadence-run` (verify_jwt=false Bearer SB_SECRET_KEY, user_id da linha, drain FOR UPDATE SKIP LOCKED, dispatch→scheduled_posts) + node `kind:cadence`; migration `20260716120000` **aplicada+verificada** · `/security-review` NO FINDINGS · smoke 7/7 · nó `c994c363`. **(3) Enxame Sensorial Fatia 1 SHIPPADA** (`predictive-swarm`, FR-PSW-002/004/005/011/012): Tier 1 gates determinísticos (loudnessGate ffmpeg EBU R128 + contrastGate WCAG/APCA + verdictFor) + tool MCP `vision.parse_sensory_gate` **VIVOS** no container `mcorch_vision_mcp` (ffmpeg 8.0.1 instalado + rebuild, /health anuncia); SSRF por redirect do ffmpeg **FECHADO** (host-pin Supabase + `-protocol_whitelist`, auditor adversarial 7 vetores); tsc 0 · vitest **121/121** · nó `9ecba7fa`. **(4) content-provenance BoK 9/9 selada** (AI Act Art.50, FR-CP-001..013): blueprint deepsearch `531e2b0` + suite `c569416`; **3 camadas** C2PA (c2pa-rs) + watermark (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool), USD=0; integra no spine `creative_assets`; nó `825088c0`. **Órfãos FK** diagnosticados (`user_provider_keys`/`user_api_keys` sem cascade; fix GO-gated). **Crítico adversarial pegou 6 bugs born-dead/SSRF pré-deploy**; contagem de Pattern Conformance das 3 BoKs conferida **MATERIALMENTE** (armadilha fechada). **12 commits** `b15554d..a33bdd7` · 2 `/security-review` NO FINDINGS + 1 auditor SSRF focado · migration aplicada + 3 fns + container deployados (GO Sovereign) · malha **9119** · nó `eed9128f`. ⚠️ Ressalvas: Cadência falta witness E2E de despacho (throwaway/UI); Enxame `swarm:read` fora do PAT allowlist (Fatia 2); rotacionar as chaves expostas. |
> 22	
> 23	| **Veo 3.1 com avatar por referência (Gemini API + Vertex service account) + blueprints cadência/enxame (2026-07-14/15)** | ✅ Sessão-maratona interativa (Sovereign ao vivo fornecendo chaves e diagnosticando billing). **(A) Motor Veo 3.1** (Amendment 25, FR-SPACES-086..091): nó Imagem→Vídeo ganha o único motor com **referências de identidade** (≤3 fotos do mood board → mesmo rosto); ledger-first + `veo-poll` (LRO owner-scoped) + failover de chave por 429. **Witness pago PROVADO E2E** (gen `02994319`, 720×1280 9:16 8s, identidade preservada Vision QA, 178 mco exatos). **(B) Veo via Vertex AI** (Amendment 26, FR-SPACES-092..096): 2º caminho de auth por **service account** (JWT RS256→token, `_shared/google-sa-auth.ts` WebCrypto, sem lib Google) p/ usar os créditos GCP (trial não cobre Gemini API/429, só Vertex — documentado no README do repo GabrielAI). Roteamento por `metadata.auth_type`; custo Vertex **267 mco** (0,15/s); poll `fetchPredictOperation` + vídeo inline base64; UI de colar SA JSON no pool. **Witness Vertex PROVADO REAL E2E em prod** (role Vertex AI User concedida 2026-07-15 → gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s com áudio, **identidade preservada** por Read ocular + Vision MCP independente, débito exato **267 mco** 4263→3996; asset `bb0ec719`, nó `4e8902d2`). Credencial no pool (id `d3c99581`, cifrada). **(C)** 2× SSRF pegos e FECHADOS pelo `/security-review` (redirect A25 + location/project no host A26 via `buildVertexUrl`); anticorpos 9+8 testes. **(D)** Blueprints selados (Fatia 0, BoK-first): nó de **Cadência** ("além do ManyChat", `docs/bok/spaces-cadence/`) + **Enxame Sensorial-Preditivo** (`docs/bok/predictive-swarm/`) — ambos via deepsearch com crítico adversarial (10+4 bloqueios corrigidos). **~14 commits** `11dafd0..541c2c4` · 3× `/security-review` (NO FINDINGS ×2 + 1 HIGH fechado) · smokes 13/13 · **584 testes** · tsc 0 · lint 0 · malha **9111** · nó `91a3f1ec`. ⚠️ SA privada colada no chat → rotacionar após o teste. |
> 24	
> 25	| **YouTube Fatia 2 + débito eslint ZERADO + roadmap não-gated + branding OAuth Google (2026-07-14)** | ✅ Sessão-maratona pós-v6.100.0 (loop autônomo GO'd + Sovereign ao vivo na verificação Google). **(A) Roadmap não-gated drenado:** carrossel IG pelo caminho AGENDADO (Amendment 22, fecha OTD-SPACES-044 — marcador de grupo `carousel_render_id` resolvido owner-scoped, FMEA-011 por construção; smoke 9/9) · reframe server-side no publish (Amendment 23, fecha OTD-SPACES-043 imagem — motor `reframeToJpeg` extraído p/ `supabase/functions/_shared/reframe.ts`, px do seed channel_profiles, fail-open; smoke 8/8 geometria 1080×1350 por decode SOF real) · trilhos de mídia LinkedIn imagem + IG Stories + X media (Amendment 24, FR-SPACES-082..085) + hardening `supabase/functions/_shared/public-url.ts` `assertPublicHttpUrl` (fecha classe SSRF pré-existente nos 5 fetch de mídia caller-controlada) · UI dos trilhos (toggle reframe no AssetDetailDialog + "Agendar carrossel" no VideoRepurposePage). **(B) Débito eslint ZERADO 448→0** (`bun run lint` exit 0; 26 warnings restantes): fan-out 1-agente-por-arquivo (122 arqs) types-only, tipos reais (Tables<>, interfaces por SELECT, catch narrowing, remoção de casts `as any` supérfluos), tsc+test verdes por lote, 6 commits + ignore de vendored/worktrees. **(C) YouTube Studio Fatia 2** (Amendment 12): editar (videos.update) + excluir permanentemente (videos.delete) vídeo via `force-ssl` + receita (revenue_metrics) via `yt-analytics-monetary.readonly` → os **4 escopos ficam demonstráveis** p/ a verificação Google (não aprova uso futuro); `social-auth-init` +escopo monetário; UI card Receita + Editar/Excluir por vídeo gated; smoke 9/9 fail-closed sem tocar canal; `/security-review` NO FINDINGS. **(D) Branding OAuth Google FIXADO** (marca verificada ✅): home era iframe-only (DOM do pai vazio) → verificador sem-JS não via nome/info → home crawlável login-free (HTML estático no `#root` do index.html + header React visível "MCORCH" + descrição + links Entrar/Privacidade/Termos; provado por curl do HTML cru servido). **21 commits** `1c59da5..08f49c5` · 2 `/security-review` NO FINDINGS · smokes 9/9+8/8+9/9 · guard-sweep +2 anticorpos · malha **9108** · nó `5f75a568`. |
> 26	
> 27	| **Assets: seletor de formato + pré-visualização fiel + modal responsivo (2026-07-14)** | ✅ Diretiva Sovereign "UI ruim nos assets, imagens gigantes estragando o modal, no mobile não é app responsivo; faltam opções de publicação + previsualização perfeita por tipo (IG stories/feed/carrossel/reels, YouTube shorts/comunidade)". **BoK-first:** Amendment 21 `21-amendment-publication-format-preview.md` (FR-SPACES-075..078 + OTD-SPACES-043/044 defer + Pattern Conformance inline #13 Human-in-the-Loop) + SOP leve `space-publish-format-preview.md`. **`src/lib/format-specs.ts`** = SSOT client de formato (canal×superfície → aspect/px/safe-zone/caption/publicabilidade; números DERIVADOS do seed `channel_profiles` — Lei 1; paridade 15/15). **`PublicationPreview.tsx`** = 10 chromes fiéis (Reels/Stories/Short **9:16** action-rail+safe-zones · Feed **4:5**/1:1 · Carrossel · Pin **2:3** · link-card · YT vídeo/comunidade · text-post; render 17/17; caveat honesto "prévia aproximada"). **`AssetDetailDialog`** reescrito: picker de formato + preview vivo, publica **imagem E vídeo** via `publish-space-asset` (migra do `publish-social` legado só-vídeo), badges honestos (Publicável/Privado até auditoria/Em breve); modal full-screen app-like no mobile (dvh/gutter/rounded/tap-44) + mídia contida. **Vision QA ocular pegou+corrigiu** um blowout de CSS Grid `min-width:auto` que estourava a imagem no mobile (fix `grid-cols-1`+`min-w-0`). Play affordance nos tiles de vídeo + título no toque; `PublishSocialInspector` do canvas reusa o mesmo preview (formatId + resolveAssetUrl). **4 commits** `56bf601..0f543af` · tsc 0 · eslint 0 · **+32 testes** · 4 deploys ao edge público (serve entry novo) · **E2E wire** (corpo da UI → publish-space-asset → linha `space_publish_variants` draft owner-scoped, limpa) · malha **9107** · nó `66952b93`. **Uncommitted→selado nesta sessão.** |
> 28	
> 29	| **Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** | ✅ sessão-maratona interativa (Sovereign testando ao vivo, GO'ing deploys). **(1) Motor Viral Quality** (video-repurpose, BoK `10-frd-sdd-viral-quality.md` selada c/ Pattern Conformance): detector `detect-viral-moments` (Hormozi sobre o SRT, janelas 15-45s, `text_beats` = cues VERBATIM, LLM só escolhe índices — zero fabricação Lei 1, JSON-mode + parse defensivo) + overlay motion-graphic (`viral-caption-overlay-9x16.html` Montserrat premium sem botão + `renderAlphaFrames` RGBA + FFmpeg overlay sobre footage reenquadrado; anticorpo do `-t` multi-input). UI "Gerar cortes virais" 1-clique (barra ancorada em sinais reais) + botão Distribuir (`publish-space-asset`) + badge SRT. **3 shorts EP01 provados E2E em prod** (abertura 9.0/finale 9.5/conspiração 8.5, Vision 7-8/10). **(2) ASR self-host** whisper.cpp US$0 + reconciliação roteiro-autoritativa (o áudio da IA erra nomes: Austin→Boston Dynamics; roteiro do GitHub GabrielAI via MCP é a verdade). **(3) Rota host-media** streaming Range (206 seek) — master 1,3GB abre na biblioteca; infra host versionada. **(4) Pool multi-key BYOK** (Amendment 20): `user_provider_keys` Vault-cifrada + `resolveProviderKey` (explícita→prioridade→legado→402) + Settings card + seletor Spaces — 3 Gmails × créditos free-tier. **6 commits** `d4972c7..23f6e65` · `/security-review` **NO FINDINGS ×4** · malha **9105** · nó `d98767ea`. **Gated Sovereign:** aplicar migration `user_provider_keys` + deploy `canvas-execute` + cadastrar 3 chaves + aprovar cadência. |
> 30	
> ```

## 🤖 Claude *(03:26:12)*

<details>
<summary>💭 Thinking Process</summary>

Now I'm reviewing the CRM Inbox source files to understand the existing WhatsApp templates edge function and the composer/thread UI, which I'll need to modify for the reaction send feature and the other task. I need to check the sprint priorities and understand the whatsapp-templates function structure to ground my understanding of the action dispatch pattern before presenting the brief.

</details>


## 🤖 Claude *(03:26:12)*

Tenho o quadro. Vou fechar o pré-flight com o sprint goal e uma leitura de fundação para aterrar o item #1 (action `reaction` em `whatsapp-templates`).

## 🤖 Claude *(03:26:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -40 || echo \"NO sprint-priorities.md\"",
  "description": "Sprint goal snapshot"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> ## 📋 FILA SOVEREIGN (ordem declarada — não reordenar sem GO)
> 
> | # | Item | Estado | Gate |
> |---|------|--------|------|
> | 1b | **Veo via Vertex AI (service account)** — Amendment 26, FR-SPACES-092..096 (2026-07-15) | ✅ **PROVADO REAL E2E 2026-07-15** (role concedida → witness pago gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s, identidade preservada Read+Vision MCP, **267 mco** exatos 4263→3996, asset `bb0ec719`, nó `4e8902d2`). code-complete + `/security-review` (1 HIGH SSRF FECHADO) · 584 testes · a chave `AQ.` do Sovereign é Gemini API mas o trial GCP só cobre o Vertex (429 na AI Studio, documentado no README do repo GabrielAI). O pipeline local usa gcloud ADC; servidor usa service account. Auth SA JWT RS256→token (WebCrypto), custo Vertex 267 mco (0,15/s), poll fetchPredictOperation, UI de colar o JSON no pool. | 🔒 **Sovereign:** criar service account no projeto `gabrielai-veo` (role Vertex AI User) → JSON → cadastrar no pool nomeado. Depois: `npx supabase functions deploy canvas-execute veo-poll` + `bun run build` + witness pago com o crédito Vertex real |
> | 1 | **Vídeo com avatar/referências no Spaces (Veo 3.1)** — Amendment 25, FR-SPACES-086..091 | ✅ **PROVADO E2E EM PROD 2026-07-14** — deploy (Sovereign) + build (feito) + smoke **12/12** + **witness pago** (gen `02994319`, 720×1280 9:16 8s, **178 mco exatos** 4441→4263, **identidade facial preservada** Vision QA ocular; failover GabrielAI-429→legada funcionou) · nó malha `ccd5dba5` | ⚠️ **OTD-SPACES-046 aberta**: chave nova "GabrielAI" (a do Vertex) com prepaid AI Studio ZERADO (429); o witness rodou na chave legada via failover. Sovereign decide se recarrega a nova em ai.studio/projects |
> | 2 | **Nó de Cadência no Spaces — "além do ManyChat"** (diretiva 2026-07-14) — cadência + automação conversacional p/ TODOS os usuários, BYOK obrigatório, encaixado nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), sem reconstruir | ✅ **BoK 9/9 SELADA 2026-07-15** (`4602b0f`, nó `d0b4fdc8`) — 10 docs + Pattern Conformance (12y/5d/4na); ESTENDE `autopilot_plans` + roteia o tick por `plan_kind` (zero pg_cron novo), reusa `scheduled_posts`/`sequences`/`nurture-dispatch`; inbound IG PROBE-GATED · **✅ Fatia 1 SHIPPADA 2026-07-15** (`6b5412a`, nó `c994c363`): migration `20260716120000` aplicada+verificada · `cadence-plan`/`cadence-run`/tick roteado deployados · `/security-review` NO FINDINGS · smoke 7/7 · build · crítico pegou 2 bugs born-dead pré-deploy | ⏳ Falta: **witness E2E de despacho** (arm→scheduled_posts, via throwaway/UI p/ não publicar real) + Fatia 2 inbound IG (PROBE-GATED FM-CAD-02) |
> | 3 | **Enxame Sensorial-Preditivo (`predictive-swarm`)** — diretiva 2026-07-14, executar **após** o loop atual. Engine de QA sensorial/psicoacústico: design·cinema·marketing como veículos sensoriais integrados. 3 superfícies MCP: `swarm.initialize_sensory_simulation` (enxames paralelos pontuam deriva de percepção) · `vision.parse_sensory_gate` (Tier 1 varredura periférica CPU-bound / pop-out da Feature Integration Theory → Tier 2 foveal só com sinal de alto valor; expande a "Essência Humana") · `mesh.consolidate_sensory_insight` (traços cognitivos → `mcorch_nodes`/`mcorch_edges`, sem PII bruta, proveniência estrita). Gates duros: telemetria+medição por execução atômica · cobrança SÓ via `deduct_mco_coins` per-tenant (ES256 JWKS contra o `sub`) · hard-fail 402/501 estruturado. Fecha com dashboard 🔄 SYNC UPDATE | ✅ **BoK 9/9 SELADA 2026-07-15** (`dc263fc`, nó `485c0f6e`) — 11 docs + Pattern Conformance (15y/6d/0na); MCP molde vision-mcp (ES256 JWKS), 3 superfícies (initialize/parse-gate Tier1 model-free→Tier2 foveal/consolidate), honesto por construção (score=predição, verdade=`creative_metrics.revenue_cents`) · **✅ Fatia 1 SHIPPADA 2026-07-15** (`65a537b`, nó `9ecba7fa`): Tier 1 gates (loudness ffmpeg + contraste WCAG/APCA + verdict) + tool `vision.parse_sensory_gate` VIVOS no container `mcorch_vision_mcp` (healthy, /health anuncia) · crítico pegou 2 blockers (ffmpeg ausente + SSRF redirect) → fechados + hardened · tsc 0 · vitest 121/121 | ⏳ Falta: `swarm:read` no CHECK do PAT allowlist (migration Fatia 2) p/ PAT externo alcançar; Fatia 2 (fan-out/job store) + Fatia 3 (retrieval) |
> | 4 | **AI Act Art. 50(2)** — marcação machine-readable de conteúdo sintético (imagem Nano Banana · vídeo HyperFrames · voz Qwen3) publicado em redes | ✅ **Escopo decidido (3 camadas) + BoK 9/9 SELADA 2026-07-15** (blueprint `531e2b0` + suite `c569416`, nó `825088c0`): C2PA (c2pa-rs) + watermark invisível (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool) — todas open-source comercial-safe USD=0; integra no spine `creative_assets` (5 colunas aditivas). Pattern Conformance 12/3/6. | ✅ Gate Closed-Loop ABERTO. **Código = fatia futura com GO Sovereign** (prazo AI Act **2026-08-02**, multa Art.99 €15M/3%) |
> | 5 | **landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte "agência dentro da plataforma" (2 vídeos Maestros da IA); build → publish → instrumenta PostHog → reverte-se-piora | ✅ **BoK 9/9 SELADA 2026-07-16** (blueprint deepsearch v0.2 + suite `11a5adb`, seal `b65e94b1`; MR14→BR18→PR18→FR20; Pattern Conformance 15/5/1). Decisões Owner: Open Design **v0.10.0 pinado** (single-file export não existe upstream #368) → **asset-bundler próprio** é o P0; hosting **`gcrux.com`** (domínio separado cookie-isolado, nunca `*.mcorch.com`); WordPress-page-first; PostHog self-host/BYOK. **Gate Closed-Loop ABERTO**. | ⏳ **Fatia 1 = código do `landing-bundler`** (inlina img/fonts/@import → data:); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95% |
> 
> **Sprint v6.107.0 — Meta app-review privacidade + WhatsApp rail E2E + AI Act badge/reframe + CRM seed (2026-07-18)** — sessão-maratona interativa (Sovereign ao vivo no console do Meta). **(1)** `meta-privacy` (deauth + data-deletion signed_request HMAC fail-closed) — as 2 URLs de callback prontas p/ submissão do app-review; `/security-review` NO FINDINGS · smoke 4/4. **(2) WhatsApp Cloud API rail E2E:** fix decisivo `whatsapp-webhook verify_jwt=false` (rail inbound estava morto) + `POST subscribed_apps` + `meta_config` fiado (token **EAA**, não IGAA); número CLOUD_API/LIVE. Templates (create/list/delete, E2E provado) + envio (template/texto livre, plumbing provado até o Meta). **(3)** IG token manual (`connect-instagram-token`). **(4)** AI Act Fatia 2: badge "gerado por IA" (WS-C) + reframe re-mark (WS-D, RPN 294). **(5)** CRM/inbox blueprint-semente deepsearch (`docs/bok/crm-inbox/`, licenças + AI Act, gate FECHADO até BoK 9/9). 11 commits `15810be..2de10cb` (→ `b4f57ba` seal) · tsc 0 · vitest 634 · SEAL ALLOWED (16/16) · malha 9135 · nó `aa4ed885`. **Próximo Sovereign:** aprovação Meta do `promo_semana` → testar envio real; `/bok-scribe crm-inbox` + jurídico; rotação de credenciais expostas no chat (EAA/IG); agente de resposta a comentários (YouTube).
> 
> **Sprint v6.100.0 — Assets: seletor de formato + pré-visualização fiel + modal responsivo (2026-07-14)** — diretiva Sovereign "UI ruim nos assets + previsualização perfeita por tipo". Amendment 21 (FR-SPACES-075..078) + SOP; `format-specs.ts` SSOT (números do seed channel_profiles, paridade 15/15); `PublicationPreview` 10 chromes fiéis (Reels/Stories/Short 9:16 + Feed 4:5/1:1 + Carrossel + Pin 2:3 + link-card + YT vídeo/comunidade + text-post, render 17/17); `AssetDetailDialog` picker + preview publicando imagem+vídeo via publish-space-asset; modal mobile-app-like (Vision QA pegou grid blowout); inspector do canvas reusa o preview. 4 commits `56bf601..0f543af` · tsc 0 · eslint 0 · +32 testes · SEAL ALLOWED (7/7) · malha 9107 · nó `66952b93`. **Próximo:** OTD-SPACES-044 (carrossel IG agendado) · OTD-SPACES-043 (reframe server-side p/ pixel-parity) · trilhos Stories/YT-comunidade (app-audit).
> 
> **Sprint v6.99.0 — Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** — repurpose completo (detector Hormozi + overlay motion-graphic, 3 shorts EP01 provados prod); ASR whisper.cpp US$0 + reconciliação roteiro-autoritativa; rota host-media (206 seek); pool multi-key BYOK (Amendment 20) p/ mineração a ~US$0; estratégia de cadência v1. 6 commits `d4972c7..623fad9` · /security-review NO FINDINGS ×4 · SEAL ALLOWED (8/8) · malha 9105 · nó `d98767ea`. **Pendente Sovereign:** aplicar migration pool + deploy canvas-execute + 3 chaves Gmail + aprovar cadência + GO publicar EP01 no YouTube.
> 
> **Sprint v6.98.0 — YouTube Studio (Fatia 1) + front-door host-local do Repurpose (2026-07-13)** — sessão interativa "colocar a ferramenta pra funcionar" com o Usuário Zero. **(1)** Painel `/dashboard/youtube` (`youtube-data` lê vídeos+métricas Data v3+Analytics v2, token per-user server-side; escopos alinhados aos 3 registrados no Google, analytics adiado até habilitar a YouTube Analytics API; mapa API exaustivo 13rec/175props/52metrics/33ações via workflow multi-agente + Pattern Conformance 21 padrões + SOP). **(2)** Front-door host-local do Repurpose **admin-only** `/dashboard/repurpose`: o master (documentário 1,3GB) vai pro **disco do host** furando o cap de 50MB do Supabase free; `host-upload-server` (loopback 3220, nginx `/api/host-upload`) recebe **upload chunked** de 80MB furando o cap de 100MB do Cloudflare; JWT+admin-gate+streaming; worker lê `bucket=local` realpath-contido **sem copiar 1,3GB**. **yt-dlp do host CONFIRMADO bloqueado** pelo YouTube (bot-check no IP de datacenter). **(3)** fix legenda drawtext (truncagem por bytes-extra UTF-8 → padding). **EP01 real 1,3GB → 5 shorts 9:16 (1080×1920) provados por Vision QA** (reframe centralizado + legenda completa). 6 commits `e174988..1730c4a` · `/security-review` **NO FINDINGS ×3** · Phase 5c **SEAL ALLOWED** (8/8) · malha **9102** · handoff `9f7b191a`. **Pendente (próxima):** cadência TikTok com os 5 cortes (sai **privada até a auditoria de rebranding aprovar**) + manual LinkedIn/IG · reconectar YouTube (test-user) + habilitar YouTube Analytics API p/ métricas · reframe subject-aware (OTD-VR-002) p/ planos letterboxed · BoK youtube-studio 9/9. **Lições:** (a) Vision QA em mídia REAL é o detector honesto — pegou legenda truncada que passou em toda checagem estrutural (5 clips 9:16, durações exatas) mas estava visualmente cortada; (b) caps de plataforma (Supabase 50MB, Cloudflare 100MB) exigem furá-los materialmente (host-disk + chunked), não assumir; (c) o gate de segurança do harness bloqueou editar nginx de produção — respeitei (Lei 4), o Sovereign colou o bloco, eu validei (`nginx -t`) + reload + provei a rota E2E.
> 
> **Sprint v6.97.0 — Motor de repurpose de vídeo: 1 master → N shorts + carrossel IG (2026-07-12)** — diretiva Sovereign "construa a metade que falta reusando a que existe": o MCORCH distribuía mas não produzia cortes. Sessão-maratona interativa (Sovereign aplicou 3 migrations ao vivo + testou cada gate). **BoK-first (Closed-Loop):** blueprint `docs/bok/video-repurpose/` fundamentado em 10 pointers verificados file:line + no mapa do repo `gabrielZarattini/GabrielAI` (o INVERSO — N takes Veo→1 master; fonte do master + schema de metadados + filosofia data-driven). Correções ao snapshot: segmenter=**FR-CP-012** (não OTD-CP-011); OTD-CP-009 fechada (imagem); youtube Pilar I=montagem; carrossel existente=PDF/LinkedIn. **(Fatia 1 VIVA)** `source_module='external'` + `ingest-external-asset` owner-scoped + smoke 5/5. **(Fatia 2 VIVA E2E)** worker `video-repurpose-bridge` + `segment-core` (trim frame-accurate + reframe 16:9→9:16/1:1 center-safe + legenda queimada; guarda OTD-VR-006 no read-time); **3 clipes reais provados por Vision QA** (timestamp confirma o trim). **(Fatia 3 E2E provada)** `carousel-core` (key-frames→slides 4:5) + branch `media_type=CAROUSEL` no publish-social + seam `publish-space-carousel`; **3 slides reais**. **Distribuição reusada:** cortes/slides viram `creative_assets` que o nó "Publicar em Rede Social" (**OTD-SPACES-036** `space_publish_variants`, também landado) consome. **Witness LoRA** bloqueado só em crédito Replicate BYOK (plumbing provado). Rail 100% grátis US$ 0 · `/security-review` **NO FINDINGS ×3** · Phase 5c **SEAL ALLOWED** (8/8) · mesh **9097** · handoff `f050959c` · 6 commits `ac5ca86..831f5cc`. **Pendente (ação Sovereign):** deploy Fatia 3 (`npx supabase functions deploy video-repurpose-run publish-social publish-space-carousel`) · subir master real do EP01 via Fatia 1 → rodar worker → ver cortes+carrossel do documentário real · auditoria de app IG/TikTok destrava o publish real. **Próximas fatias:** 4=mapeador metadado→legenda nativa+HTML WP · 5=fiar na distribuição E2E. **Lições:** (a) verificar cada pointer materialmente pegou que o repo andou (FR-CP-012, OTD-CP-009 fechada) e que o GabrielAI é o INVERSO — não molde do segmenter; (b) Vision QA em mídia REAL de produção é o único detector honesto (pegou truncamento de legenda longa → OTD-VR-007); (c) reusar os trilhos (o sink que eu tinha acabado de criar) fechou o loop ingest→corte→publicação sem reconstruir nada.
> **Sprint v6.96.0 — Voz clonada self-host COMPLETA + Modo Expressivo + motion design do canvas (2026-07-09/10)** — sessão-maratona interativa (Sovereign testando ao vivo; 13 commits `578f02e..eb422fd`). **(1) Rail de voz US$ 0 VIVO** no nó Clone de Voz (OTD-VOICE-001 fechada por veredito auditivo): Qwen3-TTS 0.6B+1.7B no host · fila `video_renders` engine `qwen3-voice` · worker `voice-bridge.service` com heartbeat anti-reaper (bug witnessed: reaper de 45min re-claimava job vivo) · multi-amostra FR-SPACES-059 (principal + 5 clipes ≤7s, ffprobe fail-closed) · perfil ICL `.qvoice` + `-ref.wav` (x-vector reprovado pelo ouvido; grafts são model-bound) · smoke **12/12**. **(2) Modo Expressivo**: 1.7B + assets `.expr`, witness RTF 13,9 "composed 3 spans", normalizador da sintaxe do Sovereign (`{happy}`/`<#0.5#>`/`(gasps)` → gramática real; tag desconhecida NUNCA falada), roteiro 20k, "Gerar roteiro com IA" (select pela regra perene). **(3) Reparos**: reunion migration `20260710170000` (drift de 07/jul derrubara `avatar-studio` do guard — áudio fora do spine EM SILÊNCIO; anticorpo: SEMPRE checar `error` de `supabase.rpc`, ele não lança) + aba Áudios na Biblioteca + Histórico `generate_voice` + backfills. **(4) Motion design Amendment 19**: motion=telemetria (processing/transmitting/established), FlowEdge com partículas, 1 seam p/ 12 node types, frame-diff provou. **(5) Regra perene BYOK** (`useConfiguredProviders` da view mascarada; memória `feedback_byok_only_available_options`) + ElevenLabs IVC multi-amostra + **F5-TTS/Fish Speech REJEITADOS** (pesos non-commercial). 2× `/security-review` NO FINDINGS · Phase 5c **SEAL ALLOWED** (15/15) · mesh **9094** · handoff `8c1f0e7b`. **Lições:** (a) o aside do /security-review pegou enum CHECK errado no INSERT do histórico — reviewer independente paga sempre; (b) o WAF do Management API devolve HTML-challenge (não JSON-error) em DDL grande com `DO $$` — gate de apply DEVE validar o corpo + prova material; (c) fail-soft sem log = falso-sucesso de um dia inteiro.
> **Sprint v6.83.1 — Fix Assets: exibição de mídia privada owner-scoped em TODO o ecossistema (2026-07-03)** — diretiva direta do Sovereign ("a maioria das mídias sumiu; garanta E2E que aparecem em todos os lugares"). **Diagnóstico refutou a hipótese de lixo de smoke (Lei 1):** os 90 assets são TODOS do User 0 (`ada39fae`, saldo 4571). Causa real: buckets viraram privados+owner-scoped (correto — fechou enumeração cross-tenant), mas o app resolvia URL **pública** (400 em bucket privado) e o cliente não assinava objeto com prefixo ≠ uid (`owner=NULL` service-role). Escopo: 84 creative_assets + 68 vm_canvas_executions + 32 graphs + 1 space. **Fix:** migration `20260703030000` (3 policies owner-scoped 4-rotas `=auth.uid()` + triggers de id server-side INSERT+UPDATE anti-claim/PK-swap + data-repair is_public) + fix bug vivo `canvas-execute:555` + lib `asset-url.ts` (`toDisplayUrl`/`useDisplayUrl` re-assina no render, cura pública-morta E assinada-expirada) + `<StorageImg/Video/Audio>` em **13 superfícies** + `resolveAssetUrl` chaveia pelo bucket real. **Segurança:** `/security-review` independente **CLOSED 9/10** — achou e me fez fechar 1 HIGH cross-tenant que a 1ª versão introduziu (claim via `vm_canvas_projects` id-squat + PK-swap). Cross-tenant **BLOCKED ao vivo** (throwaway: sign/claim/PK-swap). **Prova:** signing antes FAIL→SIGNED 200 · tsc 0 · build+deploy · deploy canvas-execute · **E2E local determinístico: Biblioteca 67/71 imgs+19 vídeos, Canvas 17/17+4 vídeos, 0 dead-public, Vision-QA APROVADO ×2 + confirmação ocular (90 assets)** · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9047** · handoff `6e2b32b2` · commits `6e5e005`/`459cd25`. **Lição:** o classificador do harness bloqueou o apply de DDL sob /loop genérico → respeitei o gate (Lei 4), o Sovereign rodou `!`, e o `/security-review` ANTES do apply-final pegou meu próprio HIGH — o gate de RLS provou seu valor de novo (FMEA-011). SOP `private-bucket-asset-signing.md`.
> 
> **Sprint v6.83.0 — Spaces 2d compose VIVO E2E: drift do Higgsfield resolvido (OTD-SPACES-003) (2026-07-03)** — loop autônomo fechou a única pendência real da Fase 2d. **Nunca chutei semântica de provider (Lei 1):** sonda 422 zero-custo (type-poisoning revela schema Pydantic sem enfileirar job pago) provou que `soul/compose` **nunca existiu** — path é `soul/{mode}` (mode literal `reference|character|standard`), refs exigem `custom_reference_id` cunhado async (`/v1/custom-references`, fila de minutos, incompatível com janela sync). **Fix:** compose migrado p/ **OpenRouter Nano Banana multimodal** (motor da 2b já provado), custo re-pinado 18→10 (o 18 precificava ficção), BYOK openrouter fail-closed (gate C4), `generateHiggsfield` throw honesto p/ compose (OTD-SPACES-005). **Achado colateral P1:** `canvas-assets` privado desde a criação → `getPublicUrl` = URLs 400 mortas em 4 call-sites → tudo assina (server 7d, refs client 365d). **Anticorpo:** `smoke-higgsfield-schema.ts` 7/7 pina o contrato vivo (drift = exit 1). **Prova:** smoke Spaces **31/31** (C3 refund+pinned 10 · C4 402 pré-débito) · vitest **398** · tsc 0 · deno check · **E2E pago** (space `4909d024`, generation `cc789ada` done, PNG 919KB URL assinada HTTP 200, saldo 4581→4571 exato, Vision QA high) · review 3-lentes inline (Opus, após créditos Fable esgotarem) · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9045** · handoff `8733cab`. **Direção Sovereign registrada — OTD-SPACES-007:** conector per-user do **MCP oficial Higgsfield** (`mcp.higgsfield.ai`; Bearer BYOK=catálogo, conta=OAuth com DCR+refresh provados) → 30+ modelos auto-descritivos atrás de 1 integração; BoK-gated antes do código. **Pending:** OTD-SPACES-004/006/007 · Workflow Apps/FX/multi-page (Fase 2) · voz clonada (biometria) · app-registration YT/TikTok · Universe cutover. **Lição:** a sonda de schema por payload-inválido é a técnica canônica p/ fechar drift de provider externo sem gastar — e vira sentinel permanente, não one-off.
> 
> **Sprint v6.82.1 — Sprint Spaces 1b→2d SELADO: canvas pago com 4 modalidades (2026-07-02)** — 6 iterações autônomas do loop pós-GO Sovereign. **(1b LIVE)** GO executado: migration `20260702190000` aplicada+registrada+provada (DDL 8/8) · **drift do ledger de migrations FECHADO** (10 registradas por sonda DDL, audit exit 0) · fix ordem de guards · smoke 13/13 · E2E pago magic_prompt (saldo −1 exato, Vision QA high). **(2a vídeo)** ledger-first no submit + webhook hash-safe (SHA-256-only, migration `20260702210000`) + supressão do deduct legado; review **NO P0/HIGH** (MEDIUM+2 LOW corrigidos); **canvas→vídeo REAL** MP4 11.3MB via webhook Higgsfield, saldo −40 exato, Vision QA no vídeo (space-demo `51b229cf` vivo). **(2b)** References picker upload real, cap honesto 4 = verdade do server. **(2c voz)** 8 vozes stock via `tts-speak` com JWT do usuário; review **APPROVED** + F1 pinado (gate A4); WAV 9s real, saldo −2 exato (space-demo `1d77b500` vivo). **(2d composer)** código-completo + **ACHADO**: Higgsfield dropou `mode=compose` → compose legado do Canvas Studio quebrado por API drift; estorno integral provado; **OTD-SPACES-003**. **Prova:** smoke **30/30** · vitest **398** · tsc 0 · SOPs S14-S32 ANTES do código · Phase 5c **SEAL ALLOWED** · mesh **9043** · handoff `f85d3cf4`. **Pending:** OTD-SPACES-001/002/003 · Workflow Apps/FX/multi-page (Fase 2) · voz clonada (biometria, Fila) · app-registration YT/TikTok (Fila). **Lição:** parar no erro material do provider (compose 422) em vez de chutar semântica = Lei 1 aplicada a APIs externas; e o pin de custo contra payload forjado (F1/A4/C3) virou padrão obrigatório de todo custo declarado.
> 
> **Sprint v6.76.0 — Spaces Fase 1b: execução runGraph + ledger generations CÓDIGO-COMPLETO, apply em prod GATED (2026-07-02)** — loop re-armado, ciclo fechado completo até o portão de produção: mapeamento ultracode `wf_b4abf175-410` (24 contradições BoK↔código resolvidas) → SOP Lei 2 `spaces-graph-execution.md` (S1-S13) → migration `20260702190000` (ledger `generations` + RPCs atômicas `begin/finalize_space_generation` service-role-only, **NÃO aplicada**) → branch ledger-first exclusivo no `canvas-execute` (422 pré-débito · cap IN-list · `refund_pending` honesto · done-fallback) → client `useGenerationLedger`/clusters/Estimar+Rodar → **/security-review independente SOUND** (4 achados corrigidos, incl. `self-heal-spaces.sh`). **Prova:** vitest **17/17** (+ mirror-parity mecânico) · deno check · eslint 0 · tsc 0 · Phase 5c **SEAL ALLOWED** (11/11) · mesh **9034** · handoff `209cbcd8`. **🔒 Pendente GO Sovereign:** apply da migration (classificador negou 4× sob modo auto — `! bash scripts/qa/apply-spaces-1b-migration.sh` destrava) → deploy fn → smoke 8 gates → E2E+Vision QA. **Achado:** 6 migrations `202607*` aplicadas-mas-não-registradas no ledger remoto (db push INSEGURO). **Lição:** o portão de permissão do harness é um Owner-gate real — 4 recusas respeitadas sem contorno é o protocolo de Lei 4 funcionando.
> 
> **Sprint v6.75.0 — loop it.2-3 (selo final): reward_weights config-as-data + Spaces Fase 1a canvas vivo (2026-07-02)** — **(it.2)** NFR-VA-010: pesos do reward do Viral Autopilot viram DADO por plano (`autopilot_plans.reward_weights` jsonb; `resolveRewardConfig` valida+normaliza, inválido→fail-safe; auditoria `weights_source`). /security-review NO FINDINGS · smoke **16/16** (`6058e78`). **(it.3)** Spaces Fase 1a: **canvas infinito 72/28 VIVO** em `/dashboard/spaces` (home + `:id`), Spotlight 26 tipos, conexão tipada, persistência `spaces.graph` jsonb RLS-own — zero execução/ledger (Fase 1b depois). /security-review NO FINDINGS · vitest 5/5 · **E2E browser User 0 (DB graph=2 nós) + Vision-QA APROVADO** (`9ea6ac0`). **Prova:** tsc 0 · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9033** · handoff `13fd6fe0`. **Loop PARADO** (janela alta + Fatia 1b grande à frente). **Pending:** Spaces Fase 1b (`runGraph`→`canvas-execute`+ledger+clusters — fecha canvas→conteúdo pago) · Universe cutover (Sovereign) · V4-2 (experiment-gated). **Lição:** selar antes de uma Fatia grande protege trabalho durável sem desperdício (Lei 3 calibrada).
> 
> **Sprint v6.74.0 — spaces-evolution BoK 9/9 + loop re-armado it.1: B5 Pauta de Receita (2026-07-02)** — **(1)** A pedido direto do Sovereign, a única suíte BoK incompleta foi fechada ANTES de continuar o roadmap: 06/07/08 grounded no scaffold Phase 0 promovido + **Pattern Conformance §11** (4 yes · 8 deferred nomeados · 9 n-a) + renames canônicos → **25/25 suítes verdes**, seal `8f5fd3fd` DERIVES_FROM viralmind, **BoK Gate do Spaces Fase 1 ABERTO** (`4a8fee0`). Verificação mecânica corrigiu 2 imprecisões pré-commit (Lei 1). **(2)** Loop autônomo re-armado (prompt canônico) — it.1 = **B5 Pauta de Receita FR-VA-031 (HITL)**: SOP Lei 2 → ranking puro vitest 7/7 → seção na AutopilotPage → browser-verify User 0 (linha #1 ↔ `content_library e27a09e7`) → **Vision-QA APROVADO high** (`367db9b`). **Prova:** tsc 0 · Phase 5c **SEAL ALLOWED** (8/8) · mesh **9032** · handoff `10d8c70b`. ⚠️ Workflows quota-blocked até 4:20am → execução inline. **Pending:** `reward_weights` config-as-data (NFR-VA-010) · Spaces Fase 1 MVP · V4-2 · witness G7 imagem multi-canal no próximo ciclo pago.
> 
> **Sprint v6.73.4 — Loop it.4 (selo final): B4 EWMA multi-ciclo no analyze (2026-07-02)** — reward sobre janela M=5 ciclos peso 0.5^idade (anti-thrash; janela lembra, plano virgem não inventa; auditoria `reward_vector.ewma`). Smoke **13/13** (L7: evidência acumulada 7 vence recente 3 — single-cycle flipava) · deployado · SOP amendada · Phase 5c SEAL ALLOWED · mesh **9023** · handoff `1ddd4e86`. **Loop PARADO (janela ~95%).** Restam desbloqueados: B5 pauta de receita (FR-VA-031) · V4-2 · `reward_weights` config-as-data.
> ```

## 🤖 Claude *(03:26:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"action ===|case '|body\\.action|const action|switch\" supabase/functions/whatsapp-templates/index.ts | head -40; echo \"--- lines ---\"; wc -l supabase/functions/whatsapp-templates/index.ts supabase/functions/whatsapp-webhook/index.ts",
  "description": "Inspect action dispatch in whatsapp-templates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 89:  const action = body.action ?? "list";
> 98:    if (action === "list") {
> 105:    if (action === "create") {
> 131:    if (action === "delete") {
> 141:    if (action === "mark_read") {
> 184:    if (action === "send") {
> --- lines ---
>   463 supabase/functions/whatsapp-templates/index.ts
>   390 supabase/functions/whatsapp-webhook/index.ts
>   853 total
> ```

## 🤖 Claude *(03:26:27)*

<details>
<summary>💭 Thinking Process</summary>

I've got everything I need to generate the /handson brief—the sealed CRM Inbox Amendment with its commit hash and milestone, a clean worktree and Docker environment, and the sprint goal from priorities. The knowledge base is complete and verified at 9/9 completeness.

Now I'm mapping out the next items: FR-CRM-028, FR-CRM-033, and FR-CRM-031, with Settings MIV print-gated. I can see the WhatsApp templates action dispatch structure already has list, create, delete, mark_read, and send—FR-CRM-028 will add a reaction action to that. Since item #3 is print-gated and the Sovereign already approved the 1+2+3 sequence, I'll present the brief and flag that I'm ready to start with FR-CRM-028. For the knowledge mesh, I have the 9190 nodes from the handoff state and can reference the edge count from the GraphRAG source. I'll write this up concisely in Portuguese.

</details>


## 🤖 Claude *(03:26:51)*

═══════════════════════════════════════════════════════════
  HANDSON — CRM Inbox Amendment 10 (seal 2026-07-19)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **CRM Inbox Amendment 10** — composer completo + swap/recibos ao vivo + ficha rica do lead (malha 9190)
  Últimos commits:
    `20daaee` — docs(handoff): seal CRM Inbox Amendment 10
    `0629280` — docs(readme): v6.109.0
    `37863f0` — feat(crm-inbox): render de localização e contatos inbound (FR-CRM-027)
    `db1763e` — feat(crm-inbox): envio de mídia no composer (FR-CRM-025)
    `b31c062` — style(settings): título com a serifa de marca (font-heading)

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (nada em `git status`, `scratch/` limpo)

🏗️ **INFRA**
  `mcorch_chroma`:     Up 4 weeks — Chroma API v2: **OK** (`heartbeat` respondeu)
  `mcorch_claude_mem`: Up 4 weeks (healthy)
  `mcorch_vision_mcp`: Up 3 days (healthy)
  `mega-brain-{daemon,webhook,dashboard}`: Up 4 weeks (daemon+webhook healthy)

🧠 **KNOWLEDGE MESH**
  **9190 nós** (fonte: Task State header) · milestone do seal `9ad13522`
  BoK `crm-inbox` selada 9/9 → seal `2dff4a5a` (DERIVES_FROM marketing-hub)

🔧 **TYPESCRIPT**
  Zero erros ✅ (`tsc --noEmit` limpo — lembrete: o `tsc` da raiz é no-op p/ código da app; gate real é `bun run build`)

📚 **BoK SUITES** (relevante à sessão)
  `crm-inbox` — 9/9 selada + `10-amendment-rich-media-omnichannel.md` + SOP `crm-inbox-window-state.md`
  Gate BoK: ✅ ABERTO — todo o trabalho "1+2+3" é **ação nova em fn existente** (NFR-CRM-005), não módulo novo → sem novo `/bok-scribe`.

📌 **SPRINT**
  Goal: Distribuição social autônoma + (loop ativo) **CRM/Inbox Omnichannel nativo**
  Loop CRM GO'd pelo Sovereign ("1+2+3")

⚡ **PRÓXIMOS PASSOS** (a fila "1+2+3")
  1. **FR-CRM-028 — envio de reação** a um balão: nova action `reaction` em `whatsapp-templates` (`{message_id, emoji}`, grátis/window-agnostic) + UI hover no balão inbound. Reações **inbound já renderizam**. Dispatch atual da fn: `list/create/delete/mark_read/send` → `reaction` é o 6º irmão.
  2. **FR-CRM-033 — registry omnichannel** + UI "Conectar nova caixa" (deriva de `social_accounts`/`meta_config`; WhatsApp vivo, demais gated) · **FR-CRM-031** espelho WhatsApp toggle lazy.
  3. **Settings — passe MIV profundo**: ⏳ **gated no print/referência** que o Sovereign vai enviar. Hoje só o título foi ajustado (cards já usam tokens). *Não redesenhar no escuro.*

⚠️ **ALERTAS**
  - **Witness E2E dos envios é cérebro-sem-mãos** (Lei 1): HMAC/token no vault + CF barra o browser de datacenter. Plumbing se prova por eszip (`strings|grep`) + bundle env-baked; o teste live real é do Sovereign.
  - **Cap de 100 edge fns**: `deploy fn1 fn2` bulk = 402 → sempre `deploy <fn>` single (isento). eszip é binário → verificar com `strings|grep`, o "No change found" do CLI **mente**.
  - **Pendente Sovereign (não-código)**: rotacionar credenciais expostas (`META_APP_SECRET`/EAA/IG) — lembrete critical já semeado no banner do `/dashboard/admin`.
  - **Fatia 3 (agente de reply)** segue GATED no jurídico AI Act Art.50 (prazo 2026-08-02).

═══════════════════════════════════════════════════════════
  Pronto para trabalhar.
═══════════════════════════════════════════════════════════

Contexto absorvido. O item **#3 (Settings MIV)** está travado no seu print — não vou redesenhar no escuro. Os itens **#1** e **#2** estão desbloqueados e você já deu o GO "1+2+3" na sessão anterior.

**ORO triplet do loop:**
- Operator: MCORCH Master Execution Agent
- Reviewer: `/security-review` (toda migration nova) + Sovereign (witness E2E dos envios ao vivo)
- Owner: Sovereign (blast radius: número WhatsApp LIVE +39, PII/LGPD, custo per-message)

Quer que eu **arranque no #1 (FR-CRM-028 — reação-send)** agora, ou prefere enviar o print de Settings primeiro para eu paralelizar #1 + #3? Minha recomendação: **começar pelo #1** (self-contained, action nova + UI hover, zero migration) enquanto o print não chega.

## 👤 User *(03:28:44)*

Veja que no primeiro print do inbox temos o problema agora de compartilhar contato veja se é possivel melhorar isso. E agora você pode ver o setting na segunda imagem e na terceira como poderia ser

## 🤖 Claude *(03:29:36)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the three images the user shared, I'm examining how the CRM inbox is rendering different content types. The first screenshot shows a conversation with a sticker image, emoji reactions that appear as boxes or ghost characters, and a contact card that's displaying poorly with just a placeholder icon and dash instead of actual contact information.

The user is pointing out that the contact card rendering needs improvement. The second screenshot shows the current state of the settings dashboard — it's very basic with plain stacked text inputs, labels, and masked fields for API keys with test buttons, no visual polish or hierarchy. The third screenshot is a mockup of how it could look: a redesigned settings page with provider icons for each API service, organized in rows with icons, names, descriptions, masked inputs with eye toggles, grouped into cards with better visual structure, a quick tips sidebar, and a polished header with a 3D shield graphic.

So there are two main pieces of work here: fixing the contact card rendering in the inbox, and redesigning the settings page to match the target mockup with proper visual hierarchy and provider branding. So the Settings redesign is now unblocked with the mockup provided, and there's a new priority: fixing the contact-card rendering that currently shows just a dash. I should use the Workflow tool for thorough verification given the production constraints, but first I need to examine the existing code to understand what's broken and what needs redesigning. I'm hitting a tension here — the Sovereign's directive to work hands-on in the foreground and avoid multi-agent workflows directly contradicts the system reminder about using Workflow tools for substantive tasks. I need to figure out which takes precedence before I proceed. I can still be thorough through careful direct work and review gates without needing background fan-out workflows. The Sovereign's explicit instruction to work foreground takes precedence, so I'll honor that constraint while maintaining rigor through synchronous verification and review tools.

Now let me think through the UI work and how the MCORCH laws apply here. I need to verify both changes work correctly in a real browser environment. Since the datacenter browser is blocked by Cloudflare for the live site, I'll use a local vite preview with an agent-browser to test the Settings refactor, and run Vision QA on rendered screenshots for both the contact-card fix and the UI pass. Now I'm diving into the actual code to understand what needs testing — starting with the ThreadView component and Settings page. Let me start exploring the codebase to find those files.

</details>


## 🤖 Claude *(03:29:44)*

Recebido — dois itens concretos e o print de Settings destravou o #3. Deixa eu reconciliar a diretiva primeiro, depois mão na massa.

**Nota de reconciliação (ultracode × sua diretiva):** o lembrete de sessão diz "ultracode ON → use Workflow em tudo, em fundo". Mas você foi explícito no `/handson`: **"mão na massa, foreground — evitar workflows de fundo com fan-out de vários agentes"**. Sua diretiva direta e recente vence o *como* (executo foreground, sem fan-out de fundo); o ultracode fica valendo pro *padrão de qualidade* (exaustivo + verificação adversarial via `/security-review`, `/code-review`, Vision QA). Se quiser que eu solte um workflow em algum ponto, é só dizer.

Dois alvos desta sessão:
- **A) Card de contato inbound quebrado** (print 1): o balão `👤 Contato / — / 00:21` renderiza vazio — o vCard não está sendo parseado. Melhorar.
- **B) Settings — passe MIV profundo** (print 2 → print 3): sair do texto plano monoespaçado para os cards com ícone de provider + descrição + olho + Testar, agrupamento (card roxo Avatar/Clone AI), sidebar "Dica rápida", header com escudo.

Vou ler o código real dos dois antes de tocar em nada. Nada no escuro.

## 🤖 Claude *(03:29:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== inbox components ===\"; ls -la src/components/inbox/ 2>/dev/null; echo \"=== settings components ===\"; ls -la src/components/settings/ 2>/dev/null; echo \"=== SettingsPage ===\"; ls -la src/pages/SettingsPage.tsx 2>/dev/null; wc -l src/pages/SettingsPage.tsx 2>/dev/null",
  "description": "Locate inbox + settings source files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === inbox components ===
> total 76
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jul 19 00:08 .
> drwxrwxr-x 28 gcrUX  gcrUX   4096 Jul 18 16:55 ..
> -rw-rw-r--  1 ubuntu ubuntu 17110 Jul 18 23:14 ContactPanel.tsx
> -rw-rw-r--  1 ubuntu ubuntu  4345 Jul 18 22:30 ConversationList.tsx
> -rw-rw-r--  1 ubuntu ubuntu 20617 Jul 19 00:03 MessageComposer.tsx
> -rw-rw-r--  1 ubuntu ubuntu 15625 Jul 19 00:08 ThreadView.tsx
> === settings components ===
> total 88
> drwxrwxr-x  2 gcrUX  gcrUX   4096 Jul 18 14:58 .
> drwxrwxr-x 28 gcrUX  gcrUX   4096 Jul 18 16:55 ..
> -rw-rw-r--  1 ubuntu ubuntu  5660 Jul  8 22:04 HiggsfieldConnectorCard.tsx
> -rw-rw-r--  1 gcrUX  gcrUX  14867 Jun 16 23:57 McpConnectorsCard.tsx
> -rw-rw-r--  1 ubuntu ubuntu 12609 Jul 17 20:03 MetaConfigCard.tsx
> -rw-rw-r--  1 ubuntu ubuntu 10460 Jul 15 15:01 ProviderKeysCard.tsx
> -rw-rw-r--  1 gcrUX  gcrUX   6964 Jun 27 13:09 SocialAppConfigCard.tsx
> -rw-rw-r--  1 ubuntu ubuntu  6271 Jul 18 14:58 WhatsappSendCard.tsx
> -rw-rw-r--  1 ubuntu ubuntu  8267 Jul 18 14:39 WhatsappTemplatesCard.tsx
> === SettingsPage ===
> -rw-rw-r-- 1 ubuntu ubuntu 33106 Jul 18 23:54 src/pages/SettingsPage.tsx
> 672 src/pages/SettingsPage.tsx
> ```

## 🤖 Claude *(03:29:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== contacts/location handling in ThreadView ===\"; grep -n \"contact\\|Contato\\|location\\|vcard\\|vCard\\|Localiza\u00e7\u00e3o\\|Localizacao\" src/components/inbox/ThreadView.tsx 2>/dev/null | head -40; echo \"=== webhook contacts/location parse ===\"; grep -n \"contacts\\|location\\|vcard\\|content_type\\|payload\\|raw\" supabase/functions/whatsapp-webhook/index.ts | head -40",
  "description": "Find contact/location render + webhook storage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === contacts/location handling in ThreadView ===
> 102: * a location (→ map link) or shared contact vCards. Best-effort — never throws on a malformed shape.
> 108:  if (msg.content_type === "location") {
> 128:  if (msg.content_type === "contacts") {
> 129:    const contacts = (Array.isArray(payload) ? payload : [payload]) as {
> 135:        {contacts.map((c, i) => {
> 136:          const nm = c?.name?.formatted_name ?? "Contato";
> 203:      case "location": return <MapPin className="w-3.5 h-3.5" />;
> 204:      case "contacts": return <User className="w-3.5 h-3.5" />;
> 211:    sticker: "Figurinha", reaction: "Reação", location: "Localização", contacts: "Contato",
> 220:      {/* Header — contact avatar + name + window state (WhatsApp top bar, MIV) */}
> 311:                      {(msg.content_type === "location" || msg.content_type === "contacts") && <StructuredPayload msg={msg} />}
> === webhook contacts/location parse ===
> 1:// deploy: crm-inbox Fatia 1 content_type mapping fix (unmapped WA types no longer dropped) 2026-07-18
> 34:    "raw",
> 108:      const rawBody = await req.text();
> 113:      const isValid = await verifySignature(rawBody, signature, appSecret);
> 120:      const payload = JSON.parse(rawBody);
> 123:      const entry = payload.entry?.[0];
> 192:      // Process contacts & messages
> 193:      const contact = value.contacts?.[0];
> 204:        // reaction/location/contacts (persisted structurally), anything else clamps to 'text'.
> 206:        const CONTENT_TYPE_DOMAIN = new Set(["text", "image", "audio", "video", "document", "sticker", "reaction", "location", "contacts"]);
> 209:          sticker: "Figurinha", location: "Localização", contacts: "Contato", reaction: "Reação",
> 295:          // content_type now carries the REAL type (the CHECK domain was extended by migration
> 302:            content_type: contentType,
> 331:          // Location/contacts: structural payloads kept in metadata (no media bytes to pull).
> 332:          if ((waType === "location" || waType === "contacts") && message[waType]) {
> 333:            (messageRecord.metadata as Record<string, unknown>).wa_payload = message[waType];
> ```

## 🤖 Claude *(03:29:53)*

<details>
<summary>💭 Thinking Process</summary>

I need to examine the ThreadView.tsx file more closely, specifically looking at how contacts and locations are rendered and how the webhook storage handles the data structure.

</details>


## 🤖 Claude *(03:29:53)*

Vou ler o render estruturado no `ThreadView.tsx` e como o webhook guarda o payload de contacts, pra entender por que o card sai vazio.

## 🤖 Claude *(03:29:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/inbox/ThreadView.tsx",
  "offset": 95,
  "limit": 120
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 95	      Baixar documento
> 96	    </a>
> 97	  );
> 98	}
> 99	
> 100	/**
> 101	 * Renders inbound structured payloads the webhook persisted in metadata.wa_payload (FR-CRM-027):
> 102	 * a location (→ map link) or shared contact vCards. Best-effort — never throws on a malformed shape.
> 103	 */
> 104	function StructuredPayload({ msg }: { msg: MessageRow }) {
> 105	  const payload = (msg.metadata as Record<string, unknown> | null)?.wa_payload;
> 106	  if (!payload) return null;
> 107	
> 108	  if (msg.content_type === "location") {
> 109	    const loc = payload as { latitude?: number; longitude?: number; name?: string; address?: string };
> 110	    if (loc.latitude == null || loc.longitude == null) return null;
> 111	    return (
> 112	      <a
> 113	        href={`https://www.google.com/maps?q=${loc.latitude},${loc.longitude}`}
> 114	        target="_blank"
> 115	        rel="noreferrer"
> 116	        className="flex items-start gap-2 my-1 p-2 rounded-lg bg-background/60 border border-border hover:border-primary/40 transition-colors"
> 117	      >
> 118	        <MapPin className="w-4 h-4 mt-0.5 text-primary flex-shrink-0" />
> 119	        <div className="min-w-0">
> 120	          {loc.name && <p className="text-sm text-foreground truncate">{loc.name}</p>}
> 121	          <p className="text-xs text-muted-foreground break-words">{loc.address ?? `${loc.latitude}, ${loc.longitude}`}</p>
> 122	          <p className="text-[11px] text-primary mt-0.5">Ver no mapa</p>
> 123	        </div>
> 124	      </a>
> 125	    );
> 126	  }
> 127	
> 128	  if (msg.content_type === "contacts") {
> 129	    const contacts = (Array.isArray(payload) ? payload : [payload]) as {
> 130	      name?: { formatted_name?: string };
> 131	      phones?: { phone?: string }[];
> 132	    }[];
> 133	    return (
> 134	      <div className="my-1 space-y-1">
> 135	        {contacts.map((c, i) => {
> 136	          const nm = c?.name?.formatted_name ?? "Contato";
> 137	          const phone = c?.phones?.[0]?.phone ?? "";
> 138	          return (
> 139	            <div key={i} className="flex items-center gap-2 p-2 rounded-lg bg-background/60 border border-border">
> 140	              <User className="w-4 h-4 text-primary flex-shrink-0" />
> 141	              <div className="min-w-0">
> 142	                <p className="text-sm text-foreground truncate">{nm}</p>
> 143	                {phone && <p className="text-xs text-muted-foreground font-mono">{phone}</p>}
> 144	              </div>
> 145	            </div>
> 146	          );
> 147	        })}
> 148	      </div>
> 149	    );
> 150	  }
> 151	
> 152	  return null;
> 153	}
> 154	
> 155	/** WhatsApp-style delivery receipt (outbound only): ✓ sent · ✓✓ delivered · ✓✓ cyan read. */
> 156	function Receipt({ status }: { status: string | null | undefined }) {
> 157	  if (status === "read") return <CheckCheck className="w-3.5 h-3.5 text-primary" aria-label="Lido" />;
> 158	  if (status === "delivered") return <CheckCheck className="w-3.5 h-3.5 text-muted-foreground" aria-label="Entregue" />;
> 159	  if (status === "failed") return <AlertTriangle className="w-3 h-3 text-[var(--gold)]" aria-label="Falhou" />;
> 160	  return <Check className="w-3.5 h-3.5 text-muted-foreground" aria-label="Enviado" />;
> 161	}
> 162	
> 163	interface ThreadViewProps {
> 164	  messages: MessageRow[];
> 165	  conversation: {
> 166	    id: string;
> 167	    lead_name: string | null;
> 168	    window_expires_at: string | null;
> 169	    last_inbound_at: string | null;
> 170	  } | null;
> 171	  onOpenContact?: () => void;
> 172	}
> 173	
> 174	export function ThreadView({ messages, conversation, onOpenContact }: ThreadViewProps) {
> 175	  const formatTime = (iso: string) => {
> 176	    try { return format(parseISO(iso), "HH:mm", { locale: ptBR }); } catch { return "—"; }
> 177	  };
> 178	  const formatDate = (iso: string) => {
> 179	    try {
> 180	      const date = parseISO(iso);
> 181	      const today = new Date();
> 182	      if (date.toDateString() === today.toDateString()) return "Hoje";
> 183	      const yesterday = new Date(today.getTime() - 86400000);
> 184	      if (date.toDateString() === yesterday.toDateString()) return "Ontem";
> 185	      return format(date, "dd/MM/yyyy", { locale: ptBR });
> 186	    } catch { return "—"; }
> 187	  };
> 188	
> 189	  const groups = messages.reduce((acc: Record<string, MessageRow[]>, msg) => {
> 190	    const date = formatDate(msg.created_at);
> 191	    (acc[date] ||= []).push(msg);
> 192	    return acc;
> 193	  }, {});
> 194	
> 195	  const getContentIcon = (type: MessageRow["content_type"]) => {
> 196	    switch (type) {
> 197	      case "image": return <Image className="w-3.5 h-3.5" />;
> 198	      case "video": return <Video className="w-3.5 h-3.5" />;
> 199	      case "audio": return <Mic className="w-3.5 h-3.5" />;
> 200	      case "document": return <File className="w-3.5 h-3.5" />;
> 201	      case "sticker": return <Smile className="w-3.5 h-3.5" />;
> 202	      case "reaction": return <Smile className="w-3.5 h-3.5" />;
> 203	      case "location": return <MapPin className="w-3.5 h-3.5" />;
> 204	      case "contacts": return <User className="w-3.5 h-3.5" />;
> 205	      case "template": return <FileText className="w-3.5 h-3.5" />;
> 206	      default: return null;
> 207	    }
> 208	  };
> 209	  const TYPE_LABEL: Record<string, string> = {
> 210	    image: "Imagem", video: "Vídeo", audio: "Áudio", document: "Documento",
> 211	    sticker: "Figurinha", reaction: "Reação", location: "Localização", contacts: "Contato",
> 212	  };
> 213	
> 214	  const windowOpen = conversation?.window_expires_at
> ```

## 🤖 Claude *(03:29:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/whatsapp-webhook/index.ts",
  "offset": 290,
  "limit": 55
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 290	          console.error("Failed to upsert conversation:", convErr);
> 291	          pulse("degraded", "conversation_upsert_failed");
> 292	          // Don't 500 — Meta will redeliver; we log and return 200 fast
> 293	        } else {
> 294	          // 5. Insert inbound message with dedup by provider_message_id (Meta redelivers).
> 295	          // content_type now carries the REAL type (the CHECK domain was extended by migration
> 296	          // 20260718230000); only genuinely-unsupported types clamp to 'text' (kept in metadata.wa_type).
> 297	          const contentType = CONTENT_TYPE_DOMAIN.has(waType) ? waType : "text";
> 298	          const messageRecord: Record<string, unknown> = {
> 299	            conversation_id: conversation.id,
> 300	            user_id: tenantId,
> 301	            direction: "inbound",
> 302	            content_type: contentType,
> 303	            body: message.text?.body ?? caption ?? null,
> 304	            provider_message_id: message.id,
> 305	            authored_by: "human",
> 306	            metadata: {
> 307	              sentinel: sentinelResult,
> 308	              backfill: false,
> 309	              wa_type: waType,
> 310	            } as Record<string, unknown>,
> 311	            created_at: timestamp,
> 312	          };
> 313	
> 314	          // Media: persist the pointer + enqueue for the host worker (crm-media-bridge pulls the bytes).
> 315	          if (mediaObj?.id) {
> 316	            messageRecord.media_mime = mediaObj.mime_type ?? null;
> 317	            messageRecord.media_status = "pending";
> 318	            (messageRecord.metadata as Record<string, unknown>).wa_media = {
> 319	              id: mediaObj.id,
> 320	              mime: mediaObj.mime_type ?? null,
> 321	              sha256: mediaObj.sha256 ?? null,
> 322	            };
> 323	          }
> 324	
> 325	          // Reaction: not media — record the emoji + the wamid of the reacted balloon (FR-CRM rich media).
> 326	          if (waType === "reaction" && message.reaction) {
> 327	            messageRecord.reaction_emoji = message.reaction.emoji ?? null;
> 328	            messageRecord.reaction_target_wamid = message.reaction.message_id ?? null;
> 329	          }
> 330	
> 331	          // Location/contacts: structural payloads kept in metadata (no media bytes to pull).
> 332	          if ((waType === "location" || waType === "contacts") && message[waType]) {
> 333	            (messageRecord.metadata as Record<string, unknown>).wa_payload = message[waType];
> 334	          }
> 335	
> 336	          const { error: msgErr } = await admin
> 337	            .from("messages")
> 338	            .insert(messageRecord)
> 339	            // ON CONFLICT (user_id, provider_message_id) DO NOTHING via unique partial index
> 340	            .select("id");
> 341	
> 342	          if (msgErr && msgErr.code !== "23505") {
> 343	            console.error("Failed to insert message:", msgErr);
> 344	            pulse("degraded", "message_insert_failed");
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-18 - eb0262f6-e35f-4101-be5e-35c24a9a5e1f]]
> * **Próxima Sessão**: [[2026-07-19 - Refinar inbox WhatsApp×MIV e enriquecer schema leads]]
%% --- TIMELINE END --- %%
