# SOP — Pauta de Oportunidades de Receita (FR-VA-031 · HITL)

> **Lei 2 (Processo Antecipado).** SOP do processo humano que a superfície `RevenuePauta`
> (AutopilotPage) automatiza a *apresentação* — a **decisão permanece humana** por design
> ("Receita = pauta humana, não otimização cega", `docs/bok/viral-autopilot/04-frd.md` FR-VA-031).
> Criada 2026-07-02, antes do código (loop autônomo).

## Operator

**Sovereign (Gabriel)** — único decisor de monetização. A UI apenas ranqueia e apresenta;
nenhuma ação de monetização é executada automaticamente.

## Sequence (como o operator decide HOJE, manualmente)

1. Abrir `/dashboard/autopilot` → seção **"Pauta de Receita"**.
2. Ler os candidatos ranqueados — cada linha é um criativo com desempenho REAL coletado
   (`creative_metrics`: impressões, engajamentos, hook rate, cliques de afiliado) e o
   status de monetização derivado de `affiliate_links.content_id`:
   - **candidato** — engajamento alto e NENHUM link de afiliado anexado (a oportunidade);
   - **monetizado** — tem link, ainda sem conversão (`revenue_cents = 0`);
   - **convertendo** — tem link E receita real (`revenue_cents > 0`).
3. Avaliar **retorno × esforço × prioridade** (colunas da UI):
   - *Retorno* = sinal de engajamento real (taxa + volume) — nunca projeção fabricada;
   - *Esforço* = "Baixo — anexar link ML" quando o criativo já tem `product_id` rastreado;
     "Médio — definir produto" quando não tem;
   - *Prioridade* = posição no rank (candidatos primeiro, por engajamento).
4. Decidir por criativo: monetizar (anexar link ML via fluxo vigente `process-affiliate-link`
   / painel de afiliados) · re-amplificar (nova variação no plano) · ignorar.

## Verification gates

| Gate | Critério material |
|---|---|
| G1 — dado real | Toda linha da pauta corresponde a rows reais de `creative_metrics` do tenant (RLS own); lista vazia mostra empty-state honesto, nunca placeholder fabricado. |
| G2 — status correto | `monetizado`/`convertendo` batem com `affiliate_links` (join client-side por `content_id`); um criativo com link nunca aparece como `candidato`. |
| G3 — zero side-effect | A pauta é read-only: nenhuma mutação/débito ao renderizar ou ranquear. |
| G4 — ranking puro testado | `rankRevenueCandidates()` é função pura com testes vitest (agregação, ordenação candidato-primeiro, guard divisão-por-zero). |

## Recovery path

- Query falhou → card mostra erro pt-BR + botão de recarregar (TanStack `refetch`); nunca
  lista parcial silenciosa.
- Métricas ausentes (coletor FR-VA-028 ainda não rodou) → empty-state "coletando desempenho"
  (espelha o insight card do ciclo 1) — **não** degradar para dados de outra fonte.

## Success signal

O Sovereign abre a pauta e vê criativos reais ranqueados com status de monetização correto
(provado por browser-verify + conferência de 1 linha contra o DB). A decisão de monetizar
continua sendo dele — a superfície só elimina a garimpagem manual de métricas.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%
