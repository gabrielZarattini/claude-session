# SOP — Faxina de projeto Spaces (rascunhos/cache) · FR-SPACES-143/144

> Lei 2 (Processo Antecipado). SSOT técnico: `docs/bok/spaces-evolution/39-amendment-project-cleanup.md`.
> Nasceu de dois casos reais de 2026-08-05: (a) faxina incompleta deixou 9 nós do d0d82aeb com
> referências mortas; (b) Passo B disparado sem querer exigiu STOP na fila.

| Campo | Conteúdo |
|-------|----------|
| **Operator** | Dono do projeto, na UI: botão **"Limpar rascunhos"** (TopBar do editor) e **STOP** (Console de Execução). Ops de emergência: scripts da sessão como molde (`emergency-cancel-v2.ts`). |
| **Sequence — faxina** | 1) abrir o projeto → "Limpar rascunhos"; 2) o diálogo roda `dry_run` e mostra contagens (rascunhos · fila · referências mortas) + o que é preservado; 3) confirmar → `execute`; 4) a PRÓPRIA UI reseta os nós cujo output ∈ `gone_keys` (dona do grafo aberto — sem clobber); autosave persiste. |
| **Sequence — STOP** | Por job: ✕ na linha do console (queued nunca roda; running é abortado pelo worker no próximo pulso). Geral: botão STOP no cabeçalho — cancela a fila do projeto + aborta o loop de camadas da aba (pagos não-despachados não despacham). |
| **Verification gates** | G1 dry_run mostra contagens coerentes com o canvas; G2 pós-execute: nós afetados em "não gerado" e Biblioteca sem os rascunhos; G3 masters/vozes/Veo/finais INTACTOS (allowlist `<uid>/motion/`+`<uid>/sfx/` e `asset_role != 'final'` — provado pelo witness E2E); G4 STOP: fila zerada (`video_renders` sem queued/running do projeto). |
| **Recovery** | Rascunho apagado = re-gerável grátis (Executar a fase/nó de novo). Cancelou demais no STOP: re-clicar a fase (prontos não re-executam — FR-142). Referência morta remanescente: reabrir o diálogo (dry_run cura via `dead_references`). |
| **Success signal** | Toast "Faxina concluída — N removidos · M nós resetados"; console vazio; `infra_health_logs` `service=cleanup-project-drafts/spaces-queue-cancel` healthy. |

**Regras invioláveis:** allowlist nunca vira denylist (mídia paga é INAPAGÁVEL por esta rota) ·
`dry_run` é o default da fn (execute exige `dry_run:false` explícito) · deleção de fila só pela fn
(`RLS RESTRICTIVE no-delete` continua para o cliente) · sweep agendado só com opt-in futuro.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%
