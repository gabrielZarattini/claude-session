# Scratchpad Harvest — colheita de aprendizado contínuo entre sessões (Lei 2)

> **Nasceu do quase-acidente EP05 (2026-08-03).** A sessão-maratona de produção do master EP05
> deixou os runners (trilha Lyria, assemble, VFX título GSAP, screencast) + 1.9GB de intermediários
> SOMENTE em `/tmp/claude-1001/<projeto>/<sessão>/scratchpad` — diretório volátil, por-sessão, que
> morre num reboot do host. A sessão seguinte recuperou 100% do material **por sorte** (host up
> 7 semanas). O `/handoff` não tinha fase de colheita; agora tem (PHASE 1b). Este SOP é a fonte.

## Operator
O agente da sessão (MCORCH Master Execution Agent), na PHASE 1b do `/handoff` — ou a qualquer
momento em que perceber que material valioso vive só no scratchpad. O Sovereign não executa nada.

## Sequence

1. **Inventário material** — `ls -la <scratchpad>/` + `du -sh <scratchpad>/*/`. Critério de
   sucesso: cada arquivo/dir classificado numa das 4 classes abaixo (nenhum "não sei o que é").
2. **Promover runners/técnicas** → `scripts/<módulo>/` no repo, com nota no README da pasta
   (paths de workdir apontam para o scratchpad de origem — anotar isso). Sucesso: `git status`
   mostra os arquivos staged; commit na Phase 2 do seal.
3. **Promover processos/gates aprendidos** → SOP em `docs/processes/<slug>.md` quando a sequência
   se repetirá (§5 Obstacle→Synthesis do CLAUDE.md). Sucesso: arquivo existe + entra na Key Files
   Reference se for load-bearing.
4. **Promover entregáveis de mídia** → Biblioteca (`canvas-assets` bucket + `register_creative_asset`
   RPC, molde `scripts/ep05/upload-a6.ts`). Sucesso: asset id retornado pela RPC, citado no Record.
5. **Registrar no Record do HANDOFF.md** (Phase 5): path do scratchpad da sessão · lista do que
   foi promovido (paths/ids) · o que ficou para trás como descartável e por quê.

## Classes

| Classe | Critério | Destino |
|--------|----------|---------|
| Runner/técnica | outra sessão precisaria reexecutar/estudar | `scripts/<módulo>/` |
| Processo/gate | sequência com gates que reincide | `docs/processes/` |
| Entregável de mídia | o Sovereign avalia/usa | Biblioteca (asset registrado) |
| Descartável | logs, re-downloads do bucket, venvs, frames intermediários | fica; documentado como descartável |

## Verification gates

- **G1 (promoção real):** todo item classe 1-2 aparece em `git status` antes da Phase 2; todo
  item classe 3 tem asset id de `register_creative_asset`. Claim sem prova = violação Lei 1.
- **G2 (Record cita o path):** o Record novo contém a string `/scratchpad` com o path da sessão.
  Grep mecânico: `grep -c "scratchpad" HANDOFF.md` cresce no seal.
- **G3 (nada órfão):** re-rodar o inventário após a promoção — o que sobrou é só classe 4.

## Recovery path (material de sessão ANTERIOR possivelmente perdido)

1. Scratchpads antigos sobrevivem enquanto o host não reinicia:
   `ls /tmp/claude-1001/<projeto-slug>/` (um UUID por sessão).
2. Localizar por nome de artefato: `find /tmp/claude-1001/<projeto-slug>/ -maxdepth 3 -name "<padrão>"`.
   (Isso NÃO é o "find cego no host" proibido pela skill host-media-masters — o escopo é o diretório
   de scratchpads do projeto, não o filesystem.)
3. Se o host reiniciou e o material morreu: reconstruir a partir do que o Record cita (assets da
   Biblioteca + scripts promovidos). Se o Record não cita nada → o seal violou este SOP; registrar
   o custo real da perda no próximo Record para calibrar o gate.

## Success signal

O `/handson` seguinte consegue retomar a produção SEM arqueologia: os runners estão em
`scripts/<módulo>/`, os entregáveis na Biblioteca, e o Record diz onde está cada coisa.
Prova viva: sessão 2026-08-03b remontou o master EP05 (A6) em minutos porque o A5 local +
speech + segs sobreviveram — com este SOP, isso deixa de depender de sorte.
