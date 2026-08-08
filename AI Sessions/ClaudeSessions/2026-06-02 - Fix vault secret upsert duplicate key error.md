---
type: session-stub
archived: true
original_size_bytes: 428879
original_size: 419 KB
date: 2026-06-02
session_id: c3171bbf-a868-4311-b231-ed1a7ec72ca4
full_path: _full-sessions/ClaudeSessions/2026-06-02 - Fix vault secret upsert duplicate key error.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-02%20-%20Fix%20vault%20secret%20upsert%20duplicate%20key%20error.md
---

# Fix vault secret upsert duplicate key error

> [!abstract] Sessao arquivada
> O conteudo completo (**419 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-02%20-%20Fix%20vault%20secret%20upsert%20duplicate%20key%20error.md)**

- **Data:** 2026-06-02
- **Session ID:** `c3171bbf-a868-4311-b231-ed1a7ec72ca4`
- **Tamanho original:** 419 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-02 - Fix vault secret upsert duplicate key error.md`

## Roteiro da sessao

- Bug de availability confirmado materialmente em 2026-06-02 (sessão do fix do WordPress BYOK), deixado como dív
- You are a senior security engineer conducting a focused security review of the changes on this branch.

## Previa

> # Fix vault secret upsert duplicate key error
> **Date:** 2026-06-02 | **Session ID:** `c3171bbf-a868-4311-b231-ed1a7ec72ca4`
> 
> ---
> 
> ## 👤 User *(14:10:11)*
> 
> Bug de availability confirmado materialmente em 2026-06-02 (sessão do fix do WordPress BYOK), deixado como dívida residual documentada.
> 
> PROBLEMA: O trigger BEFORE INSERT/UPDATE `trg_encrypt_user_api_keys` (em `supabase/migrations/20260601000000_credential_encryption.sql`, recriado em `20260601060000_user_api_keys_apify_token.sql`) chama `vault.create_secret(value, '<nome-deterministico>')` INCONDICIONALMENTE quando uma coluna-segredo muda de valor. `vault.create_secret` faz `INSERT INTO vault.secrets` puro SEM ON CONFLICT, e `vault.secrets.name` tem índice único (`secrets_name_idx`). Logo: editar um segredo para um valor NOVO enquanto o segredo de mesmo nome determinístico ainda existe → `ERROR 23505 duplicate key ... secrets_name_idx`. 
> 
> Para WordPress isso se manifesta no fluxo "Editar senha sem desconectar antes" (em `src/pages/SocialAccountsPage.tsx` o botão "Editar"). Os mesmos triggers irmãos `trg_encrypt_meta_config` e `trg_encrypt_social_accounts` têm o mesmo padrão (nomes por `id` de linha, então re-salvar token na mesma linha também colide).
> 
> CONTEXTO JÁ RESOLVIDO (não refazer): o double-fire do `INSERT...ON CONFLICT` no `trg_instead_of_user_api_keys` foi corrigido em `20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first). O disconnect via `disconnect_wordpress()` deleta o segredo, então connect→disconnect→reconnect funciona. Só falta o caso "trocar valor sem deletar antes".
> 
> FIX PROPOSTO: criar um helper `vault_upsert_secret(p_value text, p_name text, p_desc text) RETURNS uuid` que: `SELECT id FROM vault.secrets WHERE name=p_name`; se achou → `vault.update_secret(id, p_value)` e retorna id; senão → `vault.create_secret(...)`. Substituir as ~11 chamadas `vault.create_secret` em `trg_encrypt_user_api_keys` (e avaliar fazer o mesmo em `trg_encrypt_meta_config`/`trg_encrypt_social_accounts`) por esse helper, preservando o guard de "já é UUID → keep". 
> 
> REQUISITOS: nova migration com timestamp > 20260602130000; OBRIGATÓRIO passar `/security-review` (mexe na camada central de encriptação de credenciais — toda migration passa por /security-review por regra do CLAUDE.md). Verificar materialmente via Management API (token em ~/.supabase/access-token, project ref bcyvddsykvehvpwstlfa, endpoint POST https://api.supabase.com/v1/projects/<ref>/database/query): simular um usuário com set_config('request.jwt.claims', '{"sub":"<uid>","role":"authenticated"}', true) e provar que salvar um segredo DUAS vezes com valores diferentes não dá 23505 e que o decrypted_user_api_keys reflete o 2º valor. Atualizar o SOP `docs/processes/credential-disconnect-clear.md` (seção "Known latent debt") quando fechado.
> 
> ## 🤖 Claude *(14:10:37)*
> 
> 
> ## 🤖 Claude *(14:10:41)*
> 
> Vou começar entendendo materialmente o estado atual da camada de encriptação. Deixe-me declarar o enquadramento e partir para a exploração.
> 
> **ORO triplet desta task:**
> - **Operator:** AI Agent (MCORCH Master Execution Agent)
> - **Reviewer:** Sovereign (Gabriel)
> - **Owner:** Sovereign — blast radius = camada central de encriptação de TODAS as credenciais BYOK de TODOS os tenants; falha em produção = corrupção/perda de segredo Vault ou DoS de salvar credencial.
> 
> Lei 2 (Processo Antecipado): isto é **bug fix em feature já documentada** (SOP `docs/processes/credential-disconnect-clear.md` existe) → sem BoK gate. Mas toca a camada de encriptação → `/security-review` obrigatório.
> 
> Vou explorar o estado material primeiro.
>

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage]]
> * **Próxima Sessão**: [[2026-06-02 - agent-a5d10b1c82e30c144]]
%% --- TIMELINE END --- %%
