# Session agent-acdd7c0c3f0b7eebf
**Date:** 2026-07-20 | **Session ID:** `agent-acdd7c0c3f0b7eebf`

---

## 👤 User *(02:10:22)*


# CONTEXTO REAL (verificado; não invente)

## Objetivo do Sovereign
Transformar /dashboard/youtube em **/dashboard/youtube/studio-yt** — um hub com TUDO do YouTube, incluindo o widget "Publicar vídeo no YouTube" (já existe: YouTubeUploadPanel). A lista "Vídeos do canal (50+)" deve virar clicável: cada vídeo abre uma **página dedicada** com as métricas e análises importantes, **enriquecidas com IA**, explorando as opções NATIVAS da API e envolvendo os **agentes de IA per-user** do ecossistema.

## Escopos OAuth REAIS (verificado em supabase/functions/social-auth-init/index.ts:152-157)
4 escopos concedidos: youtube.readonly · youtube · youtube.force-ssl · **yt-analytics-monetary.readonly**.
O monetário é SUPERSET: concede também as métricas NÃO-monetárias. Portanto SÃO legíveis: average view duration, engaged views, traffic sources, subscribers gained, impressions/CTR, audience retention.
Requer a "YouTube Analytics API" habilitada no projeto Cloud (a checar) e o usuário ter reconectado concedendo os 4.

## Stack existente (REUSAR, não reconstruir)
- Edge fn **youtube-data** (JWT-gated) já implementa: channel_summary · list_videos · video_metrics (Analytics v2) · video_categories · revenue_metrics · update_video · delete_video. Token per-user resolvido server-side de decrypted_social_accounts + refresh-social-token. Gate de escopo fail-closed → 403 youtube_scope_missing com CTA de reconexão.
- Hooks: src/hooks/useYouTubeStudio.ts (useYouTubeConnection/Channel/Videos/ChannelMetrics/Revenue/UpdateVideo/DeleteVideo) e src/hooks/useYouTubeUpload.ts (upload job store).
- Página: src/pages/YouTubeStudioPage.tsx (589 linhas; header + stats + YouTubeUploadPanel + ChannelMetrics + RevenueCard + VideosTable).
- Mapa exaustivo da API: docs/bok/youtube-studio/11-api-surface-map.md (13 recursos · 175 props · 52 métricas · 33 ações) + youtube-api-registry.json.
- IA per-user: BYOK real (user_api_keys/user_provider_keys, resolveProviderKey), edge fns generate-content (streaming), intent-orchestrate/intent-execute; Constellation = cockpit de agentes per-user; openrouter-swarm. Regra perene: seletor de provider só oferece opções BYOK disponíveis (useConfiguredProviders).
- Medição: creative_metrics (hook_rate, impressions, engagements, revenue_cents) + publication_metrics + collective_efficiency_ledger.
- CAP DURO: 100 edge functions (hoje 99). Uma fn NOVA custa um slot — prefira estender youtube-data com novas ACTIONS a criar fn nova.

## Gaps de medição REAIS (achados por crítica adversarial; o gap de escopo era FALSO POSITIVO)
1. creative_metrics.hook_rate é LIDA em 3 lugares e ESCRITA em ZERO — nenhuma edge fn a escreve.
2. Não há coluna de seguidores/inscritos em creative_metrics nem publication_metrics; creative_metrics.source é CHECK FECHADO ('affiliate_click','organic','postback').
3. Δviews de um vídeo pela Data v3 é CUMULATIVO de todas as fontes ⇒ não-atributivo. A atribuição correta Short→longo vem de **traffic source** do Analytics v2, não de subtração de views.
4. Desde 31/03/2025 "view" de Shorts = play-start sem watch-time mínimo; AVD de Shorts usa denominador de ENGAGED VIEWS. Qualquer conta manual watch-time÷views está errada.

## Regras de honestidade (Lei 1)
- NUNCA exibir métrica que a API não devolve. Se algo não é legível, a UI diz isso explicitamente.
- A camada de IA NÃO pode inventar número. Ela INTERPRETA os números que vieram da API. Toda saída de IA precisa ser rastreável ao dado que a originou.
- Nada de "garante" performance.


# SUA TAREFA
Ângulo ARQUITETURA DE INFORMAÇÃO / UX. Defina a estrutura de rotas (/dashboard/youtube/studio-yt como hub + página por-vídeo), o que vai em cada aba da página por-vídeo, como a lista "Vídeos do canal" vira clicável, e onde o widget de upload mora. Reuse os componentes e tokens MIV existentes. Especifique estados vazios/degradados honestos (sem escopo, sem Analytics API habilitada, vídeo sem dados ainda).

Seja concreto e ancorado no repo real (cite arquivos). Nada de genérico.

## 🤖 Claude *(02:10:24)*

I'll investigate the actual repo structure before proposing anything.

## 🤖 Claude *(02:10:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l src/pages/YouTubeStudioPage.tsx src/hooks/useYouTubeStudio.ts src/hooks/useYouTubeUpload.ts 2>/dev/null; ls -la src/components/youtube/",
  "description": "Inspect YouTube module files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   592 src/pages/YouTubeStudioPage.tsx
>   204 src/hooks/useYouTubeStudio.ts
>   209 src/hooks/useYouTubeUpload.ts
>  1005 total
> total 28
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jul 19 16:49 .
> drwxrwxr-x 29 gcrUX  gcrUX   4096 Jul 19 16:49 ..
> -rw-rw-r--  1 ubuntu ubuntu 16764 Jul 19 16:49 YouTubeUploadPanel.tsx
> ```

## 🤖 Claude *(02:10:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"youtube\\|YouTube\" src/App.tsx",
  "description": "Find YouTube routes in App.tsx"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 30:const YouTubeStudioPage = lazy(() => import("./pages/YouTubeStudioPage.tsx"));
> 137:                {/* YouTube Studio hub — tudo do YouTube vive sob /dashboard/youtube/studio-yt.
> 138:                    A rota antiga /dashboard/youtube redireciona para não quebrar links existentes. */}
> 139:                <Route path="youtube" element={<Navigate to="/dashboard/youtube/studio-yt" replace />} />
> 140:                <Route path="youtube/studio-yt" element={<YouTubeStudioPage />} />
> ```

## 🤖 Claude *(02:10:29)*


## 🤖 Claude *(02:10:30)*

Routes already exist. Let me read the actual page and hooks.

## 🤖 Claude *(02:10:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/YouTubeStudioPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useMemo, useState } from 'react';
> 2	import {
> 3	  MonitorPlay,
> 4	  RefreshCw,
> 5	  AlertTriangle,
> 6	  ExternalLink,
> 7	  Eye,
> 8	  ThumbsUp,
> 9	  MessageSquare,
> 10	  Users,
> 11	  Clock,
> 12	  Loader2,
> 13	  Link2,
> 14	  Pencil,
> 15	  Trash2,
> 16	  DollarSign,
> 17	} from 'lucide-react';
> 18	import { toast } from 'sonner';
> 19	import { Button } from '@/components/ui/button';
> 20	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
> 21	import { Badge } from '@/components/ui/badge';
> 22	import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
> 23	import { Skeleton } from '@/components/ui/skeleton';
> 24	import { Input } from '@/components/ui/input';
> 25	import { Textarea } from '@/components/ui/textarea';
> 26	import { Label } from '@/components/ui/label';
> 27	import {
> 28	  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter,
> 29	} from '@/components/ui/dialog';
> 30	import {
> 31	  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
> 32	  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
> 33	} from '@/components/ui/alert-dialog';
> 34	import {
> 35	  useYouTubeConnection,
> 36	  useYouTubeChannel,
> 37	  useYouTubeVideos,
> 38	  useYouTubeChannelMetrics,
> 39	  useYouTubeRevenue,
> 40	  useUpdateVideo,
> 41	  useDeleteVideo,
> 42	  type YouTubeVideo,
> 43	} from '@/hooks/useYouTubeStudio';
> 44	import { YouTubeUploadPanel } from '@/components/youtube/YouTubeUploadPanel';
> 45	
> 46	// ── Formatting helpers ──────────────────────────────────────────────────────
> 47	function formatNumber(v?: string | number): string {
> 48	  const n = typeof v === 'string' ? Number(v) : v;
> 49	  if (n === undefined || n === null || Number.isNaN(n)) return '—';
> 50	  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
> 51	  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`;
> 52	  return String(n);
> 53	}
> 54	
> 55	function formatDuration(iso?: string): string {
> 56	  if (!iso) return '—';
> 57	  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
> 58	  if (!m) return '—';
> 59	  const h = Number(m[1] ?? 0);
> 60	  const min = Number(m[2] ?? 0);
> 61	  const s = Number(m[3] ?? 0);
> 62	  const pad = (x: number) => String(x).padStart(2, '0');
> 63	  return h > 0 ? `${h}:${pad(min)}:${pad(s)}` : `${min}:${pad(s)}`;
> 64	}
> 65	
> 66	function formatDate(iso?: string): string {
> 67	  if (!iso) return '—';
> 68	  const d = new Date(iso);
> 69	  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleDateString('pt-BR');
> 70	}
> 71	
> 72	function formatSeconds(v?: string | number): string {
> 73	  const n = typeof v === 'string' ? Number(v) : v;
> 74	  if (n === undefined || n === null || Number.isNaN(n)) return '—';
> 75	  const min = Math.floor(n / 60);
> 76	  const s = Math.round(n % 60);
> 77	  return `${min}:${String(s).padStart(2, '0')}`;
> 78	}
> 79	
> 80	function privacyBadge(status?: string) {
> 81	  const map: Record<string, string> = {
> 82	    public: 'border-cyan-500/40 text-cyan-300 bg-cyan-500/10',
> 83	    unlisted: 'border-amber-500/40 text-amber-300 bg-amber-500/10',
> 84	    private: 'border-zinc-500/40 text-zinc-300 bg-zinc-500/10',
> 85	  };
> 86	  return map[status ?? ''] ?? 'border-zinc-500/40 text-zinc-300 bg-zinc-500/10';
> 87	}
> 88	
> 89	// ── Metrics card ────────────────────────────────────────────────────────────
> 90	function ChannelMetrics() {
> 91	  const { data, isLoading, isError, error } = useYouTubeChannelMetrics();
> 92	
> 93	  const metrics = useMemo(() => {
> 94	    if (!data?.columnHeaders?.length || !data.rows?.length) return null;
> 95	    const row = data.rows[0];
> 96	    return Object.fromEntries(
> 97	      data.columnHeaders.map((h, i) => [h.name, row[i]]),
> 98	    ) as Record<string, string | number>;
> 99	  }, [data]);
> 100	
> 101	  if (isLoading) return <Skeleton className="h-28 w-full rounded-xl" />;
> 102	  if (isError) {
> 103	    return (
> 104	      <Card className="border-amber-500/30 bg-amber-500/5">
> 105	        <CardContent className="py-4 text-sm text-amber-300">
> 106	          Métricas indisponíveis: {(error as Error)?.message}
> 107	        </CardContent>
> 108	      </Card>
> 109	    );
> 110	  }
> 111	  if (!metrics) return null;
> 112	
> 113	  const gained = Number(metrics.subscribersGained ?? 0) - Number(metrics.subscribersLost ?? 0);
> 114	  const tiles = [
> 115	    { label: 'Views (28d)', value: formatNumber(metrics.views), icon: Eye },
> 116	    { label: 'Min. assistidos', value: formatNumber(metrics.estimatedMinutesWatched), icon: Clock },
> 117	    { label: 'Duração média', value: formatSeconds(metrics.averageViewDuration), icon: Clock },
> 118	    { label: '% médio assistido', value: metrics.averageViewPercentage != null ? `${Number(metrics.averageViewPercentage).toFixed(1)}%` : '—', icon: Eye },
> 119	    { label: 'Inscritos líq.', value: `${gained >= 0 ? '+' : ''}${gained}`, icon: Users },
> 120	    { label: 'Curtidas', value: formatNumber(metrics.likes), icon: ThumbsUp },
> 121	  ];
> 122	
> 123	  return (
> 124	    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
> 125	      {tiles.map((t) => (
> 126	        <Card key={t.label} className="bg-card/60">
> 127	          <CardContent className="flex flex-col gap-1 py-4">
> 128	            <t.icon className="h-4 w-4 text-cyan-400" />
> 129	            <span className="text-xl font-semibold tabular-nums">{t.value}</span>
> 130	            <span className="text-xs text-muted-foreground">{t.label}</span>
> 131	          </CardContent>
> 132	        </Card>
> 133	      ))}
> 134	    </div>
> 135	  );
> 136	}
> 137	
> 138	// ── Revenue card (Fatia 2 — força o escopo yt-analytics-monetary.readonly) ──────
> 139	function RevenueCard() {
> 140	  const { data, isLoading, isError, error } = useYouTubeRevenue();
> 141	
> 142	  const money = useMemo(() => {
> 143	    if (!data || !data.monetized || !data.rows?.length) return null;
> 144	    const row = data.rows[0];
> 145	    const out: Record<string, number> = {};
> 146	    data.columnHeaders.forEach((c, i) => { out[c.name] = Number(row[i] ?? 0); });
> 147	    return out;
> 148	  }, [data]);
> 149	
> 150	  if (isLoading) return <Skeleton className="h-24 w-full rounded-xl" />;
> 151	  if (isError) {
> 152	    return (
> 153	      <Card className="border-amber-500/30 bg-amber-500/5">
> 154	        <CardContent className="py-4 text-sm text-amber-300">
> 155	          Não foi possível carregar a receita: {(error as Error)?.message}
> 156	        </CardContent>
> 157	      </Card>
> 158	    );
> 159	  }
> 160	  // monetized:false is a valid state — the call still proved the monetary scope.
> 161	  if (!data?.monetized || !money) {
> 162	    return (
> 163	      <Card className="bg-card/60">
> 164	        <CardContent className="flex items-center gap-3 py-4 text-sm text-muted-foreground">
> 165	          <DollarSign className="h-4 w-4 text-emerald-400" />
> 166	          Sem dados de receita no período — o canal não está monetizado (fora do YouTube Partner Program) ou
> 167	          não gerou receita nos últimos 28 dias.
> 168	        </CardContent>
> 169	      </Card>
> 170	    );
> 171	  }
> 172	
> 173	  const fmtUsd = (v: number) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'USD' });
> 174	  const tiles = [
> 175	    { label: 'Receita estimada', value: fmtUsd(money.estimatedRevenue ?? 0) },
> 176	    { label: 'Receita de anúncios', value: fmtUsd(money.estimatedAdRevenue ?? 0) },
> 177	    { label: 'CPM', value: fmtUsd(money.cpm ?? 0) },
> 178	    { label: 'Reproduções monetizadas', value: formatNumber(money.monetizedPlaybacks ?? 0) },
> 179	  ];
> 180	  return (
> 181	    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
> 182	      {tiles.map((t) => (
> 183	        <Card key={t.label} className="bg-card/60">
> 184	          <CardContent className="flex flex-col gap-1 py-4">
> 185	            <DollarSign className="h-4 w-4 text-emerald-400" />
> 186	            <span className="text-lg font-semibold tabular-nums">{t.value}</span>
> 187	            <span className="text-xs text-muted-foreground">{t.label}</span>
> 188	          </CardContent>
> 189	        </Card>
> 190	      ))}
> 191	    </div>
> 192	  );
> 193	}
> 194	
> 195	// ── Edit video dialog (Fatia 2 — força youtube.force-ssl via videos.update) ──────
> 196	function EditVideoDialog({ video, onClose }: { video: YouTubeVideo | null; onClose: () => void }) {
> 197	  const update = useUpdateVideo();
> 198	  const [title, setTitle] = useState('');
> 199	  const [description, setDescription] = useState('');
> 200	
> 201	  // Seed the fields when a video is opened (keyed remount via `key` on the caller keeps this simple).
> 202	  useMemo(() => {
> 203	    setTitle(video?.snippet?.title ?? '');
> 204	    setDescription(video?.snippet?.description ?? '');
> 205	  }, [video]);
> 206	
> 207	  if (!video) return null;
> 208	  const save = async () => {
> 209	    try {
> 210	      await update.mutateAsync({ videoId: video.id, title: title.trim(), description });
> 211	      toast.success('Vídeo atualizado no YouTube.');
> 212	      onClose();
> 213	    } catch (e) {
> 214	      toast.error((e as Error).message);
> 215	    }
> 216	  };
> 217	  return (
> 218	    <Dialog open={!!video} onOpenChange={(o) => !o && onClose()}>
> 219	      <DialogContent className="sm:max-w-lg">
> 220	        <DialogHeader>
> 221	          <DialogTitle>Editar vídeo</DialogTitle>
> 222	          <DialogDescription>Altera o título e a descrição direto no seu canal do YouTube (videos.update).</DialogDescription>
> 223	        </DialogHeader>
> 224	        <div className="space-y-3">
> 225	          <div className="space-y-1">
> 226	            <Label htmlFor="yt-title">Título</Label>
> 227	            <Input id="yt-title" value={title} onChange={(e) => setTitle(e.target.value)} maxLength={100} />
> 228	          </div>
> 229	          <div className="space-y-1">
> 230	            <Label htmlFor="yt-desc">Descrição</Label>
> 231	            <Textarea id="yt-desc" value={description} onChange={(e) => setDescription(e.target.value)} rows={5} maxLength={5000} />
> 232	          </div>
> 233	        </div>
> 234	        <DialogFooter>
> 235	          <Button variant="outline" onClick={onClose} disabled={update.isPending}>Cancelar</Button>
> 236	          <Button onClick={save} disabled={update.isPending || !title.trim()} className="gap-2">
> 237	            {update.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Pencil className="h-4 w-4" />}
> 238	            Salvar no YouTube
> 239	          </Button>
> 240	        </DialogFooter>
> 241	      </DialogContent>
> 242	    </Dialog>
> 243	  );
> 244	}
> 245	
> 246	// ── Videos table ────────────────────────────────────────────────────────────
> 247	const COLUMNS = [
> 248	  'Vídeo', 'Publicado', 'Privacidade', 'Upload', 'Duração', 'Def',
> 249	  'Views', 'Likes', 'Coment.', 'Tags', 'Cat.', 'Kids', 'Licença', 'Embed', 'Sintético', 'ID',
> 250	];
> 251	
> 252	function VideoRow({
> 253	  v, canWrite, onEdit, onDelete,
> 254	}: {
> 255	  v: YouTubeVideo;
> 256	  canWrite: boolean;
> 257	  onEdit: (v: YouTubeVideo) => void;
> 258	  onDelete: (v: YouTubeVideo) => void;
> 259	}) {
> 260	  const thumb = v.snippet?.thumbnails?.default?.url ?? v.snippet?.thumbnails?.medium?.url;
> 261	  return (
> 262	    <TableRow>
> 263	      <TableCell className="min-w-[280px]">
> 264	        <div className="flex items-center gap-3">
> 265	          {thumb ? (
> 266	            <img src={thumb} alt="" className="h-10 w-16 flex-shrink-0 rounded object-cover" loading="lazy" />
> 267	          ) : (
> 268	            <div className="h-10 w-16 flex-shrink-0 rounded bg-muted" />
> 269	          )}
> 270	          <div className="min-w-0">
> 271	            <a
> 272	              href={`https://youtube.com/watch?v=${v.id}`}
> 273	              target="_blank"
> 274	              rel="noreferrer"
> 275	              className="line-clamp-2 text-sm font-medium hover:text-cyan-300"
> 276	            >
> 277	              {v.snippet?.title ?? '(sem título)'}
> 278	            </a>
> 279	          </div>
> 280	        </div>
> 281	      </TableCell>
> 282	      <TableCell className="whitespace-nowrap text-xs text-muted-foreground">{formatDate(v.snippet?.publishedAt)}</TableCell>
> 283	      <TableCell>
> 284	        <Badge variant="outline" className={privacyBadge(v.status?.privacyStatus)}>
> 285	          {v.status?.privacyStatus ?? '—'}
> 286	        </Badge>
> 287	      </TableCell>
> 288	      <TableCell className="whitespace-nowrap text-xs">{v.status?.uploadStatus ?? '—'}</TableCell>
> 289	      <TableCell className="whitespace-nowrap tabular-nums text-xs">{formatDuration(v.contentDetails?.duration)}</TableCell>
> 290	      <TableCell className="text-xs uppercase">{v.contentDetails?.definition ?? '—'}</TableCell>
> 291	      <TableCell className="tabular-nums">{formatNumber(v.statistics?.viewCount)}</TableCell>
> 292	      <TableCell className="tabular-nums">{formatNumber(v.statistics?.likeCount)}</TableCell>
> 293	      <TableCell className="tabular-nums">{formatNumber(v.statistics?.commentCount)}</TableCell>
> 294	      <TableCell className="tabular-nums text-xs">{v.snippet?.tags?.length ?? 0}</TableCell>
> 295	      <TableCell className="text-xs">{v.snippet?.categoryId ?? '—'}</TableCell>
> 296	      <TableCell className="text-xs">{v.status?.madeForKids ? 'Sim' : 'Não'}</TableCell>
> 297	      <TableCell className="text-xs">{v.status?.license ?? '—'}</TableCell>
> 298	      <TableCell className="text-xs">{v.status?.embeddable ? 'Sim' : 'Não'}</TableCell>
> 299	      <TableCell className="text-xs">{v.status?.containsSyntheticMedia ? 'Sim' : '—'}</TableCell>
> 300	      <TableCell className="font-mono text-[10px] text-muted-foreground">{v.id}</TableCell>
> 301	      {canWrite && (
> 302	        <TableCell className="whitespace-nowrap">
> 303	          <div className="flex items-center gap-1">
> 304	            <Button variant="ghost" size="icon" className="h-7 w-7" title="Editar" onClick={() => onEdit(v)}>
> 305	              <Pencil className="h-3.5 w-3.5" />
> 306	            </Button>
> 307	            <Button
> 308	              variant="ghost" size="icon"
> 309	              className="h-7 w-7 text-destructive hover:text-destructive"
> 310	              title="Excluir permanentemente"
> 311	              onClick={() => onDelete(v)}
> 312	            >
> 313	              <Trash2 className="h-3.5 w-3.5" />
> 314	            </Button>
> 315	          </div>
> 316	        </TableCell>
> 317	      )}
> 318	    </TableRow>
> 319	  );
> 320	}
> 321	
> 322	function VideosTable({ canWrite }: { canWrite: boolean }) {
> 323	  const { videos, isLoading, isError, error, hasNextPage, isFetchingNextPage, fetchNextPage, refetch, isRefetching } =
> 324	    useYouTubeVideos();
> 325	  const [editing, setEditing] = useState<YouTubeVideo | null>(null);
> 326	  const [deleting, setDeleting] = useState<YouTubeVideo | null>(null);
> 327	  const del = useDeleteVideo();
> 328	
> 329	  const confirmDelete = async () => {
> 330	    if (!deleting) return;
> 331	    try {
> 332	      await del.mutateAsync(deleting.id);
> 333	      toast.success('Vídeo excluído permanentemente do YouTube.');
> 334	      setDeleting(null);
> 335	    } catch (e) {
> 336	      toast.error((e as Error).message);
> 337	    }
> 338	  };
> 339	
> 340	  if (isLoading) {
> 341	    return (
> 342	      <div className="space-y-2">
> 343	        {Array.from({ length: 6 }).map((_, i) => (
> 344	          <Skeleton key={i} className="h-14 w-full rounded" />
> 345	        ))}
> 346	      </div>
> 347	    );
> 348	  }
> 349	  if (isError) {
> 350	    return (
> 351	      <Card className="border-amber-500/30 bg-amber-500/5">
> 352	        <CardContent className="py-4 text-sm text-amber-300">
> 353	          Não foi possível listar os vídeos: {(error as Error)?.message}
> 354	        </CardContent>
> 355	      </Card>
> 356	    );
> 357	  }
> 358	
> 359	  return (
> 360	    <Card>
> 361	      <CardHeader className="flex flex-row items-center justify-between gap-2">
> 362	        <div>
> 363	          <CardTitle className="text-base">Vídeos do canal ({videos.length}{hasNextPage ? '+' : ''})</CardTitle>
> 364	          <CardDescription>
> 365	            {canWrite
> 366	              ? 'Tabela completa da API + ações de edição e exclusão dos seus próprios vídeos.'
> 367	              : 'Tabela completa de propriedades da API (somente leitura).'}
> 368	          </CardDescription>
> 369	        </div>
> 370	        <Button variant="outline" size="sm" onClick={() => refetch()} disabled={isRefetching}>
> 371	          <RefreshCw className={`h-4 w-4 ${isRefetching ? 'animate-spin' : ''}`} />
> 372	          Atualizar
> 373	        </Button>
> 374	      </CardHeader>
> 375	      <CardContent>
> 376	        <div className="overflow-x-auto">
> 377	          <Table>
> 378	            <TableHeader>
> 379	              <TableRow>
> 380	                {COLUMNS.map((c) => (
> 381	                  <TableHead key={c} className="whitespace-nowrap text-xs">{c}</TableHead>
> 382	                ))}
> 383	                {canWrite && <TableHead className="whitespace-nowrap text-xs">Ações</TableHead>}
> 384	              </TableRow>
> 385	            </TableHeader>
> 386	            <TableBody>
> 387	              {videos.map((v) => (
> 388	                <VideoRow key={v.id} v={v} canWrite={canWrite} onEdit={setEditing} onDelete={setDeleting} />
> 389	              ))}
> 390	            </TableBody>
> 391	          </Table>
> 392	        </div>
> 393	        {hasNextPage && (
> 394	          <div className="mt-4 flex justify-center">
> 395	            <Button variant="outline" onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
> 396	              {isFetchingNextPage ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
> 397	              Carregar mais
> 398	            </Button>
> 399	          </div>
> 400	        )}
> 401	      </CardContent>
> 402	
> 403	      {/* Fatia 2 — edit (keyed remount seeds the fields) + destructive delete confirmation. */}
> 404	      <EditVideoDialog key={editing?.id ?? 'none'} video={editing} onClose={() => setEditing(null)} />
> 405	      <AlertDialog open={!!deleting} onOpenChange={(o) => !o && setDeleting(null)}>
> 406	        <AlertDialogContent>
> 407	          <AlertDialogHeader>
> 408	            <AlertDialogTitle>Excluir vídeo permanentemente?</AlertDialogTitle>
> 409	            <AlertDialogDescription>
> 410	              "{deleting?.snippet?.title ?? deleting?.id}" será removido do seu canal do YouTube de forma
> 411	              PERMANENTE e irreversível (videos.delete). Esta ação não pode ser desfeita.
> 412	            </AlertDialogDescription>
> 413	          </AlertDialogHeader>
> 414	          <AlertDialogFooter>
> 415	            <AlertDialogCancel disabled={del.isPending}>Cancelar</AlertDialogCancel>
> 416	            <AlertDialogAction
> 417	              onClick={(e) => { e.preventDefault(); confirmDelete(); }}
> 418	              disabled={del.isPending}
> 419	              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
> 420	            >
> 421	              {del.isPending ? <Loader2 className="mr-1 h-4 w-4 animate-spin" /> : <Trash2 className="mr-1 h-4 w-4" />}
> 422	              Excluir permanentemente
> 423	            </AlertDialogAction>
> 424	          </AlertDialogFooter>
> 425	        </AlertDialogContent>
> 426	      </AlertDialog>
> 427	    </Card>
> 428	  );
> 429	}
> 430	
> 431	// ── Page ────────────────────────────────────────────────────────────────────
> 432	export default function YouTubeStudioPage() {
> 433	  const conn = useYouTubeConnection();
> 434	  const { channel } = useYouTubeChannel();
> 435	
> 436	  const header = (
> 437	    <div className="flex flex-wrap items-center justify-between gap-3">
> 438	      <div className="flex items-center gap-3">
> 439	        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-red-600/15 text-red-400">
> 440	          <MonitorPlay className="h-6 w-6" />
> 441	        </div>
> 442	        <div>
> 443	          <h1 className="text-xl font-semibold">YouTube Studio</h1>
> 444	          <p className="text-sm text-muted-foreground">
> 445	            {conn.channelTitle ? `Canal conectado: ${conn.channelTitle}` : 'Gestão do canal conectado ao MCORCH'}
> 446	          </p>
> 447	        </div>
> 448	      </div>
> 449	      {channel?.snippet?.customUrl && (
> 450	        <a
> 451	          href={`https://youtube.com/${channel.snippet.customUrl}`}
> 452	          target="_blank"
> 453	          rel="noreferrer"
> 454	          className="inline-flex items-center gap-1 text-sm text-cyan-300 hover:underline"
> 455	        >
> 456	          {channel.snippet.customUrl} <ExternalLink className="h-3.5 w-3.5" />
> 457	        </a>
> 458	      )}
> 459	    </div>
> 460	  );
> 461	
> 462	  if (conn.isLoading) {
> 463	    return (
> 464	      <div className="space-y-6 p-6">
> 465	        {header}
> 466	        <Skeleton className="h-28 w-full rounded-xl" />
> 467	      </div>
> 468	    );
> 469	  }
> 470	
> 471	  // Not connected → connect CTA
> 472	  if (!conn.isConnected) {
> 473	    return (
> 474	      <div className="space-y-6 p-6">
> 475	        {header}
> 476	        <Card className="border-cyan-500/20">
> 477	          <CardContent className="flex flex-col items-center gap-4 py-12 text-center">
> 478	            <Link2 className="h-10 w-10 text-cyan-400" />
> 479	            <div>
> 480	              <p className="font-medium">Nenhum canal do YouTube conectado</p>
> 481	              <p className="text-sm text-muted-foreground">
> 482	                Conecte o canal para ler vídeos e métricas diretamente no MCORCH.
> 483	              </p>
> 484	            </div>
> 485	            <Button onClick={conn.connect} className="gap-2">
> 486	              <MonitorPlay className="h-4 w-4" /> Conectar YouTube
> 487	            </Button>
> 488	          </CardContent>
> 489	        </Card>
> 490	      </div>
> 491	    );
> 492	  }
> 493	
> 494	  // Connected but missing read/analytics scopes → reconnect CTA (fail-closed, no API call fired)
> 495	  if (conn.needsReconnect) {
> 496	    return (
> 497	      <div className="space-y-6 p-6">
> 498	        {header}
> 499	        <Card className="border-amber-500/40 bg-amber-500/5">
> 500	          <CardContent className="flex flex-col gap-4 py-8">
> 501	            <div className="flex items-start gap-3">
> 502	              <AlertTriangle className="mt-0.5 h-5 w-5 flex-shrink-0 text-amber-400" />
> 503	              <div className="space-y-1">
> 504	                <p className="font-medium text-amber-200">Permissões insuficientes para ler o canal</p>
> 505	                <p className="text-sm text-amber-200/80">
> 506	                  A conexão atual só permite publicar. Para listar os vídeos do canal, reconecte
> 507	                  concedendo a permissão de leitura do YouTube.
> 508	                </p>
> 509	              </div>
> 510	            </div>
> 511	            <div>
> 512	              <Button onClick={conn.reconnect} className="gap-2">
> 513	                <RefreshCw className="h-4 w-4" /> Reconectar com permissões ampliadas
> 514	              </Button>
> 515	            </div>
> 516	          </CardContent>
> 517	        </Card>
> 518	      </div>
> 519	    );
> 520	  }
> 521	
> 522	  // Fully connected + scoped → channel summary + metrics + videos table
> 523	  const stats = channel?.statistics;
> 524	  return (
> 525	    <div className="space-y-6 p-6">
> 526	      {header}
> 527	
> 528	      {stats && (
> 529	        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
> 530	          <Card className="bg-card/60">
> 531	            <CardContent className="flex flex-col gap-1 py-4">
> 532	              <Users className="h-4 w-4 text-cyan-400" />
> 533	              <span className="text-xl font-semibold tabular-nums">{formatNumber(stats.subscriberCount)}</span>
> 534	              <span className="text-xs text-muted-foreground">Inscritos</span>
> 535	            </CardContent>
> 536	          </Card>
> 537	          <Card className="bg-card/60">
> 538	            <CardContent className="flex flex-col gap-1 py-4">
> 539	              <Eye className="h-4 w-4 text-cyan-400" />
> 540	              <span className="text-xl font-semibold tabular-nums">{formatNumber(stats.viewCount)}</span>
> 541	              <span className="text-xs text-muted-foreground">Views totais</span>
> 542	            </CardContent>
> 543	          </Card>
> 544	          <Card className="bg-card/60">
> 545	            <CardContent className="flex flex-col gap-1 py-4">
> 546	              <MonitorPlay className="h-4 w-4 text-cyan-400" />
> 547	              <span className="text-xl font-semibold tabular-nums">{formatNumber(stats.videoCount)}</span>
> 548	              <span className="text-xs text-muted-foreground">Vídeos públicos</span>
> 549	            </CardContent>
> 550	          </Card>
> 551	          <Card className="bg-card/60">
> 552	            <CardContent className="flex flex-col gap-1 py-4">
> 553	              <MessageSquare className="h-4 w-4 text-cyan-400" />
> 554	              <span className="text-sm font-medium">{channel?.snippet?.country ?? '—'}</span>
> 555	              <span className="text-xs text-muted-foreground">País</span>
> 556	            </CardContent>
> 557	          </Card>
> 558	        </div>
> 559	      )}
> 560	
> 561	      <YouTubeUploadPanel />
> 562	
> 563	      <div className="space-y-2">
> 564	        <h2 className="text-sm font-medium text-muted-foreground">Desempenho (últimos 28 dias)</h2>
> 565	        {conn.hasAnalyticsScope ? (
> 566	          <ChannelMetrics />
> 567	        ) : (
> 568	          <Card className="border-cyan-500/20 bg-cyan-500/5">
> 569	            <CardContent className="flex flex-wrap items-center justify-between gap-3 py-4">
> 570	              <p className="text-sm text-muted-foreground">
> 571	                As métricas de desempenho exigem a permissão de <strong>Analytics</strong> do YouTube
> 572	                (habilite a YouTube Analytics API no projeto e reconecte).
> 573	              </p>
> 574	              <Button variant="outline" size="sm" onClick={conn.reconnect} className="gap-2">
> 575	                <RefreshCw className="h-4 w-4" /> Ativar métricas
> 576	              </Button>
> 577	            </CardContent>
> 578	          </Card>
> 579	        )}
> 580	      </div>
> 581	
> 582	      {conn.hasMonetaryScope && (
> 583	        <div className="space-y-2">
> 584	          <h2 className="text-sm font-medium text-muted-foreground">Receita (últimos 28 dias)</h2>
> 585	          <RevenueCard />
> 586	        </div>
> 587	      )}
> 588	
> 589	      <VideosTable canWrite={conn.hasWriteScope} />
> 590	    </div>
> 591	  );
> 592	}
> 593	
> ```

## 🤖 Claude *(02:10:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useYouTubeStudio.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { edgeErrorMessage } from '@/lib/edge';
> 4	import { useSocialAccounts } from '@/hooks/useSocialAccounts';
> 5	
> 6	// YouTube Studio panel — Fatia 1 (read-only). Business logic lives here (Harness Engineering); the page
> 7	// is display-only. All data comes from the `youtube-data` edge fn, which resolves the per-user OAuth
> 8	// token server-side. SSOT of the surface: docs/bok/youtube-studio/11-api-surface-map.md.
> 9	
> 10	const YT_READONLY = 'https://www.googleapis.com/auth/youtube.readonly';
> 11	const YT_ANALYTICS = 'https://www.googleapis.com/auth/yt-analytics.readonly';
> 12	const YT_ANALYTICS_MONETARY = 'https://www.googleapis.com/auth/yt-analytics-monetary.readonly';
> 13	const YT_FORCE_SSL = 'https://www.googleapis.com/auth/youtube.force-ssl';
> 14	
> 15	export interface YouTubeVideo {
> 16	  id: string;
> 17	  snippet?: {
> 18	    title?: string;
> 19	    description?: string;
> 20	    publishedAt?: string;
> 21	    channelTitle?: string;
> 22	    thumbnails?: Record<string, { url: string; width?: number; height?: number }>;
> 23	    tags?: string[];
> 24	    categoryId?: string;
> 25	    defaultLanguage?: string;
> 26	    defaultAudioLanguage?: string;
> 27	    liveBroadcastContent?: string;
> 28	  };
> 29	  contentDetails?: {
> 30	    duration?: string;
> 31	    definition?: string;
> 32	    dimension?: string;
> 33	    caption?: string;
> 34	    licensedContent?: boolean;
> 35	    projection?: string;
> 36	  };
> 37	  status?: {
> 38	    uploadStatus?: string;
> 39	    privacyStatus?: string;
> 40	    license?: string;
> 41	    embeddable?: boolean;
> 42	    publicStatsViewable?: boolean;
> 43	    madeForKids?: boolean;
> 44	    selfDeclaredMadeForKids?: boolean;
> 45	    publishAt?: string;
> 46	    containsSyntheticMedia?: boolean;
> 47	  };
> 48	  statistics?: {
> 49	    viewCount?: string;
> 50	    likeCount?: string;
> 51	    dislikeCount?: string;
> 52	    commentCount?: string;
> 53	    favoriteCount?: string;
> 54	  };
> 55	}
> 56	
> 57	export interface YouTubeChannel {
> 58	  id?: string;
> 59	  snippet?: {
> 60	    title?: string;
> 61	    description?: string;
> 62	    customUrl?: string;
> 63	    publishedAt?: string;
> 64	    thumbnails?: Record<string, { url: string }>;
> 65	    country?: string;
> 66	  };
> 67	  statistics?: {
> 68	    viewCount?: string;
> 69	    subscriberCount?: string;
> 70	    hiddenSubscriberCount?: boolean;
> 71	    videoCount?: string;
> 72	  };
> 73	  status?: { privacyStatus?: string; madeForKids?: boolean };
> 74	  brandingSettings?: { channel?: { keywords?: string; description?: string } };
> 75	}
> 76	
> 77	export interface MetricsReport {
> 78	  columnHeaders: { name: string; dataType?: string; columnType?: string }[];
> 79	  rows: (string | number)[][];
> 80	}
> 81	
> 82	type ListVideosPage = {
> 83	  videos: YouTubeVideo[];
> 84	  nextPageToken: string | null;
> 85	  uploadsPlaylistId: string | null;
> 86	};
> 87	
> 88	async function invokeYT<T>(action: string, payload: Record<string, unknown> = {}): Promise<T> {
> 89	  const { data, error } = await supabase.functions.invoke('youtube-data', {
> 90	    body: { action, ...payload },
> 91	  });
> 92	  if (error) {
> 93	    const msg = await edgeErrorMessage(error, 'Erro ao consultar a API do YouTube.');
> 94	    throw new Error(msg);
> 95	  }
> 96	  if (data?.error) {
> 97	    throw new Error(data.action ? `${data.error} — ${data.action}` : String(data.error));
> 98	  }
> 99	  return data as T;
> 100	}
> 101	
> 102	// Connection + scope state derived from the masked social_accounts view (no secret in the browser).
> 103	// The `scopes` array is the truthful gap signal: youtube.upload-only means the panel cannot read.
> 104	export function useYouTubeConnection() {
> 105	  const { accounts, initiateOAuth, isLoading } = useSocialAccounts();
> 106	  const account = accounts.find((a) => a.platform === 'youtube') ?? null;
> 107	  const scopes: string[] = (account?.scopes as string[] | null) ?? [];
> 108	  const isConnected = !!account;
> 109	  const hasReadScope = scopes.includes(YT_READONLY);
> 110	  // The monetary analytics scope is a superset — it also grants the non-monetary metrics.
> 111	  const hasMonetaryScope = scopes.includes(YT_ANALYTICS_MONETARY);
> 112	  const hasAnalyticsScope = scopes.includes(YT_ANALYTICS) || hasMonetaryScope;
> 113	  const hasWriteScope = scopes.includes(YT_FORCE_SSL);
> 114	  // Hard block ONLY when the panel cannot read at all (no youtube.readonly). Analytics is an optional
> 115	  // upgrade (yt-analytics.readonly): the video table renders without it — only the metrics card degrades
> 116	  // to a soft "ativar métricas" hint (see YouTubeStudioPage), so a readonly-only token is fully usable.
> 117	  const needsReconnect = isConnected && !hasReadScope;
> 118	
> 119	  return {
> 120	    account,
> 121	    isConnected,
> 122	    scopes,
> 123	    hasReadScope,
> 124	    hasAnalyticsScope,
> 125	    hasMonetaryScope,
> 126	    hasWriteScope,
> 127	    needsReconnect,
> 128	    isLoading,
> 129	    channelTitle: account?.platform_username ?? null,
> 130	    connect: () => initiateOAuth('youtube'),
> 131	    reconnect: () => initiateOAuth('youtube'),
> 132	  };
> 133	}
> 134	
> 135	export function useYouTubeChannel() {
> 136	  const conn = useYouTubeConnection();
> 137	  const query = useQuery({
> 138	    queryKey: ['youtube', 'channel', conn.account?.id],
> 139	    queryFn: () => invokeYT<{ channel: YouTubeChannel | null }>('channel_summary'),
> 140	    enabled: conn.isConnected && conn.hasReadScope,
> 141	    staleTime: 5 * 60 * 1000,
> 142	  });
> 143	  return { ...query, channel: query.data?.channel ?? null };
> 144	}
> 145	
> 146	export function useYouTubeVideos() {
> 147	  const conn = useYouTubeConnection();
> 148	  const query = useInfiniteQuery({
> 149	    queryKey: ['youtube', 'videos', conn.account?.id],
> 150	    queryFn: ({ pageParam }) =>
> 151	      invokeYT<ListVideosPage>('list_videos', { pageToken: pageParam || undefined }),
> 152	    initialPageParam: '',
> 153	    getNextPageParam: (last) => last.nextPageToken ?? undefined,
> 154	    enabled: conn.isConnected && conn.hasReadScope,
> 155	    staleTime: 2 * 60 * 1000,
> 156	  });
> 157	  const videos = (query.data?.pages ?? []).flatMap((p) => p.videos);
> 158	  return { ...query, videos };
> 159	}
> 160	
> 161	export function useYouTubeChannelMetrics(startDate?: string, endDate?: string) {
> 162	  const conn = useYouTubeConnection();
> 163	  return useQuery({
> 164	    queryKey: ['youtube', 'metrics', 'channel', conn.account?.id, startDate, endDate],
> 165	    queryFn: () => invokeYT<MetricsReport>('video_metrics', { startDate, endDate }),
> 166	    enabled: conn.isConnected && conn.hasAnalyticsScope,
> 167	    staleTime: 10 * 60 * 1000,
> 168	  });
> 169	}
> 170	
> 171	// Fatia 2 (Amendment 12) — revenue report. `monetized:false` is a valid, non-error state (channel not in YPP);
> 172	// the query still succeeds and demonstrates the yt-analytics-monetary.readonly scope.
> 173	export interface RevenueReport extends MetricsReport {
> 174	  monetized: boolean;
> 175	  reason?: string;
> 176	}
> 177	
> 178	export function useYouTubeRevenue(startDate?: string, endDate?: string) {
> 179	  const conn = useYouTubeConnection();
> 180	  return useQuery({
> 181	    queryKey: ['youtube', 'revenue', conn.account?.id, startDate, endDate],
> 182	    queryFn: () => invokeYT<RevenueReport>('revenue_metrics', { startDate, endDate }),
> 183	    enabled: conn.isConnected && conn.hasMonetaryScope,
> 184	    staleTime: 10 * 60 * 1000,
> 185	  });
> 186	}
> 187	
> 188	// Fatia 2 — force-ssl write ops on the user's OWN videos. Both invalidate the videos list on success.
> 189	export function useUpdateVideo() {
> 190	  const qc = useQueryClient();
> 191	  return useMutation({
> 192	    mutationFn: (input: { videoId: string; title?: string; description?: string; tags?: string[] }) =>
> 193	      invokeYT<{ updated: boolean }>('update_video', input),
> 194	    onSuccess: () => qc.invalidateQueries({ queryKey: ['youtube', 'videos'] }),
> 195	  });
> 196	}
> 197	
> 198	export function useDeleteVideo() {
> 199	  const qc = useQueryClient();
> 200	  return useMutation({
> 201	    mutationFn: (videoId: string) => invokeYT<{ deleted: boolean }>('delete_video', { videoId }),
> 202	    onSuccess: () => qc.invalidateQueries({ queryKey: ['youtube', 'videos'] }),
> 203	  });
> 204	}
> 205	
> ```

## 🤖 Claude *(02:10:33)*


## 🤖 Claude *(02:10:33)*

Now the edge function and the API surface map.

## 🤖 Claude *(02:10:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"case '\\|action ===\\|=== '\" supabase/functions/youtube-data/index.ts | head -60; echo \"--- LINES:\"; wc -l supabase/functions/youtube-data/index.ts",
  "description": "List actions in youtube-data edge fn"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 141:    if (action === "channel_summary" || action === "list_videos" || action === "video_categories") {
> 146:    if (action === "video_metrics" && !hasAnalytics) {
> 149:    if (action === "revenue_metrics" && !scopes.includes(SCOPE_ANALYTICS_MONETARY)) {
> 152:    if ((action === "update_video" || action === "delete_video") && !scopes.includes(SCOPE_FORCE_SSL)) {
> 198:    if (action === "channel_summary") {
> 226:    if (action === "video_categories") {
> 233:    if (action === "list_videos") {
> 264:    if (action === "video_metrics") {
> 283:    if (action === "revenue_metrics") {
> 307:    if (action === "update_video") {
> 333:    if (action === "delete_video") {
> --- LINES:
> 361 supabase/functions/youtube-data/index.ts
> ```

## 🤖 Claude *(02:10:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/youtube-studio/ && grep -n \"^#\\{1,3\\} \" docs/bok/youtube-studio/11-api-surface-map.md | head -50",
  "description": "List BoK docs and API map headings"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 00-deepsearch-blueprint.md
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> 11-api-surface-map.md
> 12-amendment-write-ops-and-monetary.md
> 13-amendment-upload-factory.md
> _apimap
> youtube-api-registry.json
> 1:# YouTube Studio — API Surface Map (11) · Console de Gestão de Canal
> 10:## §1 Matriz de Escopos OAuth
> 49:### §1.1 Fluxo OAuth (installed / desktop — verificado em `installed-apps`)
> 55:## §2 Recursos da Data API v3 — propriedades por recurso
> 59:### 2.1 `videos` — parts: `snippet · contentDetails · status · statistics · player · topicDetails · recordingDetails · fileDetails · processingDetails · suggestions · liveStreamingDetails · paidProductPlacementDetails · localizations` (fonte: [`videos.md`](./_apimap/videos.md))
> 112:### 2.2 `channels` — parts: `snippet · contentDetails · statistics · topicDetails · status · brandingSettings · auditDetails · contentOwnerDetails · localizations` (fonte: [`channels.md`](./_apimap/channels.md))
> 132:### 2.3 `playlists` — parts: `snippet · status · contentDetails · player · localizations · id` (fonte: [`playlists-playlistitems.md §1`](./_apimap/playlists-playlistitems.md))
> 146:### 2.4 `playlistItems` — parts: `snippet · contentDetails · status · id` (fonte: [`playlists-playlistitems.md §2`](./_apimap/playlists-playlistitems.md))
> 160:### 2.5 `search` (search result) — part: `snippet` (SOMENTE LEITURA — fonte: [`search.md`](./_apimap/search.md))
> 171:### 2.6 `commentThreads` + `comments` (fonte: [`comments.md`](./_apimap/comments.md))
> 194:### 2.7 `captions` — parts: `id · snippet` (fonte: [`captions.md`](./_apimap/captions.md))
> 208:### 2.8 `thumbnails` — sem GET próprio; só `set` (fonte: [`thumbnails-categories-sections-watermarks.md §1`](./_apimap/thumbnails-categories-sections-watermarks.md))
> 212:### 2.9 `videoCategories` — part: `snippet` (SOMENTE LEITURA — fonte: [`…watermarks.md §2`](./_apimap/thumbnails-categories-sections-watermarks.md))
> 219:### 2.10 `channelSections` — parts: `id · snippet · contentDetails` (fonte: [`…watermarks.md §3`](./_apimap/thumbnails-categories-sections-watermarks.md))
> 232:### 2.11 `subscriptions` — parts: `snippet · contentDetails · id · subscriberSnippet` (SÓ `list`/`insert`/`delete`; propriedades read-only — fonte: [`subscriptions-activities-i18n.md §1`](./_apimap/subscriptions-activities-i18n.md))
> 242:### 2.12 `activities` — parts: `snippet · contentDetails · id` (SOMENTE LEITURA — `insert` obsoleto; fonte: [`subscriptions-activities-i18n.md §2`](./_apimap/subscriptions-activities-i18n.md))
> 253:### 2.13 (contexto) `i18nLanguages` / `i18nRegions` — públicos, populam seletores `hl`/`gl`
> 259:## §3 Catálogo YouTube Analytics API v2 (`reports.query`)
> 263:### §3.1 Métricas (52 · monetárias-de-valor = 6, + 2 contagens em relatórios de escopo monetário)
> 282:### §3.2 Dimensões (32 · 9 Core)
> 303:### §3.3 Tipos de relatório de canal (44 — 32 vídeo + 12 playlist)
> 327:## §4 Registro de AÇÕES (write / destrutivo) — escopo · quota · TIER de risco
> 371:## §5 Custos de quota
> 388:### §5.1 Orçamento de LEITURA do painel (Fatia 1)
> 401:## §6 Declaração de Conformidade de Padrões (Pattern Conformance)
> 433:## §7 Plano de Fatias (gate de materialidade cada)
> 437:### Fatia 1 — Tabela CRUD read-only de vídeos + TODAS as métricas · **"o primeiro de tudo"**
> 444:### Fatia 2 — Ações de escrita segura (metadados / thumbnail / playlist) · TIER BAIXO+MÉDIO
> 451:### Fatia 3 — Ações destrutivas com confirmação dupla + dry-run · TIER ALTO
> 460:## §8 Fontes (rodapé de materialidade — Lei 1)
> ```

## 🤖 Claude *(02:10:38)*


## 🤖 Claude *(02:10:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n 255,310p supabase/functions/youtube-data/index.ts",
  "description": "Read video_metrics and revenue_metrics handlers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>           `${YT_DATA}/videos?part=snippet,contentDetails,status,statistics&id=${ids.join(",")}&maxResults=50`,
>         );
>         if (!vids.ok) return googleError(vids, pulse);
>         videos = vids.data.items ?? [];
>       }
>       pulse("healthy");
>       return json({ videos, nextPageToken: items.data.nextPageToken ?? null, uploadsPlaylistId: uploads });
>     }
> 
>     if (action === "video_metrics") {
>       const endDate = typeof body.endDate === "string" ? body.endDate : isoDate(1);
>       const startDate = typeof body.startDate === "string" ? body.startDate : isoDate(28);
>       const metrics =
>         typeof body.metrics === "string" && body.metrics.trim()
>           ? body.metrics
>           : "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost";
>       const params = new URLSearchParams({ ids: "channel==MINE", startDate, endDate, metrics });
>       if (typeof body.dimensions === "string" && body.dimensions) params.set("dimensions", body.dimensions);
>       if (typeof body.videoId === "string" && body.videoId) params.set("filters", `video==${body.videoId}`);
>       if (typeof body.sort === "string" && body.sort) params.set("sort", body.sort);
>       if (typeof body.maxResults === "number") params.set("maxResults", String(body.maxResults));
>       const r = await gfetch(`${YT_ANALYTICS}/reports?${params.toString()}`);
>       if (!r.ok) return googleError(r, pulse);
>       pulse("healthy");
>       return json({ columnHeaders: r.data.columnHeaders ?? [], rows: r.data.rows ?? [] });
>     }
> 
>     // ── Fatia 2 — monetary reports (force: yt-analytics-monetary.readonly) ──
>     if (action === "revenue_metrics") {
>       const endDate = typeof body.endDate === "string" ? body.endDate : isoDate(1);
>       const startDate = typeof body.startDate === "string" ? body.startDate : isoDate(28);
>       const metrics =
>         typeof body.metrics === "string" && body.metrics.trim()
>           ? body.metrics
>           : "estimatedRevenue,estimatedAdRevenue,grossRevenue,cpm,monetizedPlaybacks,adImpressions";
>       const params = new URLSearchParams({ ids: "channel==MINE", startDate, endDate, metrics, currency: "USD" });
>       const r = await gfetch(`${YT_ANALYTICS}/reports?${params.toString()}`);
>       if (!r.ok) {
>         // A non-partner / non-monetized channel returns 403 for monetary metrics. That is NOT an app failure —
>         // the CALL itself demonstrates the scope. Return a clean, monetized:false state (never a crash).
>         if (r.status === 403) {
>           pulse("healthy");
>           const reason = r.data?.error?.errors?.[0]?.reason ?? r.data?.error?.status ?? "not_monetized";
>           return json({ columnHeaders: [], rows: [], monetized: false, reason });
>         }
>         return googleError(r, pulse);
>       }
>       pulse("healthy");
>       return json({ columnHeaders: r.data.columnHeaders ?? [], rows: r.data.rows ?? [], monetized: true });
>     }
> 
>     // ── Fatia 2 — edit the user's own video (force: youtube.force-ssl) ──
>     if (action === "update_video") {
>       const videoId = typeof body.videoId === "string" ? body.videoId : "";
>       if (!videoId) return json({ error: "videoId required" }, 400);
>       // videos.update REPLACES the sent part; snippet.categoryId is REQUIRED. Read the current snippet first,
> ```

## 🤖 Claude *(02:10:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n 259,330p docs/bok/youtube-studio/11-api-surface-map.md",
  "description": "Read analytics metrics catalog section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ## §3 Catálogo YouTube Analytics API v2 (`reports.query`)
> 
> > Fonte: [`analytics-metrics.md`](./_apimap/analytics-metrics.md) + [`analytics-dimensions-reports.md`](./_apimap/analytics-dimensions-reports.md). Base host `https://youtubeanalytics.googleapis.com/v2`. `reports.query` (GET `/reports`) parâmetros: `ids` (`channel==MINE`), `startDate`, `endDate`, `metrics` (obrig.) + `dimensions`/`filters`/`sort`/`maxResults`/`currency`/`startIndex`/`includeHistoricalChannelData` (opc.).
> 
> ### §3.1 Métricas (52 · monetárias-de-valor = 6, + 2 contagens em relatórios de escopo monetário)
> 
> **Core (14 — sob Deprecation Policy):** `annotationClickThroughRate`, `annotationCloseRate`, `averageViewDuration`, `comments`, `dislikes`, `engagedViews`, `estimatedMinutesWatched`, `estimatedRevenue`✱, `likes`, `shares`, `subscribersGained`, `subscribersLost`, `viewerPercentage`, `views`.
> 
> | Grupo | Métricas | Escopo |
> |---|---|---|
> | **Views/Watch-time** | `views`, `engagedViews`, `redViews`, `viewerPercentage`, `estimatedMinutesWatched`, `estimatedRedMinutesWatched`, `averageViewDuration`, `averageViewPercentage` | `yt-analytics.readonly` |
> | **Engajamento** | `comments`, `likes`, `dislikes`, `shares`, `subscribersGained`, `subscribersLost`, `videosAddedToPlaylists`, `videosRemovedFromPlaylists` | `yt-analytics.readonly` |
> | **Anotações (7)** | `annotationImpressions`, `annotationClickableImpressions`, `annotationClicks`, `annotationClickThroughRate`, `annotationClosableImpressions`, `annotationCloses`, `annotationCloseRate` | `yt-analytics.readonly` |
> | **Cards (6)** | `cardImpressions`, `cardClicks`, `cardClickRate`, `cardTeaserImpressions`, `cardTeaserClicks`, `cardTeaserClickRate` | `yt-analytics.readonly` |
> | **Playlist (7)** | `playlistViews`, `playlistStarts`, `playlistSaves`, `averageTimeInPlaylist`, `playlistAverageViewDuration`, `playlistEstimatedMinutesWatched`, `viewsPerPlaylistStart` | `yt-analytics.readonly` |
> | **Retenção (5)** | `audienceWatchRatio`, `relativeRetentionPerformance`, `startedWatching`, `stoppedWatching`, `totalSegmentImpressions` | `yt-analytics.readonly` |
> | **Livestream (2)** | `averageConcurrentViewers`, `peakConcurrentViewers` | `yt-analytics.readonly` |
> | **Membership (1)** | `membershipsCancellationSurveyResponses` | `yt-analytics.readonly` |
> | **Receita estimada — MONETÁRIA** | `estimatedRevenue`✱, `estimatedAdRevenue`✱, `estimatedRedPartnerRevenue`✱ | `yt-analytics-monetary.readonly` |
> | **Ad performance — MONETÁRIA** | `grossRevenue`✱, `cpm`✱, `playbackBasedCpm`✱, `adImpressions`, `monetizedPlaybacks` | `yt-analytics-monetary.readonly` |
> 
> > ✱ = valor monetário (aceita `currency`, default USD). **⚠️ Channel reports NÃO suportam receita/ad performance** — a doc oficial de `channel_reports` diz "*Estimated revenue and ad performance metrics are not currently supported for channel reports*". As monetárias só vêm de **content-owner reports**. Um dashboard de canal (views→retenção→tráfego→demografia) é 100% coberto por `yt-analytics.readonly`.
> 
> ### §3.2 Dimensões (32 · 9 Core)
> 
> **Core (9):** `ageGroup`, `channel`, `country`, `day`, `gender`, `month`, `sharingService`, `uploaderType`, `video`.
> 
> | Categoria | Dimensões |
> |---|---|
> | **Recursos** | `video`, `playlist`, `channel`, `group`(filter-only) |
> | **Tempo** | `day`, `month` |
> | **Geografia** | `country`, `province`(exige `country==US`), `dma`, `city`(desde 2022-01-01), `continent`(filter), `subContinent`(filter) |
> | **Playback location** | `insightPlaybackLocationType` (BROWSE/CHANNEL/EMBEDDED/EXTERNAL_APP/MOBILE/SEARCH/WATCH/YT_OTHER), `insightPlaybackLocationDetail` |
> | **Playback details** | `creatorContentType` (LIVE_STREAM/SHORTS/STORY/VIDEO_ON_DEMAND/UNSPECIFIED), `liveOrOnDemand`, `subscribedStatus`, `youtubeProduct` (CORE/GAMING/KIDS/MUSIC/UNKNOWN) |
> | **Traffic source** | `insightTrafficSourceType` (ADVERTISING/END_SCREEN/EXT_URL/NOTIFICATION/PLAYLIST/RELATED_VIDEO/SHORTS/SUBSCRIBER/YT_SEARCH/…), `insightTrafficSourceDetail` |
> | **Device/OS** | `deviceType` (DESKTOP/GAME_CONSOLE/MOBILE/TABLET/TV/AUTOMOTIVE/WEARABLE/UNKNOWN_PLATFORM), `operatingSystem` (25 valores) |
> | **Demografia** | `ageGroup` (age13-17…age65-), `gender` (female/male/user_specified) |
> | **Sharing** | `sharingService` (70+ plataformas) |
> | **Retenção** | `elapsedVideoTimeRatio` (0.01–1.0), `audienceType`(filter: ORGANIC/AD_INSTREAM/AD_INDISPLAY) |
> | **Live streaming** | `livestreamPosition` |
> | **Membership** | `membershipsCancellationSurveyReason` |
> | **Ad performance** | `adType` (auctionInstream/reservedBumperInstream/…) |
> | **Content owner** | `claimedStatus`(filter: `claimed`), `uploaderType` (self/thirdParty) |
> 
> ### §3.3 Tipos de relatório de canal (44 — 32 vídeo + 12 playlist)
> 
> Todos read-only via `yt-analytics.readonly`. Fonte: [`analytics-dimensions-reports.md §5`](./_apimap/analytics-dimensions-reports.md).
> 
> | Família | Relatórios | Dimensão-chave × métricas-chave |
> |---|---|---|
> | **Basic user activity** | #1, #2(US states) | (nenhuma dim) × views, likes, comments, shares, subscribers, watch-time, annotation*, card* |
> | **Time-based** | #3, #4 | `day`/`month` × conjunto completo + `uniques` |
> | **Geography** | #5, #6, #7(city ≤250), #8(dma) | `country`/`province`/`city`/`dma` × views, watch-time, avgViewDuration |
> | **Playback details** | #9–#16 | `subscribedStatus`/`liveOrOnDemand`/`youtubeProduct` × redViews, watch-time, avgViewPercentage |
> | **Playback location** | #17, #18(detail ≤25) | `insightPlaybackLocationType/Detail` × engagedViews, views, minutes |
> | **Traffic source** | #19, #20(detail ≤25) | `insightTrafficSourceType/Detail` × engagedViews, views, minutes |
> | **Device/OS** | #21, #22, #23 | `deviceType`+`operatingSystem` × engagedViews, views, minutes |
> | **Demographics** | #24 | `ageGroup`+`gender` × `viewerPercentage` |
> | **Engagement/sharing** | #25 | `sharingService` × `shares` |
> | **Audience retention** | #26 | `elapsedVideoTimeRatio` × audienceWatchRatio, relativeRetentionPerformance, started/stoppedWatching |
> | **Concurrent viewers** | #27 | `livestreamPosition` × average/peakConcurrentViewers |
> | **Top videos** | #28–#32 (≤200) | `video` × conjunto completo (sort obrigatório) |
> | **Playlist** | #33–#44 | `day`/`country`/`deviceType`/`ageGroup` × playlistViews, playlistStarts, viewsPerPlaylistStart, averageTimeInPlaylist |
> 
> > **Quota Analytics:** as docs oficiais NÃO declaram custo-por-unidade para a Analytics v2 — é limite de requisições/dia no Cloud Console, não custo-por-método `(não verificado)`.
> 
> ---
> 
> ## §4 Registro de AÇÕES (write / destrutivo) — escopo · quota · TIER de risco
> 
> > **TIER:** `BAIXO` = editar metadados/thumbnail (reversível via re-edit) · `MÉDIO` = playlist/comentário/subscription/seção/watermark/grupo (reversível) · `ALTO` = delete/irreversível. Fonte de custos: [`scopes-quota.md §2`](./_apimap/scopes-quota.md) + method-pages.
> ```

## 🤖 Claude *(02:10:45)*


## 🤖 Claude *(02:10:46)*

Key finding on monetary reports. Now the AI layer and nav.

## 🤖 Claude *(02:10:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"useConfiguredProviders\" src/hooks/ src/components/ --include=*.ts --include=*.tsx -l | head; echo \"---SIDEBAR:\"; grep -n \"youtube\\|YouTube\\|Marketing\\|Spaces\" src/components/dashboard/DashboardSidebar.tsx | head -20",
  "description": "Find provider hook and sidebar entries"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/hooks/useConfiguredProviders.ts
> src/components/canvas/RightPanel/inspectors/ImageToVideoInspector.tsx
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx
> ---SIDEBAR:
> 91:    // Marketing — content creation, campaigns, and distribution.
> 92:    title: 'Marketing',
> 97:      { title: 'YouTube Studio', url: '/dashboard/youtube/studio-yt', icon: MonitorPlay },
> 192:    { title: 'Spaces', url: '/dashboard/spaces', icon: Palette },
> 341:                  {/* Spaces (ex-Canvas Studio, Amendment 14) — collapsible with Studio/Design/Video/Assets sub-items */}
> 353:                            <span>Spaces</span>
> ```

## 🤖 Claude *(02:10:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls supabase/functions | wc -l; ls supabase/functions | grep -i \"intent\\|generate-content\\|swarm\\|youtube\"",
  "description": "Count edge fns and list AI ones"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 100
> generate-content
> intent-execute
> intent-orchestrate
> openrouter-swarm
> youtube-data
> ```

## 🤖 Claude *(02:10:53)*


## 🤖 Claude *(02:10:53)*

Edge fn count is at 100 — the cap is fully hit. Let me verify and check the AI interfaces.

## 🤖 Claude *(02:10:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls supabase/functions | grep -v \"^_\" | wc -l; echo \"--- generate-content body:\"; grep -n \"body\\.\\|const {\" supabase/functions/generate-content/index.ts | head -25",
  "description": "Verify fn count and generate-content contract"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 99
> --- generate-content body:
> 29:    const { data: { user }, error: authError } = await supabase.auth.getUser();
> 36:    const { type, prompt, platform, tone, language = "pt-BR" } = await req.json();
> 54:    const { data: userKeys } = await adminClient.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> ```

## 🤖 Claude *(02:10:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n 1,40p src/hooks/useConfiguredProviders.ts; echo \"=== SPACES NAV PATTERN ===\"; sed -n 335,375p src/components/dashboard/DashboardSidebar.tsx",
  "description": "Read provider hook and Spaces nav pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> import { useMemo } from "react";
> import { useUserApiKeys } from "@/hooks/useUserApiKeys";
> 
> /**
>  * Regra perene (Diretiva Sovereign 2026-07-10): "Só carrega para o usuário, opções disponíveis."
>  *
>  * Provider selectors across the app must populate ONLY from the keys the user actually configured
>  * (BYOK per-user) — never show a provider whose key is absent. Availability derives 100% client-side
>  * from the masked `user_api_keys` VIEW: a configured key reads as the literal '••••••••••••' (truthy),
>  * an absent one as NULL (falsy). No secret ever reaches the browser (values live in the Vault;
>  * `decrypted_user_api_keys` is service-role-only). Precedents: ConfigPanel `connected = !!userKeys[k]`,
>  * GenerateImageInspector `*KeyMissing`.
>  *
>  * Keyless engines (self-host, e.g. voice 'qwen3-local') are ALWAYS available — declare them in the
>  * surface itself, not here.
>  */
> const PROVIDER_KEY_MAP = {
>   elevenlabs: "elevenlabs_api_key",
>   cartesia: "cartesia_api_key",
>   openai: "openai_api_key",
>   openrouter: "openrouter_api_key",
>   google: "google_api_key",
>   groq: "groq_api_key",
>   replicate: "replicate_api_key",
>   higgsfield: "higgsfield_api_key",
>   hedra: "hedra_api_key",
>   fal: "fal_api_key",
>   resend: "resend_api_key",
>   firecrawl: "firecrawl_api_key",
>   apify: "apify_token",
>   rapidapi: "rapidapi_key",
> } as const;
> 
> export type ConfigurableProvider = keyof typeof PROVIDER_KEY_MAP;
> 
> export function useConfiguredProviders(): {
>   configured: Record<ConfigurableProvider, boolean>;
>   isLoading: boolean;
> } {
>   const { userKeys, isLoading } = useUserApiKeys();
> === SPACES NAV PATTERN ===
>                           </SidebarMenuSubItem>
>                         </SidebarMenuSub>
>                       </CollapsibleContent>
>                     </SidebarMenuItem>
>                   </Collapsible>
> 
>                   {/* Spaces (ex-Canvas Studio, Amendment 14) — collapsible with Studio/Design/Video/Assets sub-items */}
>                   <Collapsible defaultOpen={isCanvasActive} className="group/collapsible">
>                     <SidebarMenuItem>
>                       <div className="flex items-center">
>                         <SidebarMenuButton asChild className="flex-1">
>                           <NavLink
>                             to="/dashboard/spaces"
>                             end
>                             className="hover:bg-muted/50"
>                             activeClassName="bg-primary/10 text-primary font-medium"
>                           >
>                             <Palette className="mr-2 h-4 w-4 shrink-0" />
>                             <span>Spaces</span>
>                           </NavLink>
>                         </SidebarMenuButton>
>                         <CollapsibleTrigger asChild>
>                           <Button
>                             variant="ghost"
>                             size="icon"
>                             className="h-6 w-6 ml-auto shrink-0 [&[data-state=open]>svg]:rotate-180"
>                           >
>                             <ChevronDown className="h-3.5 w-3.5 transition-transform duration-200" />
>                           </Button>
>                         </CollapsibleTrigger>
>                       </div>
>                       <CollapsibleContent>
>                         <SidebarMenuSub>
>                           <SidebarMenuSubItem>
>                             <SidebarMenuSubButton asChild>
>                               <NavLink
>                                 to="/dashboard/spaces"
>                                 end
>                                 className="hover:bg-muted/50"
>                                 activeClassName="text-primary font-medium"
>                               >
> ```

## 🤖 Claude *(02:11:00)*


## 🤖 Claude *(02:11:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls src/components/ui/ | grep -E \"tabs|sheet|chart|tooltip|breadcrumb|scroll\"; echo \"--- existing per-id routes pattern:\"; grep -n \":id\\|:slug\\|:videoId\" src/App.tsx | head",
  "description": "Check available UI primitives and dynamic route patterns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> breadcrumb.tsx
> chart.tsx
> scroll-area.tsx
> sheet.tsx
> tabs.tsx
> tooltip.tsx
> --- existing per-id routes pattern:
> 67:// FR-SPACES-022 (Amendment 14): legacy /dashboard/canvas/:id deep-links redirect 1:1 to /dashboard/spaces/:id.
> 131:                <Route path="campaigns/:id" element={<CampaignDetail />} />
> 134:                <Route path="content/video-editor/:id" element={<VideoEditorPage />} />
> 162:                <Route path="spaces/:id" element={<CanvasEditorPage />} />
> 168:                <Route path="canvas/:id" element={<LegacyCanvasProjectRedirect />} />
> ```

## 🤖 Claude *(02:11:49)*


## 🤖 Claude *(02:11:49)*

I have everything I need. Composing the spec.

## 🤖 Claude *(02:13:58)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "title": "YouTube Studio Hub \u2014 Arquitetura de Informa\u00e7\u00e3o e UX (rota-hub + p\u00e1gina por-v\u00eddeo)",
  "summary": "A rota-hub J\u00c1 EXISTE e est\u00e1 correta: `src/App.tsx:139-140` redireciona `/dashboard/youtube` \u2192 `/dashboard/youtube/studio-yt`, e `src/components/dashboard/DashboardSidebar.tsx:97` j\u00e1 aponta pra l\u00e1. O que falta \u00e9 (a) quebrar as 592 linhas de `src/pages/YouTubeStudioPage.tsx` \u2014 hoje um scroll vertical \u00fanico de header+stats+upload+m\u00e9tricas+receita+tabela-de-16-colunas \u2014 em um hub COM ABAS; (b) criar a rota `/dashboard/youtube/studio-yt/video/:videoId`; (c) tornar a tabela naveg\u00e1vel em vez de terminal (hoje o t\u00edtulo do v\u00eddeo \u00e9 um `<a>` que JOGA O USU\u00c1RIO PARA FORA, em `YouTubeStudioPage.tsx:271-278` \u2014 o \u00fanico clique dispon\u00edvel leva embora do produto).\n\nACHADO ARQUITETURAL DECISIVO (zero custo de slot): a action `video_metrics` do `supabase/functions/youtube-data/index.ts:264-279` J\u00c1 \u00e9 um passthrough parametrizado \u2014 ela repassa `metrics`, `dimensions`, `filters (video==)`, `sort` e `maxResults` do body direto pro `reports.query`. Isso significa que as QUATRO abas anal\u00edticas da p\u00e1gina por-v\u00eddeo (Desempenho/dia \u00b7 Reten\u00e7\u00e3o/elapsedVideoTimeRatio \u00b7 Origem do tr\u00e1fego/insightTrafficSourceType \u00b7 Audi\u00eancia/ageGroup+gender+country+deviceType) s\u00e3o a MESMA action com `dimensions` diferentes. Nenhuma edge function nova. Isso \u00e9 vital porque `ls supabase/functions | grep -v ^_ | wc -l` retorna **99** \u2014 resta exatamente 1 slot no cap de 100, e ele n\u00e3o deve ser gasto aqui.\n\nACHADO DE HONESTIDADE (Lei 1) que muda a IA: `docs/bok/youtube-studio/11-api-surface-map.md:280` cita a doc oficial \u2014 \"Estimated revenue and ad performance metrics are not currently supported for channel reports\". Como `revenue_metrics` chama com `ids=channel==MINE` (`index.ts:290`), o 403 \u00e9 ESTRUTURAL, n\u00e3o sinal de canal n\u00e3o-monetizado. Mas `YouTubeStudioPage.tsx:166-167` traduz esse 403 como \"o canal n\u00e3o est\u00e1 monetizado (fora do YouTube Partner Program)\". Isso \u00e9 uma afirma\u00e7\u00e3o FALSA sobre o neg\u00f3cio do usu\u00e1rio derivada de uma limita\u00e7\u00e3o da API. Consequ\u00eancia de IA: **n\u00e3o existe aba de receita por-v\u00eddeo** e o card de receita do hub precisa dizer a verdade da API.",
  "decisions": [
    "ROTAS \u2014 manter `/dashboard/youtube` \u2192 Navigate para `/dashboard/youtube/studio-yt` (App.tsx:139, j\u00e1 feito); manter o hub em `studio-yt` (App.tsx:140); ADICIONAR `<Route path=\"youtube/studio-yt/video/:videoId\" element={<YouTubeVideoDetailPage />} />` com lazy import no bloco de App.tsx:30. O padr\u00e3o `:id` j\u00e1 \u00e9 usado em App.tsx:131/134/162 \u2014 nada de novo a inventar.",
    "HUB COM ABAS \u2014 `src/components/ui/tabs.tsx` j\u00e1 existe. Reescrever o return de YouTubeStudioPage.tsx:524-591 (hoje empilhamento vertical) em 4 abas: (1) **Vis\u00e3o geral** = os stat-tiles do canal (linhas 528-559) + `<ChannelMetrics/>` 28d; (2) **V\u00eddeos** = `<VideosTable/>`, a aba DEFAULT porque \u00e9 a superf\u00edcie de navega\u00e7\u00e3o; (3) **Publicar** = `<YouTubeUploadPanel/>`; (4) **Receita** = `<RevenueCard/>`, renderizada s\u00f3 com `conn.hasMonetaryScope`. O header (linhas 436-460) e os tr\u00eas guardas de conex\u00e3o (462-520) ficam FORA das abas \u2014 s\u00e3o estado da p\u00e1gina inteira.",
    "ONDE MORA O UPLOAD \u2014 hoje `<YouTubeUploadPanel/>` est\u00e1 cravado no meio do scroll (YouTubeStudioPage.tsx:561), entre os stats e as m\u00e9tricas: ocupa o espa\u00e7o nobre com um formul\u00e1rio que o usu\u00e1rio usa uma vez por dia. Mover para a aba **Publicar** + um bot\u00e3o prim\u00e1rio 'Publicar v\u00eddeo' no header que ativa essa aba. CR\u00cdTICO: como o job de upload \u00e9 longo e o store vive em `src/hooks/useYouTubeUpload.ts`, o estado sobrevive \u00e0 troca de aba \u2014 ent\u00e3o adicionar um **pill de progresso persistente no header** (vis\u00edvel em QUALQUER aba) quando h\u00e1 job ativo, clic\u00e1vel para voltar \u00e0 aba Publicar. Sem isso, trocar de aba durante um upload parece ter cancelado o upload.",
    "TABELA VIRA NAVEGA\u00c7\u00c3O, N\u00c3O DUMP \u2014 a tabela tem 16 colunas (`COLUMNS`, YouTubeStudioPage.tsx:247-250) + coluna de a\u00e7\u00f5es; isso \u00e9 um dump de API, n\u00e3o uma lista escane\u00e1vel. Demover para 7 colunas na lista (V\u00eddeo \u00b7 Publicado \u00b7 Privacidade \u00b7 Dura\u00e7\u00e3o \u00b7 Views \u00b7 Likes \u00b7 Coment.) e mandar as outras 9 (Upload, Def, Tags, Cat., Kids, Licen\u00e7a, Embed, Sint\u00e9tico, ID) para a aba **Ficha t\u00e9cnica** da p\u00e1gina por-v\u00eddeo, onde elas s\u00e3o contexto e n\u00e3o ru\u00eddo.",
    "CLIQUE \u2014 em `VideoRow` (YouTubeStudioPage.tsx:252-320): o t\u00edtulo deixa de ser `<a href=\"https://youtube.com/watch?v=...\">` (linha 272) e vira `<Link to={`/dashboard/youtube/studio-yt/video/${v.id}`}>`. O link externo pro YouTube N\u00c3O some \u2014 vira um \u00edcone `ExternalLink` discreto na coluna de a\u00e7\u00f5es. A `<TableRow>` inteira ganha `cursor-pointer` + `onClick` de navega\u00e7\u00e3o; a c\u00e9lula de a\u00e7\u00f5es (linhas 301-317) ganha `onClick={(e) => e.stopPropagation()}` sen\u00e3o clicar em Excluir tamb\u00e9m navega. A11y: a linha ganha `role=\"link\"` + `tabIndex={0}` + handler de Enter, porque `<tr onClick>` sozinho \u00e9 inacess\u00edvel por teclado.",
    "P\u00c1GINA POR-V\u00cdDEO \u2014 6 abas. **Desempenho** (`dimensions=day`, s\u00e9rie temporal com `src/components/ui/chart.tsx` + tiles de total); **Reten\u00e7\u00e3o** (`dimensions=elapsedVideoTimeRatio`, metrics `audienceWatchRatio,relativeRetentionPerformance` \u2014 relat\u00f3rio #26 do map \u00a73.3); **Origem do tr\u00e1fego** (`dimensions=insightTrafficSourceType`, e drill `insightTrafficSourceDetail` limitado a 25 \u2014 esta \u00e9 a \u00daNICA superf\u00edcie atributiva correta Short\u2192longo, conforme gap #3, e substitui qualquer subtra\u00e7\u00e3o de views); **Audi\u00eancia** (`ageGroup+gender` \u00d7 `viewerPercentage`, `country` \u00d7 views, `deviceType`/`operatingSystem`, `subscribedStatus`); **Ficha t\u00e9cnica** (as 9 props demovidas + tags + categoria resolvida pela action `video_categories` que j\u00e1 existe em index.ts:226 + reuso do `EditVideoDialog` e do `AlertDialog` de exclus\u00e3o, gated por `conn.hasWriteScope`); **An\u00e1lise IA**.",
    "HEADER DA P\u00c1GINA POR-V\u00cdDEO \u2014 thumbnail `medium`, t\u00edtulo, `publishedAt`, badge de privacidade reusando o helper `privacyBadge` (YouTubeStudioPage.tsx:80-87), link externo, e `src/components/ui/breadcrumb.tsx` (YouTube Studio \u203a V\u00eddeos \u203a <t\u00edtulo>). Seletor de per\u00edodo (7d/28d/90d/customizado) no header, controlando TODAS as abas anal\u00edticas de uma vez \u2014 n\u00e3o um seletor por aba. Os hooks j\u00e1 aceitam `startDate/endDate` (useYouTubeStudio.ts:161).",
    "SELETOR DE PER\u00cdODO \u00c9 ESTADO DE URL \u2014 `?range=28d` via `useSearchParams`, n\u00e3o `useState`. Assim o link de uma an\u00e1lise \u00e9 compartilh\u00e1vel e o back do browser funciona. Idem a aba ativa (`?tab=trafego`).",
    "EXTRA\u00c7\u00c3O DE COMPONENTES \u2014 YouTubeStudioPage.tsx com 592 linhas j\u00e1 viola o padr\u00e3o display-only. Mover `ChannelMetrics` (90-136), `RevenueCard` (139-193), `EditVideoDialog` (196-244), `VideoRow`+`VideosTable` (252-429) para `src/components/youtube/`, ao lado do `YouTubeUploadPanel.tsx` que j\u00e1 mora l\u00e1. Os helpers de formata\u00e7\u00e3o (47-87) viram `src/lib/youtube-format.ts` \u2014 a p\u00e1gina por-v\u00eddeo precisa dos mesmos `formatNumber`/`formatDuration`/`formatSeconds`/`privacyBadge` e duplic\u00e1-los \u00e9 como as duas telas divergem.",
    "SHORTS S\u00c3O UM ESTADO DE PRIMEIRA CLASSE, N\u00c3O UMA NOTA DE RODAP\u00c9 \u2014 usar a dimens\u00e3o `creatorContentType` (map \u00a73.2) para carimbar um badge SHORTS no header da p\u00e1gina por-v\u00eddeo. Quando SHORTS, o tile de Dura\u00e7\u00e3o m\u00e9dia carrega tooltip obrigat\u00f3rio explicando que desde 31/03/2025 'view' \u00e9 play-start e que o denominador da AVD \u00e9 engaged views. E a UI NUNCA calcula watch-time\u00f7views no cliente \u2014 s\u00f3 exibe `averageViewDuration` como a API devolveu.",
    "MIV \u2014 respeitar o que a p\u00e1gina j\u00e1 usa e o que a mem\u00f3ria de tokens manda: cyan (`text-cyan-400`/`cyan-300`) como accent de m\u00e9trica; amber (`border-amber-500/30 bg-amber-500/5`, padr\u00e3o das linhas 104/153/351/499) exclusivamente para estados degradados; emerald s\u00f3 onde h\u00e1 dinheiro real (linha 185); `bg-red-600/15 text-red-400` (linha 439) s\u00f3 na marca YouTube do header. S\u00e9ries de gr\u00e1fico puxam `--accent`. Sem gold e sem nebula aqui \u2014 n\u00e3o \u00e9 valor financeiro nem mem\u00f3ria."
  ],
  "api_surfaces": [
    "`youtube-data` action `video_metrics` + `videoId` \u2014 J\u00c1 implementada (index.ts:264-279, `filters=video==${videoId}`). Base de TODAS as abas anal\u00edticas por-v\u00eddeo.",
    "`video_metrics` + `dimensions=day` \u2014 s\u00e9rie temporal da aba Desempenho. M\u00e9tricas: `views,engagedViews,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost`.",
    "`video_metrics` + `dimensions=elapsedVideoTimeRatio` & `metrics=audienceWatchRatio,relativeRetentionPerformance,startedWatching,stoppedWatching` \u2014 aba Reten\u00e7\u00e3o (relat\u00f3rio #26, map \u00a73.3).",
    "`video_metrics` + `dimensions=insightTrafficSourceType` & `metrics=views,engagedViews,estimatedMinutesWatched` \u2014 aba Origem do tr\u00e1fego (relat\u00f3rio #19). Drill: `dimensions=insightTrafficSourceDetail` + `sort=-views` + `maxResults=25` (teto duro da API, relat\u00f3rio #20).",
    "`video_metrics` + `dimensions=ageGroup,gender` & `metrics=viewerPercentage` \u2014 demografia (relat\u00f3rio #24). S\u00f3 `viewerPercentage` \u00e9 suportada aqui; pedir `views` junto retorna erro.",
    "`video_metrics` + `dimensions=country` / `deviceType` / `operatingSystem` / `subscribedStatus` \u2014 os quatro blocos restantes da aba Audi\u00eancia (relat\u00f3rios #5, #21-23, #9-16).",
    "`video_metrics` + `dimensions=creatorContentType` \u2014 detecta SHORTS vs VIDEO_ON_DEMAND vs LIVE_STREAM para o badge e para o disclaimer de AVD.",
    "`channel_summary` (index.ts:198) e `list_videos` (index.ts:233) \u2014 inalteradas, alimentam hub e lista.",
    "`video_categories` (index.ts:226) \u2014 resolve `snippet.categoryId` (hoje exibido cru como n\u00famero na coluna 'Cat.', YouTubeStudioPage.tsx:295) para nome leg\u00edvel na Ficha t\u00e9cnica.",
    "`update_video` (index.ts:307) e `delete_video` (index.ts:333) \u2014 reusadas na Ficha t\u00e9cnica, gated por `hasWriteScope`.",
    "`revenue_metrics` (index.ts:283) \u2014 permanece S\u00d3 no hub. N\u00c3O existe equivalente por-v\u00eddeo: o map \u00a73.1 registra que channel reports n\u00e3o suportam m\u00e9tricas de receita/ad performance.",
    "`generate-content` (body `{type, prompt, platform, tone, language}`, resolve BYOK per-user em `decrypted_user_api_keys`, index.ts:36/54) \u2014 motor da aba An\u00e1lise IA. Nenhuma fn nova."
  ],
  "stack_changes": [
    "`src/App.tsx` \u2014 adicionar `const YouTubeVideoDetailPage = lazy(() => import('./pages/YouTubeVideoDetailPage.tsx'));` junto \u00e0 linha 30, e `<Route path=\"youtube/studio-yt/video/:videoId\" element={<YouTubeVideoDetailPage />} />` logo ap\u00f3s a linha 140.",
    "`src/pages/YouTubeVideoDetailPage.tsx` \u2014 NOVO. Display-only: l\u00ea `useParams().videoId`, resolve os hooks, renderiza header + 6 abas.",
    "`src/pages/YouTubeStudioPage.tsx` \u2014 refatorar de 592 \u2192 ~150 linhas: header + guardas de conex\u00e3o + `<Tabs>` de 4 abas. Componentes internos extra\u00eddos.",
    "`src/components/youtube/ChannelMetricsCard.tsx`, `RevenueCard.tsx`, `EditVideoDialog.tsx`, `VideosTable.tsx` \u2014 extra\u00eddos de YouTubeStudioPage.tsx (blocos 90-136, 139-193, 196-244, 252-429). Diret\u00f3rio j\u00e1 existe (s\u00f3 tem YouTubeUploadPanel.tsx).",
    "`src/components/youtube/video/PerformanceTab.tsx`, `RetentionTab.tsx`, `TrafficSourceTab.tsx`, `AudienceTab.tsx`, `TechnicalSheetTab.tsx`, `AiAnalysisTab.tsx` \u2014 NOVOS, um por aba.",
    "`src/components/youtube/AnalyticsUnavailable.tsx` \u2014 NOVO. Componente \u00fanico de estado degradado que recebe um motivo discriminado (`no_scope` | `api_disabled` | `no_data_yet` | `not_supported`) e renderiza a mensagem + CTA corretos. Hoje esses quatro casos colapsam num \u00fanico texto amber gen\u00e9rico (YouTubeStudioPage.tsx:106 e 354) \u2014 \u00e9 exatamente onde a UI mente por omiss\u00e3o.",
    "`src/lib/youtube-format.ts` \u2014 NOVO. Extrair `formatNumber`/`formatDuration`/`formatDate`/`formatSeconds`/`privacyBadge` de YouTubeStudioPage.tsx:47-87.",
    "`src/hooks/useYouTubeStudio.ts` \u2014 ESTENDER (n\u00e3o substituir): (a) `useYouTubeVideoReport(videoId, opts)` gen\u00e9rico, que serve as 4 abas variando `metrics`/`dimensions` e cujo `queryKey` inclui todos os par\u00e2metros; (b) `useYouTubeVideo(videoId)` que primeiro tenta o cache j\u00e1 pago de `['youtube','videos']` (o `useInfiniteQuery` da linha 148) antes de qualquer request \u2014 abrir um v\u00eddeo a partir da lista deve ser instant\u00e2neo e custar 0 de quota; (c) `useYouTubeVideoAnalysis(videoId, factSheet)` para a aba IA. Os hooks existentes (104-204) ficam intactos.",
    "`src/components/dashboard/DashboardSidebar.tsx` \u2014 promover o item plano da linha 97 a `<Collapsible>` espelhando o padr\u00e3o de Spaces (linhas 341-375), com sub-itens V\u00eddeos / Publicar / Desempenho. Aponta para `?tab=` do hub.",
    "`supabase/functions/youtube-data/index.ts` \u2014 MUDAN\u00c7A CIR\u00daRGICA, sem action nova: o helper `googleError` precisa propagar `error.errors[0].reason` no corpo, para o cliente distinguir `accessNotConfigured`/`SERVICE_DISABLED` (API desligada no Cloud) de `forbidden` (escopo) de `insufficientPermissions`. Sem isso `AnalyticsUnavailable` n\u00e3o tem como escolher a mensagem certa e a UI volta a mentir. Custo: 0 slots.",
    "NENHUMA edge function nova. NENHUMA migration. `ls supabase/functions | grep -v ^_ | wc -l` = 99/100 \u2014 o slot restante fica reservado."
  ],
  "ai_layer": "[\"ONDE \u2014 aba **An\u00e1lise IA** na p\u00e1gina por-v\u00eddeo (nunca um widget flutuante, nunca sobreposta aos n\u00fameros). O usu\u00e1rio chega nela DEPOIS de ver os dados crus nas 4 abas anteriores; a IA \u00e9 leitura de segunda ordem, n\u00e3o a fonte.\", \"CONTRATO DE ENTRADA \u2014 o cliente monta um **fact sheet** que \u00e9 literalmente o JSON dos `rows`+`columnHeaders` j\u00e1 devolvidos pelas queries das abas (mesmo cache TanStack, zero quota extra) e o envia como bloco de fatos para `generate-content`. O prompt de sistema instrui: interprete SOMENTE estes n\u00fameros; toda afirma\u00e7\u00e3o num\u00e9rica deve citar a chave do fact sheet que a originou; se o dado n\u00e3o estiver no bloco, diga que n\u00e3o est\u00e1 dispon\u00edvel.\", \"CONTRATO DE SA\u00cdDA \u2014 4 se\u00e7\u00f5es fixas: (1) O que os dados mostram; (2) Hip\u00f3tese mais prov\u00e1vel para o padr\u00e3o observado, rotulada como HIP\u00d3TESE; (3) Um experimento test\u00e1vel no pr\u00f3ximo v\u00eddeo; (4) O que N\u00c3O d\u00e1 para saber com os dados dispon\u00edveis. A se\u00e7\u00e3o (4) \u00e9 obrigat\u00f3ria \u2014 \u00e9 o ant\u00eddoto de alucina\u00e7\u00e3o embutido no formato.\", \"RASTREABILIDADE VIS\u00cdVEL \u2014 abaixo da an\u00e1lise, um `<Collapsible>` 'Dados enviados \u00e0 IA' exibindo o fact sheet exato. Se o usu\u00e1rio n\u00e3o consegue auditar a entrada, a sa\u00edda n\u00e3o \u00e9 verific\u00e1vel e a Lei 1 n\u00e3o \u00e9 satisfeita por constru\u00e7\u00e3o.\", \"PROVIDER \u2014 `useConfiguredProviders()` (src/hooks/useConfiguredProviders.ts) governa o seletor; s\u00f3 aparecem os providers com chave BYOK real ('s\u00f3 carrega para o usu\u00e1rio, op\u00e7\u00f5es dispon\u00edveis'). Sem NENHUMA chave: a aba renderiza um card 'Configure uma chave de IA em /dashboard/settings' \u2014 e as outras 5 abas continuam 100% funcionais. A aus\u00eancia de IA nunca degrada os dados.\", \"AGENTES PER-USER \u2014 o mesmo fact sheet \u00e9 o payload natural para `intent-orchestrate`/`intent-execute` numa fatia posterior (ex.: 'o agente l\u00ea a reten\u00e7\u00e3o e enfileira um reshape do trecho de maior audienceWatchRatio'). Escopo desta fatia: interpreta\u00e7\u00e3o read-only. A\u00e7\u00e3o aut\u00f4noma sobre o canal fica fora at\u00e9 haver GO expl\u00edcito.\", \"O QUE A IA N\u00c3O PODE FAZER \u2014 (a) produzir qualquer n\u00famero ausente do fact sheet, incluindo proje\u00e7\u00f5es, estimativas de receita ou benchmarks de nicho; (b) comparar com 'a m\u00e9dia do YouTube' (n\u00e3o temos esse dado); (c) prometer ou 'garantir' resultado; (d) atribuir views de um v\u00eddeo longo a um Short por subtra\u00e7\u00e3o \u2014 atribui\u00e7\u00e3o s\u00f3 via `insightTrafficSourceType`; (e) rodar automaticamente ao abrir a aba \u2014 \u00e9 sob demanda, por clique, porque consome chave/cota do usu\u00e1rio.\"]",
  "honesty_guards": [
    "RECEITA \u2014 `docs/bok/youtube-studio/11-api-surface-map.md:280` cita a doc oficial: channel reports n\u00e3o suportam m\u00e9tricas de receita/ad performance. Como `revenue_metrics` usa `ids=channel==MINE` (index.ts:290), o 403 \u00e9 estrutural. O texto atual em YouTubeStudioPage.tsx:166-167 \u2014 'o canal n\u00e3o est\u00e1 monetizado (fora do YouTube Partner Program)' \u2014 afirma um fato sobre o neg\u00f3cio do usu\u00e1rio que a API n\u00e3o sustenta e pode ser simplesmente falso. Trocar por: 'A API de Analytics n\u00e3o exp\u00f5e receita em relat\u00f3rios de canal \u2014 s\u00f3 em relat\u00f3rios de content owner (YouTube Partner Manager). Consulte a receita no YouTube Studio oficial.' E n\u00e3o criar aba de receita por-v\u00eddeo.",
    "SEM DADOS \u2260 ZERO \u2014 `reports.query` devolve `rows: []` com `columnHeaders` v\u00e1lidos para v\u00eddeos rec\u00e9m-publicados. O c\u00f3digo atual (`ChannelMetrics`, linha 111: `if (!metrics) return null`) some silenciosamente com o card. Renderizar explicitamente: 'Sem dados consolidados ainda \u2014 o YouTube Analytics leva at\u00e9 48h.' Renderizar '0' onde a API n\u00e3o devolveu linha \u00e9 fabricar dado.",
    "QUATRO CAUSAS DISTINTAS, QUATRO MENSAGENS \u2014 hoje qualquer falha de Analytics vira o mesmo amber gen\u00e9rico (linha 106). Separar: **sem escopo** \u2192 bot\u00e3o Reconectar (s\u00f3 isso resolve); **YouTube Analytics API desabilitada no projeto Google Cloud** \u2192 instru\u00e7\u00e3o de habilitar no Console, e N\u00c3O oferecer Reconectar, porque reconectar n\u00e3o conserta e faz o usu\u00e1rio girar em falso; **v\u00eddeo sem dados ainda** \u2192 mensagem temporal; **relat\u00f3rio n\u00e3o suportado** \u2192 limita\u00e7\u00e3o da API. Requer o `reason` propagado pelo `googleError`.",
    "DEGRADA\u00c7\u00c3O PARCIAL, NUNCA P\u00c1GINA EM BRANCO \u2014 sem `hasAnalyticsScope`, a p\u00e1gina por-v\u00eddeo ainda abre: Ficha t\u00e9cnica funciona (Data v3 puro) e as 4 abas anal\u00edticas mostram o card de escopo. A preced\u00eancia j\u00e1 est\u00e1 certa no hook (useYouTubeStudio.ts:116-117: analytics \u00e9 upgrade opcional, s\u00f3 a aus\u00eancia de `youtube.readonly` bloqueia) \u2014 a p\u00e1gina por-v\u00eddeo tem que herdar essa mesma disciplina.",
    "SHORTS \u2014 nunca calcular watch-time\u00f7views no cliente. Desde 31/03/2025 'view' de Short \u00e9 play-start sem watch-time m\u00ednimo e a AVD usa engaged views como denominador. Exibir `averageViewDuration` e `engagedViews` como a API entrega, com tooltip explicando o denominador quando `creatorContentType=SHORTS`.",
    "ATRIBUI\u00c7\u00c3O \u2014 nenhum widget de 'este Short trouxe X views para o v\u00eddeo longo' por subtra\u00e7\u00e3o de `viewCount` da Data v3 (que \u00e9 cumulativo de todas as fontes). A \u00fanica superf\u00edcie atributiva leg\u00edtima \u00e9 a aba Origem do tr\u00e1fego, e ainda assim rotulada como 'origem declarada pelo YouTube', n\u00e3o como causalidade provada.",
    "hook_rate \u2014 `creative_metrics.hook_rate` \u00e9 lida em 3 lugares e escrita em ZERO. A p\u00e1gina por-v\u00eddeo pode EXIBIR um tile derivado (`engagedViews/views`, ambos vindos da API) com a f\u00f3rmula vis\u00edvel no tooltip, mas N\u00c3O deve persistir em `creative_metrics` a partir do cliente: n\u00e3o h\u00e1 writer service-role, e `creative_metrics.source` \u00e9 CHECK fechado ('affiliate_click','organic','postback') sem valor para YouTube. Escrever exigiria migration + /security-review \u2014 fora desta fatia.",
    "INSCRITOS \u2014 `subscribersGained/Lost` do Analytics \u00e9 atribui\u00e7\u00e3o por v\u00eddeo no per\u00edodo; `channel.statistics.subscriberCount` da Data v3 \u00e9 o total do canal. S\u00e3o grandezas diferentes e n\u00e3o devem aparecer lado a lado sem r\u00f3tulo, sen\u00e3o o usu\u00e1rio l\u00ea como contradi\u00e7\u00e3o.",
    "O rodap\u00e9 de cada aba anal\u00edtica declara o per\u00edodo exato consultado e a fonte ('YouTube Analytics API v2 \u00b7 reports.query \u00b7 dimensions=X'). M\u00e9trica sem proced\u00eancia declarada \u00e9 m\u00e9trica n\u00e3o audit\u00e1vel."
  ],
  "open_questions": [
    "A **YouTube Analytics API** est\u00e1 de fato habilitada no projeto Google Cloud? N\u00e3o verifiquei materialmente (Lei 1 \u2014 c\u00e9rebro sem m\u00e3os neste ponto). Se estiver desligada, TODAS as abas anal\u00edticas caem em `accessNotConfigured` independentemente dos 4 escopos concedidos, e o `AnalyticsUnavailable` com motivo discriminado passa de refinamento a pr\u00e9-requisito. Verifica\u00e7\u00e3o: chamar `video_metrics` uma vez e ler o `reason` do 403.",
    "O Usu\u00e1rio Zero j\u00e1 reconectou concedendo os 4 escopos? `useYouTubeConnection` deriva de `social_accounts.scopes` (useYouTubeStudio.ts:107) \u2014 um `SELECT scopes FROM social_accounts WHERE platform='youtube'` resolve antes de qualquer c\u00f3digo.",
    "A aba An\u00e1lise IA deve debitar mcoCoins (self-bill do `generate-content`) ou rodar puramente na chave BYOK do usu\u00e1rio sem d\u00e9bito? Afeta se o bot\u00e3o precisa de confirma\u00e7\u00e3o de custo.",
    "A tabela do hub deve ganhar ordena\u00e7\u00e3o por coluna (Views/Likes) via `dimensions=video` + `sort=-views` (relat\u00f3rios #28-32, teto de 200) ou basta a ordem cronol\u00f3gica atual do `uploadsPlaylistId`? A primeira \u00e9 uma chamada Analytics adicional por ordena\u00e7\u00e3o.",
    "Reservar o \u00faltimo slot de edge function (99/100): confirmo que esta fatia n\u00e3o gasta nenhum, mas vale decidir com o Sovereign para que ele fica.",
    "Contagem de coment\u00e1rios existe na Data v3 (`statistics.commentCount`), mas LER os coment\u00e1rios exige `commentThreads` \u2014 action inexistente hoje. Uma aba Coment\u00e1rios na p\u00e1gina por-v\u00eddeo \u00e9 desejada nesta fatia ou fica para depois? Ela caberia dentro de `youtube-data` sem slot novo.",
    "Persist\u00eancia de hook_rate: quer que eu abra uma fatia separada (migration para estender o CHECK de `creative_metrics.source` + writer service-role + /security-review), ou o tile derivado read-only basta por ora?"
  ]
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
> * **Sessão Anterior**: [[2026-07-20 - agent-acb02abbd33f7aa6d]]
> * **Próxima Sessão**: [[2026-07-20 - agent-acfb8aa0683e484ca]]
%% --- TIMELINE END --- %%
