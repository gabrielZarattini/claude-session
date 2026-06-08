# [[2026-06-08 - Sanitize AI-generated HTML in DashboardHome with DOMPurify|Sanitize AI-generated HTML in DashboardHome with DOMPurify]]
**Date:** 2026-06-04 | **Session ID:** `a5c74064-c02c-4534-8380-0219a737b4b6`

---

## 👤 User *(20:59:54)*

In /home/gcrUX/htdocs/constellation-orchestra, src/pages/DashboardHome.tsx around line 677 renders content_library.body (AI-generated HTML from the orchestrate pipeline) via `dangerouslySetInnerHTML` with no sanitizer. A /security-review flagged this as a pre-existing stored-XSS hardening gap: the field carries raw AI HTML, and if any less-trusted source ever writes content_library.body, the sink becomes exploitable.

Harden it: sanitize the HTML on render with DOMPurify (add the `dompurify` dep if not present) before passing to dangerouslySetInnerHTML — e.g. `dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(item.body) }}`. Check for any OTHER dangerouslySetInnerHTML usages of content_library.body across src/ (grep) and apply the same sanitization consistently. Keep legitimate article formatting (allow standard tags + the affiliate <a href> links the auto-monetize step inserts — DOMPurify's default allows <a>). Verify tsc passes + the dashboard still renders an article with its affiliate links intact.

Context: the auto-monetize feature (OTD-ML-CLICKS) now embeds <a href="...process-affiliate-link?link_id=..."> anchors into article HTML, so the sanitizer must NOT strip <a href> (it doesn't by default, but confirm).

## 🤖 Claude *(21:00:18)*


## 🤖 Claude *(21:00:18)*

Vou começar declarando o ORO triplet e levantando os fatos materiais antes de tocar em qualquer código.

**ORO triplet desta task:**
- **Operator:** AI Agent (MCORCH Master Execution Agent)
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign — blast radius é stored-XSS no dashboard user-facing (renderização de HTML de IA)

Enquadramento do BoK Gate: isto é um **patch de hardening de segurança** escopado a uma feature já documentada (content_library / pipeline orchestrate) + bump de dependência — cai nas isenções do Master Protocol (não é módulo/feature/integração nova). Sigo sob as Leis de Sobrevivência (Materialidade + ORO).

Levantando os fatos em paralelo:

## 🤖 Claude *(21:00:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx",
  "offset": 640,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 640	              <Layers className="h-12 w-12 text-primary/20 mb-4" />
> 641	              <p className="text-muted-foreground text-sm italic">Aguardando ingestão via n8n...</p>
> 642	            </Card>
> 643	          ) : (
> 644	            contentItems.map((item, index) => (
> 645	              <div key={item.id} className="contents">
> 646	                <motion.div
> 647	                  whileHover={{ y: -5 }}
> 648	                  className="group relative flex flex-col glass-panel overflow-hidden transition-all hover:border-primary/40"
> 649	                >
> 650	                  {item.image_url ? (
> 651	                    <div className="h-32 overflow-hidden relative">
> 652	                      <img 
> 653	                        src={item.image_url} 
> 654	                        alt={item.title} 
> 655	                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
> 656	                      />
> 657	                      <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent" />
> 658	                      <Badge className="absolute top-2 right-2 bg-primary/20 backdrop-blur-md text-primary border-none text-[10px]">
> 659	                        {item.category}
> 660	                      </Badge>
> 661	                    </div>
> 662	                  ) : (
> 663	                    <div className="h-32 bg-secondary/30 flex items-center justify-center relative">
> 664	                      <ImageIcon className="h-8 w-8 text-primary/20" />
> 665	                      <Badge className="absolute top-2 right-2 bg-primary/20 backdrop-blur-md text-primary border-none text-[10px]">
> 666	                        {item.category}
> 667	                      </Badge>
> 668	                    </div>
> 669	                  )}
> 670	                  
> 671	                  <CardContent className="p-4 flex-1 flex flex-col">
> 672	                    <h4 className="font-heading font-bold text-sm text-foreground line-clamp-1 mb-2">
> 673	                      {item.title}
> 674	                    </h4>
> 675	                    <div 
> 676	                      className="text-xs text-muted-foreground line-clamp-2 mb-4 flex-1"
> 677	                      dangerouslySetInnerHTML={{ __html: item.content_html }}
> 678	                    />
> 679	                    <div className="flex items-center justify-between mt-auto pt-3 border-t border-primary/10">
> 680	                      <span className="text-[10px] text-muted-foreground flex items-center gap-1">
> 681	                        <Clock className="h-3 w-3" />
> 682	                        {format(parseISO(item.created_at), "dd MMM", { locale: ptBR })}
> 683	                      </span>
> 684	                      <Button variant="ghost" size="icon" className="h-7 w-7 rounded-full hover:bg-primary/20 hover:text-primary">
> 685	                        <ArrowUpRight className="h-3 w-3" />
> 686	                      </Button>
> 687	                    </div>
> 688	                  </CardContent>
> 689	                </motion.div>
> 690	                {(index + 1) % 2 === 0 && <AdPlaceholder />}
> 691	              </div>
> 692	            ))
> 693	          )}
> 694	        </div>
> 695	      </motion.div>
> 696	
> 697	      {/* Charts row */}
> 698	
> 699	      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
> 700	        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="lg:col-span-2">
> 701	          <Card className="glass-panel">
> 702	            <CardHeader className="pb-2">
> 703	              <CardTitle className="font-heading text-base flex items-center gap-2">
> 704	                <TrendingUp className="h-4 w-4 text-primary" />
> 705	                Engajamento Semanal
> 706	              </CardTitle>
> 707	            </CardHeader>
> 708	            <CardContent>
> 709	              <ResponsiveContainer width="100%" height={240}>
> ```

## 🤖 Claude *(21:00:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"dangerouslySetInnerHTML\" src/",
  "description": "Find all dangerouslySetInnerHTML usages in src/"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/pages/DashboardHome.tsx:677:                      dangerouslySetInnerHTML={{ __html: item.content_html }}
> src/components/ui/chart.tsx:70:      dangerouslySetInnerHTML={{
> ```

## 🤖 Claude *(21:00:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"dompurify\\|DOMPurify\" package.json; echo \"---deps---\"; node -e \"const p=require('./package.json'); console.log(JSON.stringify({dep:p.dependencies?.dompurify, dev:p.devDependencies?.dompurify, types:p.devDependencies?.['@types/dompurify']||p.dependencies?.['@types/dompurify']}, null, 2))\"",
  "description": "Check if dompurify is already a dependency"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---deps---
> {}
> ```

## 🤖 Claude *(21:00:36)*


## 🤖 Claude *(21:00:36)*

Dois achados materiais que mudam o plano:

1. **Discrepância com a descrição:** a linha 677 renderiza `item.content_html`, **não** `item.body`. Preciso confirmar que `content_html` é o mapeamento de `content_library.body` antes de prosseguir (Lei 1 — não confiar na descrição).
2. **Segundo sink em `chart.tsx:70`** — provavelmente o injetor de CSS do shadcn chart (não é `content_library.body`). Preciso confirmar para excluí-lo corretamente.
3. **dompurify ausente** do package.json — terei de adicionar.

Investigando a origem de `content_html` e o contexto do segundo sink:

## 🤖 Claude *(21:00:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"content_html\\|contentItems\\|useContent\\|content_library\\|\\.body\" src/pages/DashboardHome.tsx | head -40",
  "description": "Trace content_html source in DashboardHome"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 221:  const [contentItems, setContentItems] = useState<ContentLibraryItem[]>([]);
> 232:          .from('content_library')
> 242:          content_html: item.body || '',
> 260:      .channel('public:content_library')
> 263:        { event: 'INSERT', schema: 'public', table: 'content_library' },
> 269:            content_html: newItem.body || '',
> 638:          ) : contentItems.length === 0 ? (
> 644:            contentItems.map((item, index) => (
> 677:                      dangerouslySetInnerHTML={{ __html: item.content_html }}
> ```

## 🤖 Claude *(21:00:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/ui/chart.tsx",
  "offset": 55,
  "limit": 35
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 55	      </div>
> 56	    </ChartContext.Provider>
> 57	  );
> 58	});
> 59	ChartContainer.displayName = "Chart";
> 60	
> 61	const ChartStyle = ({ id, config }: { id: string; config: ChartConfig }) => {
> 62	  const colorConfig = Object.entries(config).filter(([_, config]) => config.theme || config.color);
> 63	
> 64	  if (!colorConfig.length) {
> 65	    return null;
> 66	  }
> 67	
> 68	  return (
> 69	    <style
> 70	      dangerouslySetInnerHTML={{
> 71	        __html: Object.entries(THEMES)
> 72	          .map(
> 73	            ([theme, prefix]) => `
> 74	${prefix} [data-chart=${id}] {
> 75	${colorConfig
> 76	  .map(([key, itemConfig]) => {
> 77	    const color = itemConfig.theme?.[theme as keyof typeof itemConfig.theme] || itemConfig.color;
> 78	    return color ? `  --color-${key}: ${color};` : null;
> 79	  })
> 80	  .join("\n")}
> 81	}
> 82	`,
> 83	          )
> 84	          .join("\n"),
> 85	      }}
> 86	    />
> 87	  );
> 88	};
> 89	
> ```

## 🤖 Claude *(21:00:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"content_html\" src/ | head -40",
  "description": "Find all content_html references in src/"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/pages/DashboardHome.tsx:242:          content_html: item.body || '',
> src/pages/DashboardHome.tsx:269:            content_html: newItem.body || '',
> src/pages/DashboardHome.tsx:677:                      dangerouslySetInnerHTML={{ __html: item.content_html }}
> src/types/content.ts:4:  content_html: string;
> ```

## 🤖 Claude *(21:01:00)*


## 🤖 Claude *(21:01:00)*

Confirmado materialmente:

- **`content_html` É `content_library.body`** — mapeado em [DashboardHome.tsx:242](src/pages/DashboardHome.tsx:242) (`content_html: item.body || ''`) e no realtime INSERT em [:269](src/pages/DashboardHome.tsx:269). A descrição estava correta em substância; o campo só passa por um alias local.
- **`chart.tsx:70` é o injetor de CSS do shadcn (`ChartStyle`)** — gera `<style>` a partir de `THEMES`×config (CSS dev-controlado), **não** é `content_library.body`. Fora de escopo e sanitizá-lo com DOMPurify quebraria o CSS. Excluído corretamente.
- **Só existe UM sink de `content_library.body`**: [DashboardHome.tsx:677](src/pages/DashboardHome.tsx:677). Aplicação consistente = este único ponto.

Lendo os imports do arquivo e confirmando o gerenciador de pacotes (bun):

## 🤖 Claude *(21:01:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx",
  "offset": 1,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState, useEffect } from 'react';
> 2	import { motion } from 'framer-motion';
> 3	import {
> 4	  CreditCard,
> 5	  Zap,
> 6	  BarChart3,
> 7	  Megaphone,
> 8	  Share2,
> 9	  CalendarCheck,
> 10	  Activity,
> 11	  Clock,
> 12	  TrendingUp,
> 13	  Send,
> 14	  AlertTriangle,
> 15	  CheckCircle2,
> 16	  Brain,
> 17	  Sparkles,
> 18	  ArrowUpRight,
> 19	  Loader2,
> 20	  HeartPulse,
> 21	  Shield,
> 22	  History,
> 23	  RefreshCw,
> 24	  XCircle,
> 25	  Library,
> 26	  Layers,
> 27	  Image as ImageIcon,
> 28	  Wallet,
> 29	  Coins,
> 30	  Trophy,
> 31	} from 'lucide-react';
> 32	import { useScheduledPosts } from '@/hooks/useScheduledPosts';
> 33	import { format, parseISO, startOfDay, endOfDay, addDays } from 'date-fns';
> 34	import { ptBR } from 'date-fns/locale';
> 35	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 36	import { Badge } from '@/components/ui/badge';
> 37	import { Button } from '@/components/ui/button';
> 38	import { useDashboardData } from '@/hooks/useDashboardData';
> 39	import { Skeleton } from '@/components/ui/skeleton';
> 40	import { ConstellationWidget } from '@/components/dashboard/ConstellationWidget';
> ```

## 🤖 Claude *(21:01:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la bun.lockb package-lock.json pnpm-lock.yaml yarn.lock 2>/dev/null; echo \"---\"; node -e \"const p=require('./package.json'); console.log('packageManager:', p.packageManager||'(unset)')\"",
  "description": "Identify the package manager lockfile"
}
```

## 🤖 Claude *(21:01:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/types/content.ts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rwxrwxr-x 1 ubuntu ubuntu 246885 Apr 17 00:26 bun.lockb
> -rw-rw-r-- 1 ubuntu ubuntu 382003 May 14 01:44 package-lock.json
> ---
> packageManager: (unset)
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	export interface ContentLibraryItem {
> 2	  id: string;
> 3	  title: string;
> 4	  content_html: string;
> 5	  category: string;
> 6	  image_url: string;
> 7	  created_at: string;
> 8	}
> 9	
> ```

## 🤖 Claude *(21:01:13)*


## 🤖 Claude *(21:01:13)*

Tenho o quadro completo. Há `bun.lockb` (gerenciador canônico — memória e CLAUDE.md são explícitos: **bun, nunca pnpm**). Antes de instalar, verifico se `dompurify` já existe transitivamente em `node_modules` e se traz types embutidos (v3 traz; `@types/dompurify` seria redundante):

## 🤖 Claude *(21:01:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "if [ -d node_modules/dompurify ]; then\n  echo \"PRESENT (transitive or direct)\";\n  node -e \"const p=require('./node_modules/dompurify/package.json'); console.log('version:', p.version); console.log('types:', p.types||p.typings||'(none bundled)')\";\n  ls node_modules/dompurify/dist/*.d.ts 2>/dev/null || ls node_modules/dompurify/*.d.ts 2>/dev/null || echo \"no top-level d.ts\";\nelse\n  echo \"ABSENT \u2014 needs install\";\nfi",
  "description": "Check dompurify presence and bundled types in node_modules"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ABSENT — needs install
> ```

## 🤖 Claude *(21:01:21)*


## 🤖 Claude *(21:01:21)*

`dompurify` ausente — instalando via bun (gerenciador canônico). DOMPurify v3 traz types próprios, então `@types/dompurify` é dispensável; vou confirmar após instalar:

## 🤖 Claude *(21:01:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun add dompurify 2>&1 | tail -20",
  "description": "Add dompurify dependency via bun",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [0.05ms] ".env"
> bun add v1.3.12 (700fc117)
> Resolving dependencies
> Resolved, downloaded and extracted [5]
> Saved lockfile
> 
> installed dompurify@3.4.8
> 
> 2 packages installed [158.00ms]
> ```

## 🤖 Claude *(21:01:30)*


## 🤖 Claude *(21:01:30)*

`dompurify@3.4.8` instalado. Verificando types embutidos + entrada no package.json:

## 🤖 Claude *(21:01:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "node -e \"const p=require('./node_modules/dompurify/package.json'); console.log('version:', p.version, '| types:', p.types||p.typings||p.exports?.['.']?.types||'(check exports)')\"; echo \"---bundled d.ts---\"; find node_modules/dompurify -name \"*.d.ts\" | head; echo \"---package.json dep---\"; node -e \"const p=require('./package.json'); console.log('dompurify:', p.dependencies?.dompurify)\"",
  "description": "Verify dompurify bundled types and package.json entry"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> version: 3.4.8 | types: ./dist/purify.cjs.d.ts
> ---bundled d.ts---
> node_modules/dompurify/dist/purify.cjs.d.ts
> ---package.json dep---
> dompurify: ^3.4.8
> ```

## 🤖 Claude *(21:03:05)*


## 🤖 Claude *(21:03:07)*

`dompurify@3.4.8` agora é dependência direta (`^3.4.8`) e traz types próprios (`./dist/purify.cjs.d.ts`) — **`@types/dompurify` é dispensável** (seria um stub deprecado de v2).

Aplicando as três edições (import + sanitização + comentário de intenção) em [DashboardHome.tsx](src/pages/DashboardHome.tsx):

## 🤖 Claude *(21:03:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx",
  "old_string": "import { ptBR } from 'date-fns/locale';",
  "new_string": "import { ptBR } from 'date-fns/locale';\nimport DOMPurify from 'dompurify';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:03:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx",
  "old_string": "                      {item.title}\n                    </h4>",
  "new_string": "                      {item.title}\n                    </h4>\n                    {/* content_html = content_library.body (raw AI-generated HTML); DOMPurify sanitizes to close the stored-XSS sink while preserving standard formatting + affiliate <a href> links */}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:03:12)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx",
  "old_string": "                      className=\"text-xs text-muted-foreground line-clamp-2 mb-4 flex-1\"\n                      dangerouslySetInnerHTML={{ __html: item.content_html }}",
  "new_string": "                      className=\"text-xs text-muted-foreground line-clamp-2 mb-4 flex-1\"\n                      dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(item.content_html) }}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:03:24)*


## 🤖 Claude *(21:03:25)*

As três edições aplicadas. Agora a verificação material — primeiro o typecheck (Lei 1). Checando os scripts e rodando `tsc --noEmit`:

## 🤖 Claude *(21:03:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "node -e \"const p=require('./package.json'); console.log(JSON.stringify(p.scripts, null, 2))\"",
  "description": "Show package.json scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {
>   "dev": "vite",
>   "build": "vite build",
>   "build:dev": "vite build --mode development",
>   "lint": "eslint .",
>   "preview": "vite preview",
>   "test": "vitest run",
>   "test:watch": "vitest"
> }
> ```

## 🤖 Claude *(21:03:32)*


## 🤖 Claude *(21:03:32)*

Sem script de typecheck dedicado — rodo `tsc --noEmit` direto. Verificando o tsconfig e executando:

## 🤖 Claude *(21:03:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls tsconfig*.json; echo \"---\"; npx tsc --noEmit 2>&1 | head -40; echo \"---EXIT: ${PIPESTATUS[0]}---\"",
  "description": "Run TypeScript typecheck",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> tsconfig.app.json
> tsconfig.json
> tsconfig.node.json
> ---
> ---EXIT: 0---
> ```

## 🤖 Claude *(21:03:55)*


## 🤖 Claude *(21:03:55)*

`tsc --noEmit` passou — **exit 0, zero erros** (Lei 1: prova literal).

Agora preciso provar materialmente que o sanitizer (a) preserva os links de afiliado `<a href>` e (b) remove vetores XSS. DOMPurify precisa de DOM. O projeto usa vitest — se já houver `jsdom`/`happy-dom` configurado, escrevo um teste que prova o comportamento no harness existente, **sem dep nova e sem subir o app inteiro**. Verificando o ambiente de teste:

## 🤖 Claude *(21:03:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== vite/vitest config (test env) ===\"; grep -rn \"environment\\|jsdom\\|happy-dom\\|setupFiles\" vite.config.ts vitest.config.ts 2>/dev/null; echo \"=== dom libs in node_modules ===\"; for d in jsdom happy-dom; do [ -d \"node_modules/$d\" ] && echo \"$d: PRESENT ($(node -e \"console.log(require('./node_modules/$d/package.json').version)\" 2>/dev/null))\" || echo \"$d: absent\"; done; echo \"=== existing test setup ===\"; ls src/test/ 2>/dev/null | head",
  "description": "Inspect vitest DOM environment and existing test setup"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === vite/vitest config (test env) ===
> vitest.config.ts:8:    environment: "jsdom",
> vitest.config.ts:10:    setupFiles: ["./src/test/setup.ts"],
> === dom libs in node_modules ===
> jsdom: PRESENT (20.0.3)
> happy-dom: absent
> === existing test setup ===
> aios-sql-bridge-smoke.test.ts
> billing.test.ts
> canvas-dag.test.ts
> canvas-handles.test.ts
> canvas-video-async-smoke.test.ts
> e2e-user-zero-selftest.test.ts
> example.test.ts
> marketing-hub.test.ts
> meta.test.ts
> phase-zeta.test.tsx
> ```

## 🤖 Claude *(21:04:25)*


## 🤖 Claude *(21:04:25)*

vitest está configurado com `jsdom@20.0.3` — posso provar o comportamento do sanitizer no harness existente, **sem dep nova**. Escrevo um teste que espelha exatamente a chamada de [DashboardHome.tsx](src/pages/DashboardHome.tsx) (`DOMPurify.sanitize(...)` com perfil default) e prova as duas pontas: links de afiliado preservados + vetores XSS removidos:

## 🤖 Claude *(21:04:37)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/test/dashboard-html-sanitize.test.ts",
  "content": "import { describe, it, expect } from 'vitest';\nimport DOMPurify from 'dompurify';\n\n/**\n * Stored-XSS hardening proof for DashboardHome.\n *\n * `content_library.body` (surfaced as `item.content_html`) is raw AI-generated HTML rendered\n * via `dangerouslySetInnerHTML`. The render now runs it through `DOMPurify.sanitize(...)` with\n * the default profile. These tests mirror that exact call and lock the contract on both ends:\n *   1. legitimate article formatting + the auto-monetize affiliate `<a href>` links survive, and\n *   2. script / event-handler / javascript: XSS vectors are stripped.\n *\n * Runs under the project's jsdom vitest environment, where the default DOMPurify export is the\n * initialized instance exactly as in the browser.\n */\n\n// Shape inserted by the auto-monetize step (OTD-ML-CLICKS): a click-tracked redirect anchor.\nconst AFFILIATE_HREF =\n  'https://abcdefgh.supabase.co/functions/v1/process-affiliate-link?link_id=11111111-2222-3333-4444-555555555555';\n\ndescribe('DashboardHome content_library.body sanitization', () => {\n  it('preserves auto-monetize affiliate <a href> links', () => {\n    const dirty = `<p>Confira este produto.</p><a href=\"${AFFILIATE_HREF}\">Comprar no Mercado Livre</a>`;\n    const clean = DOMPurify.sanitize(dirty);\n    expect(clean).toContain('<a');\n    expect(clean).toContain(`href=\"${AFFILIATE_HREF}\"`);\n    expect(clean).toContain('Comprar no Mercado Livre');\n  });\n\n  it('preserves standard article formatting tags', () => {\n    const dirty =\n      '<h2>T\u00edtulo</h2><p>Par\u00e1grafo com <strong>negrito</strong> e <em>it\u00e1lico</em>.</p><ul><li>item</li></ul>';\n    const clean = DOMPurify.sanitize(dirty);\n    for (const tag of ['<h2>', '<p>', '<strong>', '<em>', '<ul>', '<li>']) {\n      expect(clean).toContain(tag);\n    }\n  });\n\n  it('strips <script> tags (stored-XSS vector)', () => {\n    const clean = DOMPurify.sanitize('<p>ok</p><script>alert(document.cookie)</script>');\n    expect(clean).toContain('<p>ok</p>');\n    expect(clean.toLowerCase()).not.toContain('<script');\n    expect(clean).not.toContain('alert(document.cookie)');\n  });\n\n  it('strips inline event-handler attributes', () => {\n    const clean = DOMPurify.sanitize('<img src=x onerror=\"alert(1)\">');\n    expect(clean.toLowerCase()).not.toContain('onerror');\n  });\n\n  it('neutralizes javascript: hrefs', () => {\n    const clean = DOMPurify.sanitize('<a href=\"javascript:alert(1)\">click</a>');\n    expect(clean.toLowerCase()).not.toContain('javascript:');\n  });\n\n  it('keeps the affiliate link intact even when XSS is interleaved (real article shape)', () => {\n    const dirty = `<h2>Review</h2><p>Texto.</p><a href=\"${AFFILIATE_HREF}\">Oferta</a><script>steal()</script><img src=x onerror=alert(1)>`;\n    const clean = DOMPurify.sanitize(dirty);\n    expect(clean).toContain(`href=\"${AFFILIATE_HREF}\"`);\n    expect(clean.toLowerCase()).not.toContain('<script');\n    expect(clean.toLowerCase()).not.toContain('onerror');\n  });\n});\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/test/dashboard-html-sanitize.test.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:04:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run test src/test/dashboard-html-sanitize.test.ts 2>&1 | tail -30",
  "description": "Run the sanitization proof test",
  "timeout": 120000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> $ vitest run src/test/dashboard-html-sanitize.test.ts
> 
>  RUN  v3.2.4 /home/gcrUX/htdocs/constellation-orchestra
> 
>  ✓ src/test/dashboard-html-sanitize.test.ts (6 tests) 36ms
> 
>  Test Files  1 passed (1)
>       Tests  6 passed (6)
>    Start at  18:04:40
>    Duration  1.14s (transform 50ms, setup 89ms, collect 29ms, tests 36ms, environment 410ms, prepare 104ms)
> ```

## 🤖 Claude *(21:05:02)*


## 🤖 Claude *(21:05:03)*

Os **6 testes passam** — prova material de que o perfil default do DOMPurify preserva os links de afiliado `<a href>` + formatação padrão e remove `<script>`/event-handlers/`javascript:`.

Agora confirmo ausência de regressão: lint nos arquivos tocados + suíte completa de testes (em paralelo):

## 🤖 Claude *(21:05:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx eslint src/pages/DashboardHome.tsx src/test/dashboard-html-sanitize.test.ts 2>&1 | head -30; echo \"---ESLINT EXIT: ${PIPESTATUS[0]}---\"",
  "description": "Lint the changed files",
  "timeout": 120000
}
```

## 🤖 Claude *(21:05:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run test 2>&1 | tail -25; echo \"---FULL SUITE EXIT: ${PIPESTATUS[0]}---\"",
  "description": "Run full test suite for regression check",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/DashboardHome.tsx
>   181:19  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   182:12  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   244:39  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   266:42  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   271:44  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   323:17  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   346:17  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
> 
> ✖ 7 problems (7 errors, 0 warnings)
> 
> ---ESLINT EXIT: 1---
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> stderr | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > does not fall back on a non-billing client error (e.g. 400 bad request)
> [llm-fallback] Primary request failed with status 400 (no fallback triggered)
> 
> stdout | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Attempting primary LLM request with model "anthropic/claude-3.5-sonnet"
> 
> stdout | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Attempting Gemini Free fallback. Candidates: gemini-2.5-pro, gemini-1.5-pro
> [llm-fallback] Dispatching fallback request to Gemini Free using model "gemini-2.5-pro"
> 
> stderr | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Primary request failed (status=402). Initiating cascade. Details: {}
> 
> stdout | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Gemini Free fallback succeeded with model "gemini-2.5-pro"
> 
>  ✓ supabase/functions/_shared/llm-fallback.test.ts (6 tests) 41ms
>  ↓ src/test/aios-sql-bridge-smoke.test.ts (1 test | 1 skipped)
>  ↓ src/test/canvas-video-async-smoke.test.ts (1 test | 1 skipped)
> 
>  Test Files  19 passed | 2 skipped (21)
>       Tests  275 passed | 2 skipped (277)
>    Start at  18:05:06
>    Duration  9.90s (transform 969ms, setup 2.29s, collect 3.74s, tests 1.91s, environment 12.19s, prepare 3.05s)
> 
> ---FULL SUITE EXIT: 0---
> ```

## 🤖 Claude *(21:05:42)*


## 🤖 Claude *(21:05:46)*

Resultados materiais:

- **Suíte completa: EXIT 0** — **275 passed | 2 skipped** (277). Zero regressão; os 2 skips são smokes que dependem de rede.
- **Lint: EXIT 1**, mas os 7 erros são todos `@typescript-eslint/no-explicit-any` em linhas (181, 182, 244, 266, 271, 323, 346) que **não toquei** — código de data-layer pré-existente. Minha mudança não introduz `any`.

Confirmando o escopo exato do meu diff (Lei 1 — provar que os erros de lint são pré-existentes, não meus):

## 🤖 Claude *(21:05:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git --no-pager diff -- src/pages/DashboardHome.tsx; echo \"=== baseline lint on committed HEAD version (proves pre-existing) ===\"; git stash push -q -- src/pages/DashboardHome.tsx && npx eslint src/pages/DashboardHome.tsx 2>&1 | tail -4; git stash pop -q",
  "description": "Show exact diff and baseline lint of committed version",
  "timeout": 120000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/src/pages/DashboardHome.tsx b/src/pages/DashboardHome.tsx
> index a50181e..97149e4 100644
> --- a/src/pages/DashboardHome.tsx
> +++ b/src/pages/DashboardHome.tsx
> @@ -32,6 +32,7 @@ import {
>  import { useScheduledPosts } from '@/hooks/useScheduledPosts';
>  import { format, parseISO, startOfDay, endOfDay, addDays } from 'date-fns';
>  import { ptBR } from 'date-fns/locale';
> +import DOMPurify from 'dompurify';
>  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
>  import { Badge } from '@/components/ui/badge';
>  import { Button } from '@/components/ui/button';
> @@ -672,9 +673,10 @@ export default function DashboardHome() {
>                      <h4 className="font-heading font-bold text-sm text-foreground line-clamp-1 mb-2">
>                        {item.title}
>                      </h4>
> +                    {/* content_html = content_library.body (raw AI-generated HTML); DOMPurify sanitizes to close the stored-XSS sink while preserving standard formatting + affiliate <a href> links */}
>                      <div 
>                        className="text-xs text-muted-foreground line-clamp-2 mb-4 flex-1"
> -                      dangerouslySetInnerHTML={{ __html: item.content_html }}
> +                      dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(item.content_html) }}
>                      />
>                      <div className="flex items-center justify-between mt-auto pt-3 border-t border-primary/10">
>                        <span className="text-[10px] text-muted-foreground flex items-center gap-1">
> === baseline lint on committed HEAD version (proves pre-existing) ===
>   345:17  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
> 
> ✖ 7 problems (7 errors, 0 warnings)
> ```

## 🤖 Claude *(21:06:41)*


## 🤖 Claude *(21:06:51)*

Prova conclusiva: o lint do arquivo **na versão commitada (HEAD), antes da minha mudança, já tinha os mesmos 7 erros** `no-explicit-any` — idênticos. Logo são dívida pré-existente do data-layer, não introduzidos por mim. Meu diff é cirúrgico: 3 linhas (import + comentário + a chamada `DOMPurify.sanitize`).

Não vou commitar (status estava limpo; harness manda só commitar sob pedido). Deixo as mudanças no working tree para sua revisão.

---

## Resumo executivo — hardening stored-XSS selado

**O que foi feito:** o sink `dangerouslySetInnerHTML` que renderiza HTML cru gerado por IA passou a ser sanitizado com DOMPurify (perfil default) antes de chegar ao DOM.

**Achado que corrigiu a premissa (Lei 1 — não confiar na descrição):**
- O campo na linha não é `item.body`, é **`item.content_html`** — mas é alias de `content_library.body`, mapeado em [DashboardHome.tsx:243](src/pages/DashboardHome.tsx:243) (load inicial) e [:270](src/pages/DashboardHome.tsx:270) (realtime INSERT). Ambos desaguam **no mesmo sink único** → sanitizar no ponto de render cobre as duas origens.
- **Só existe 1 sink de `content_library.body`** no `src/`. O outro `dangerouslySetInnerHTML` ([chart.tsx:70](src/components/ui/chart.tsx:70)) é o injetor de CSS do shadcn (`ChartStyle`), dev-controlado — **fora de escopo** e sanitizá-lo quebraria o `<style>`. Excluído conscientemente.

**Mudanças:**
| Arquivo | Mudança |
|---|---|
| [DashboardHome.tsx](src/pages/DashboardHome.tsx) | `import DOMPurify` + `DOMPurify.sanitize(item.content_html)` no sink + comentário de intenção |
| `package.json` / `bun.lockb` | `dompurify@^3.4.8` (dep direta; types embutidos — `@types/dompurify` dispensável) |
| [dashboard-html-sanitize.test.ts](src/test/dashboard-html-sanitize.test.ts) | guarda de regressão do contrato de segurança (novo) |

**Provas materiais (Lei 1):**
- **`tsc --noEmit` → exit 0**, zero erros.
- **Teste do sanitizer → 6/6 passed** (36ms): preserva `<a href=".../process-affiliate-link?link_id=...">` (confirmado: default do DOMPurify mantém `<a href>`) + tags de artigo (`<h2><p><strong><em><ul><li>`); remove `<script>`, `onerror=`, `javascript:`.
- **Suíte completa → exit 0: 275 passed | 2 skipped** (zero regressão; skips são smokes de rede pré-existentes).
- **Lint:** 7 erros `no-explicit-any` — **idênticos no HEAD pré-mudança** (provado via `git stash`), logo dívida pré-existente do data-layer, não minha.

**Sobre "renderiza o artigo com afiliados intactos":** provei isso de forma determinística pelo teste que espelha exatamente a chamada de render (`DOMPurify.sanitize(item.content_html)`), em vez de subir o app com auth + seed de `content_library` — é prova mais forte e não-flaky do contrato específico. Se quiser também a renderização ao vivo no browser (screenshot 1920×1080), eu sigo — precisa de magic-link + uma row de conteúdo com link de afiliado.

**Antibody opcional (Anticorpo Permanente — para evitar reincidência):** posso adicionar a regra ESLint `react/no-danger` para que qualquer novo `dangerouslySetInnerHTML` futuro acuse no lint (com `eslint-disable` explícito no sink legítimo do chart). É uma decisão de design — só faço sob seu GO.

Aguardo GO para commitar (estilo milestone, sem Co-Authored-By, conforme sua diretriz).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-04 - Fix click tracking and complete four priority tasks]]
> * **Próxima Sessão**: [[2026-06-04 - agent-a01fb4360cc1f5068]]
%% --- TIMELINE END --- %%
