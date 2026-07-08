# SOP: WebGL Canvas Stabilization & Layout Optimization

**Status:** ACTIVE · v1.0 · 2026-06-12
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Laws:** Lei 1 (Materialidade) + Lei 2 (Processo Antecipado). Nasce de um problema real
de cintilação (flickering/piscadas) do Mega Brain WebGL Canvas no dashboard `/dashboard/core-fable`
quando mensagens eram enviadas ou quando o nível de intensidade de som se alterava.

---

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (ou qualquer subagent frontend)
- **Reviewer:** Sovereign (valida visualmente no browser)
- **Owner:** Sovereign (blast radius = UX do Core Fable / fidelidade do Mega Brain)

---

## ⚠️ Diagnóstico Técnico (As Duas Causas do Flicker)

1. **Conflito de Compositor de GPU (backdrop-filter):**
   O uso de classes CSS como `backdrop-blur-*` (que geram a propriedade CSS `backdrop-filter: blur(...)`) em elementos flutuantes (como painéis, barras de ferramentas, cabeçalhos) posicionados diretamente acima ou ao lado de um Canvas 3D (WebGL) ativo força o navegador a recompilar a árvore de composição de janelas 2D/3D a cada frame de renderização. Qualquer alteração de estado no React que cause repaints desencadeia piscadas pretas ou transparentes no WebGL Canvas.
2. **Micro-jumps por Updates em React Effects:**
   Atualizar uniforms sensíveis a animações (como `u_intensity` ou `u_thinking`) diretamente no bloco do `useEffect` a cada mudança de prop gera atualizações discretas e saltos visuais.

---

## 📋 Regras de Implementação (Gates de Estabilidade)

### 1. Proibição de `backdrop-blur` sobre ou junto a Canvas WebGL
* **Regra:** Nunca utilizar classes de desfoque de fundo (`backdrop-blur`, `backdrop-blur-sm`, `backdrop-blur-md`, `backdrop-blur-lg`) em headers, sidebars, toolbars ou painéis flutuantes (ex: `A2UIRenderer` ou HUDs) que dividem o mesmo viewport com o WebGL.
* **Alternativa:** Substituir por cores escuras sólidas/semitransparentes de alto contraste (como `bg-black/95`, `bg-[#050508]` ou `bg-zinc-950`).

### 2. Easing de Uniforms no loop `useFrame` e Desacoplamento de Estados React
* **Regra:** Em vez de mapear atualizações contínuas de props de alta frequência (como frequências de áudio ou nível de ressonância) diretamente para uniformes através de props do React (o que força o Canvas e componentes filhos a re-renderizarem constantemente), utilize uma variável de escopo ou módulo (ou subscrição direta) para passar os valores de volume/áudio ao loop de renderização do Three.js (`useFrame`) de forma imperativa.
* **Implementação:** Interpole o valor no loop de renderização R3F (`useFrame`):
  ```typescript
  // Exemplo de Easing e Leitura de Variável de Módulo
  let currentAudioIntensity = 0;
  
  export function setVisualizerIntensity(level: number) {
    currentAudioIntensity = level;
  }

  useFrame((state) => {
    if (meshRef.current) {
      const mat = meshRef.current.material as THREE.ShaderMaterial;
      const curInt = mat.uniforms.u_intensity.value;
      const targetIntensity = currentAudioIntensity;
      // Interpolação suave a cada frame
      mat.uniforms.u_intensity.value = curInt + (targetIntensity - curInt) * 0.15;
    }
  });
  ```

---

## 🧪 Verification Gates

| Gate | Comando / Inspeção | Pass |
|------|--------------------|------|
| **G1 Sem backdrop-blur** | `grep -r "backdrop-blur" src/pages/CoreFablePage.tsx src/components/core-fable/` | `0` ocorrências nas áreas do canvas |
| **G2 Easing ativo** | Verificar no código do visualizador se as variáveis atualizam via `useRef` + `useFrame` | Uniforms interpolados suavemente |
| **G3 Teste E2E visual** | Enviar mensagem no chat e verificar se o canvas continua renderizando liso | 0 piscadas ou falhas de GPU |

---

## Anti-patterns
- ❌ Reintroduzir `backdrop-blur` em elementos flutuantes acima do WebGL para "ficar bonito" (causa quebra de performance e piscadas).
- ❌ Atualizar uniforms de alta frequência via `useEffect` puro sem passar pelo easing do loop de animação `useFrame`.
