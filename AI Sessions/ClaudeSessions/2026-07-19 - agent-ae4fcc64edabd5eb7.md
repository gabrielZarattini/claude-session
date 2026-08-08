# Session agent-ae4fcc64edabd5eb7
**Date:** 2026-07-19 | **Session ID:** `agent-ae4fcc64edabd5eb7`

---

## 👤 User *(23:43:34)*

## Source Extractor

Research question: "Engenharia reversa dos FORMATOS DE VÍDEO CURTO (9:16) que estão VIRALIZANDO e PERFORMANDO AGORA (2025–2026) no nicho de INTELIGÊNCIA ARTIFICIAL / ROBÓTICA / "futuro da tecnologia" / "revolução física" (androides, Boston Dynamics, IA generativa, automação) — em DOIS mercados: (A) GLOBAL/INGLÊS como indicador ANTECEDENTE (onde as tendências nascem, TikTok/Reels/Shorts em inglês) e (B) BRASIL/pt-BR como mercado PRIMÁRIO de conversão (adota tendências globais com atraso, mas tem criadores/achados locais próprios).

Contexto (para ser ACIONÁVEL, não genérico): marca "Gabriel AI / CCIO" (persona de Chief AI Officer). Existem DOIS vídeos LONGOS no YouTube (EP01 "A Revolução Física" sobre IA+robótica; EP02) e DOIS cortes 9:16 já produzidos do EP01. Objetivo: ALCANCE/topo-de-funil — os cortes curtos devem viralizar e FUNILAR os espectadores para os dois vídeos longos.

Entregue um PLAYBOOK acionável e CITADO (cada afirmação ancorada numa fonte verificável com data; priorize 2025–2026; distinga EVIDÊNCIA vs especulação; NUNCA prometa que algo "garante" viralização):
1. ANATOMIA de um Short viral neste nicho: hook dos primeiros 1–3s (padrões concretos de abertura), estrutura de retenção, ritmo/cortes, estilo de texto-na-tela/legendas, duração ideal, uso de áudio/trending sounds, CTA/loop.
2. CRIADORES/CANAIS/EXEMPLOS específicos performando AGORA (nomear, com o que é replicável) — separando globais (inglês) de brasileiros (pt-BR).
3. MECÂNICA por plataforma (TikTok vs Instagram Reels vs YouTube Shorts) para maximizar alcance orgânico em 2025–2026 (o que cada algoritmo premia hoje).
4. Metadados de distribuição: cadência de postagem, hashtags, títulos/captions, capas/covers.
5. APLICAÇÃO CONCRETA aos 2 cortes do EP01 (documental IA/robótica) + o mecanismo de "puxar" o espectador do Short para os vídeos longos EP01/EP02.

Foque em táticas replicáveis e material recente; ignore conselhos atemporais genéricos de "poste com consistência"."

Fetch and extract key claims from this source:
**URL:** https://buffer.com/resources/instagram-algorithms/
**Title:** How the Instagram Algorithm Works: Your 2026 Guide (Buffer)
**Found via:** Mecânica de algoritmo por plataforma search

## Task
1. Use WebFetch to retrieve the page content.
2. Assess source quality: primary research/institution? secondary reporting? blog/opinion? forum? unreliable?
3. Extract 2-5 FALSIFIABLE claims that bear on the research question. Each claim must:
   - be a concrete, checkable statement (not vague generalities)
   - include a direct quote from the source as support
   - be rated central/supporting/tangential to the research question
4. Note publish date if available.

If the fetch fails or the page is irrelevant/paywalled, return claims: [] and sourceQuality: "unreliable".

Structured output only.

## 🤖 Claude *(23:43:38)*

<details>
<summary>💭 Thinking Process</summary>

I need to fetch a URL and evaluate its source quality to extract falsifiable claims about short-form video virality in the AI and robotics space, so let me start by loading the WebFetch tool.

</details>


## 🤖 Claude *(23:43:38)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:WebFetch",
  "max_results": 1
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'WebFetch'}]
> ```

## 🤖 Claude *(23:43:40)*

<details>
<summary>💭 Thinking Process</summary>

I'm going to retrieve the URL and pull out the relevant claims from it.

</details>


## 🤖 Claude *(23:43:43)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://buffer.com/resources/instagram-algorithms/",
  "prompt": "Extract concrete, falsifiable claims about how the Instagram algorithm works in 2025-2026, especially anything relevant to short-form video (Reels) reach and virality: ranking signals the algorithm rewards, the role of sends/shares/saves vs likes, watch time and retention, how reach for non-followers works, posting cadence, hashtags, captions, covers/thumbnails, trending audio, video length, original content vs reposts, and any specific mechanics for maximizing organic reach. For each claim, provide the exact quote from the page. Also note the publish or last-updated date of the article."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Instagram Algorithm Claims: Reels & Organic Reach (2026)
> 
> **Publication Date:** March 24, 2026
> 
> ## Ranking Signals for Reels
> 
> **DM Shares as Primary Signal:**
> "The more your post is shared in this way, the better it will perform." The article emphasizes that sends via direct message carry the heaviest weight for distribution compared to other engagement types.
> 
> **User Activity:**
> "Instagram looks at what reels people have liked, saved, reshared, commented on, and engaged with recently."
> 
> **Early Engagement:**
> Information about the reel itself includes "overall watch time (short, punchy clips tend to win), and early engagement signals influence how widely a reel is distributed."
> 
> ## Video Length & Format
> 
> **Optimal Length:**
> "The ideal reels length for engagement is between 30 and 90 seconds — long enough to cover what matters and short enough to keep people watching."
> 
> **Three-Second Hook:**
> "Those first three seconds decide whether someone keeps watching or scrolls away."
> 
> **Visual Hook Over Sound:**
> "About half of Instagram videos are watched without sound, so your reels need a strong visual hook."
> 
> ## Hashtags & Keywords
> 
> **Hashtag Decline:**
> "Hashtags don't help reach" and "Instagram has made changes to the weight it gives hashtags."
> 
> **Keywords Over Hashtags:**
> "Focus on adding relevant keywords to your post captions and your profile."
> 
> ## Trending Audio
> 
> "When you add these popular sounds to your reels, photo posts, or carousels, your content has a better chance of reaching new people."
> 
> ## Posting Cadence
> 
> **Spacing Posts:**
> "Dumping several posts in a row can cause Instagram to hide some of them to keep feeds balanced."
> 
> ## Original vs. Reposts
> 
> "Instagram wants to reward original content, not posts downloaded from another account and reshared from your own."
> 
> ## Non-Follower Reach
> 
> "Most content in the explore page comes from accounts people don't follow or haven't seen before."
> 
> ## Watermarks & Cross-Platform
> 
> "Reels with logos from other apps will get pushed down in the algorithm. This doesn't apply to your own branding — only to TikTok logos or watermarks from other video editing apps."
> ```

## 🤖 Claude *(23:44:06)*

<details>
<summary>💭 Thinking Process</summary>

Buffer is a reputable social media management platform, and their resources blog offers well-researched, secondary-source content that synthesizes Instagram's official mechanics with editorial rigor. I'd classify this as "secondary" reporting rather than primary, since it's an industry authority synthesizing and reporting on Instagram's stated algorithm mechanics.

Now I'm extracting the most falsifiable claims from their content: DM shares as the heaviest-weighted distribution signal for Reels, the 30-90 second ideal length, the critical first 3 seconds for viewer retention with visual hooks for silent viewing, hashtags being ineffective while captions and profile keywords matter, and how cross-posted content with other platforms' watermarks gets deprioritized. I'll focus on the five strongest and most testable of these claims.

</details>


## 🤖 Claude *(23:44:06)*

The fetch succeeded and the page is highly relevant. Buffer is an established social-media-management company; this is a well-researched, editorially-maintained industry resource (last updated March 24, 2026) that reports Instagram's stated ranking mechanics — I classify it as secondary reporting rather than primary research or personal opinion.

## 🤖 Claude *(23:44:11)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "claims": [
    {
      "claim": "On Instagram in 2026, direct-message shares (sends) are the heaviest-weighted distribution signal for Reels \u2014 sending a reel to friends via DM drives reach more than likes or comments.",
      "quote": "The more your post is shared in this way, the better it will perform.",
      "importance": "central"
    },
    {
      "claim": "The ideal Reels length for engagement in 2026 is 30\u201390 seconds \u2014 long enough to cover the point but short enough to retain viewers.",
      "quote": "The ideal reels length for engagement is between 30 and 90 seconds \u2014 long enough to cover what matters and short enough to keep people watching.",
      "importance": "central"
    },
    {
      "claim": "The first three seconds of a Reel determine whether a viewer keeps watching or scrolls, and because roughly half of Instagram videos are watched without sound, a strong VISUAL hook (not audio) is required.",
      "quote": "Those first three seconds decide whether someone keeps watching or scrolls away.",
      "importance": "central"
    },
    {
      "claim": "Hashtags no longer meaningfully help Reels reach; Instagram now weights relevant keywords in captions and profile text instead of hashtags for discovery.",
      "quote": "Hashtags don't help reach",
      "importance": "supporting"
    },
    {
      "claim": "Reels carrying watermarks or logos from other apps (e.g., TikTok) are algorithmically down-ranked on Instagram, though a creator's own branding is not penalized \u2014 meaning cross-posted clips must have third-party watermarks removed.",
      "quote": "Reels with logos from other apps will get pushed down in the algorithm. This doesn't apply to your own branding \u2014 only to TikTok logos or watermarks from other video editing apps.",
      "importance": "supporting"
    }
  ],
  "publishDate": "2026-03-24",
  "sourceQuality": "secondary"
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-19 - agent-adf44ec88a5ebb6c8]]
> * **Próxima Sessão**: [[2026-07-19 - agent-ae836d797e2099525]]
%% --- TIMELINE END --- %%
