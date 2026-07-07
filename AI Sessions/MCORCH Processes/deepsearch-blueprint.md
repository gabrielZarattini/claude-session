# SOP — Deepsearch Blueprint (semente de BoK fundamentada em pesquisa)

> **Lei 2 (Processo Antecipado).** Este SOP documenta o processo que já rodou manualmente 2×
> com sucesso antes de virar skill/agent: `docs/bok/security/00-deepsearch-blueprint.md`
> (Cyber-Sentinel, 2026-06-09) e `docs/bok/vision-mcp/00-deepsearch-blueprint.md`
> (Vision MCP v0.1.0→v0.2.0, 2026-06-10/11).
>
> **Quando usar:** o Sovereign emite uma diretiva de **módulo novo** ancorada em referência
> externa desconhecida ("a referência é <produto/URL>") ou em temas que exigem fundamento de
> mercado. O Closed-Loop Protocol exige BoK antes de código — e o blueprint é a **semente
> verificada** que alimenta o `/bok-scribe` sem improviso.

---

## Operator

Hoje: **MCORCH Master Execution Agent** (main loop com a tool `Workflow`), sob GO do Sovereign.
Reviewer: Sovereign (revisa o blueprint antes do `/bok-scribe`). Owner: Sovereign.
Forma delegável: subagent `.claude/agents/deepsearch-blueprint.md` (sem `Workflow` — executa as
frentes sequencialmente com WebSearch/WebFetch).

## Sequence

1. **ORO + gate declarado.** Declarar o triplet e afirmar explicitamente: "nenhum código antes
   da BoK" (FM de processo). Critério: o ORO aparece na resposta antes de qualquer tool call.
2. **Workflow de pesquisa (ultracode).** Estrutura provada:
   - **N frentes web** (4-6) em `pipeline()`: cada uma com prompt de domínio + regras duras de
     materialidade (toda claim com URL consultada; sem fonte → `could_not_verify`; NUNCA
     fabricar nome/versão/número).
   - **Verify adversarial por frente** (2º estágio do pipeline): fact-checker independente
     tenta REFUTAR as top ~6 claims com fontes que não sejam a original
     (`confirmed`/`refuted`/`unverifiable`).
   - **Mapeamento do repo em paralelo** (read-only): como o módulo integra ao MCORCH
     (runtime/auth/billing/mesh + assets a reusar), com referências `path:line` concretas.
   - **Completeness critic** (barreira): o que falta para uma BoK honesta? → `critical_gaps`
     (≤6, cada um com `suggested_search`).
   - **Gap-fill** (≤4 em paralelo) → gaps não preenchidos viram OTDs, nunca silêncio.
   - **Síntese**: documento completo PT-BR (termos técnicos em inglês), 10 seções no precedente
     (Sumário honesto · Pilares com veredictos · Arquitetura unificadora · Catálogo de
     referências com URL · Arquitetura MCORCH-nativa · Superfície proposta · FMEA-seed ·
     OTDs · Fatiamento MVP com gates Lei 1 · Apontadores para o BoK).
3. **Escrita em main loop.** O markdown retorna pelo workflow; o main loop grava
   `docs/bok/<slug>/00-deepsearch-blueprint.md` (controle de qualidade fica fora do subagente).
4. **Emendas (v0.x+1)** — quando o Sovereign acrescenta temas: pesquisa só das frentes novas +
   merge agent que **lê o arquivo atual e devolve o documento COMPLETO como superset**.
   Nunca aplicar "patches cegos".

## Verification gates (cada step)

| Gate | Comando/critério | Esperado |
|---|---|---|
| G1 claims verificadas | stats do workflow | `refuted` tratadas (corrigidas/excluídas); 0 claims refutadas no doc final |
| G2 artefato em disco | `ls -la` + `wc -l` + `md5sum` do arquivo | tamanho/linhas citados literais |
| G3 escapes | `grep -c '&gt;\|&lt;\|&amp;'` no markdown extraído | 0 (artefato de notificação ≠ arquivo) |
| G4 superset (emendas) | script python: headers v_old ⊆ v_new (renames intencionais à parte) · 0 OTD/FM IDs perdidos · 0 URLs perdidas · bytes crescem | tudo zero-perda |
| G5 gaps honestos | grep dos `critical_gaps` não preenchidos | todos presentes na seção OTDs |

## Recovery path

- **Session-limit mata o workflow** (sintoma: `failures: [...] session limit · resets HH:MM`):
  NÃO recomece. `Workflow({scriptPath, resumeFromRunId})` — agentes completos voltam do journal
  em cache; só os mortos re-rodam. Provado 2× (2026-06-10 23:58 e 2026-06-11 09:57). Genérico
  para QUALQUER workflow, não só este.
- **Merge agent morreu no meio de edição no arquivo:** SEMPRE faça `cp` + `md5sum` de backup
  ANTES de lançar merge (arquivo não commitado = sem rede git). Ao retomar: `diff` arquivo vs
  backup; se houver edição parcial (ex.: só bump de header), **restaurar o backup limpo** antes
  do resume — o merge agent precisa ler estado honesto.
- **Frente de pesquisa retorna vazio/baixa confiança:** registrar como finding honesto
  ("could not establish") — nunca fabricar perfil do produto-referência.

## Success signal

`docs/bok/<slug>/00-deepsearch-blueprint.md` em disco com md5/linhas citados + gates G1-G5
verdes + resumo ao Sovereign com os vereditos que mudam decisão (ex.: bifurcação de demanda)
+ oferta explícita do próximo passo: `/bok-scribe <slug>`.

---

_Anticorpo do padrão repetido 2× (Obstacle→Synthesis Mandate). Skill: `.claude/skills/deepsearch-blueprint/SKILL.md` · Agent: `.claude/agents/deepsearch-blueprint.md`._

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%
